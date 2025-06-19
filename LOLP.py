import requests
import pandas as pd
import io
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
import pvlib
import math
import numpy as np
from pvlib import shading, irradiance, soiling
from BatterySimu import*
import matplotlib.pyplot as plt
from skopt import gp_minimize
from skopt.space import Integer
from skopt.utils import use_named_args
from functools import partial
from datetime import datetime, timedelta
from enums import SystemMode
from skopt import Optimizer
from scipy.stats import qmc
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.termination import get_termination
import numpy as np
import pandas as pd
 
### --- DEFINITION OF USEFUL CLASSES --- ###

class Panels:
    def __init__(self, power, eta_tot, name=None, alpha=None, area=None, string_num=1, string_dist=None, clean_freq = 12, rainthresh = 7):
        self.name = name
        self.eta_tot = eta_tot
        self.power = power
        self.alpha = alpha
        self.area = area
        self.string_num = string_num
        self.string_dist = string_dist
        self.clean_freq = f'{clean_freq}W'
        self.rainthresh = rainthresh

        # If SOC_min is given, compute E_min from it
        if area is not None:
            self.area = area
        else:
            self.area = self.power /(0.18 * 1000) #Approx size of panel depending on power

        if alpha is not None: 
            self.alpha = alpha
        else:
            self.alpha = -33/10000 #Default mean value for the temperature coefficient of a panel


class Load:
    def __init__(self, name, df):
        self.name = name
        self.df = df 

class Location:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class PCU:
    def __init__(self, eta_cable = 2, max_charge_current = None, capacity = None, pack_voltage = None, eta_CC = 0.93, eta_inverter = 0.87):
        self.capacity = capacity # Maximum power [W] that PCU provide to load
        self.pack_voltage = pack_voltage # 12, 24, 48, 96, 120, 240 V of battery pack
        self.eta_pv_to_load = eta_CC**0.5 * eta_inverter * ((1-eta_cable/100)**2)# **0.5 because CC takes into account the MPPT converter and the battery charger converter. Only the former is used here.
        self.eta_pv_to_batt = eta_CC * ((1-eta_cable/100)**2)
        self.eta_batt_to_load = eta_inverter * ((1-eta_cable/100)**2)
        self.max_charge_current = max_charge_current 

### --- DATA FETCHING --- ###

def change_timestamp(df, Location):
    """
    Input: 
    - df: Dataframe to change from year, month, day, hour stamp to standard local time index
    - longitude, latitude: of the concerned system
    Output: modified index 
    """
    
    df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])
    df.set_index('datetime', inplace=True)
    df.drop(columns=['Year', 'Month', 'Hour', 'Minute', 'Day'], inplace=True)

    timezone_finder = TimezoneFinder()
    tz = timezone_finder.timezone_at(lng=Location.longitude, lat=Location.latitude)
    df.index = df.index.tz_localize(tz) 
    
    return df

def fetch_irradiation(Location, year):

    """
    Input: Location object with 'latitude' and 'longitude' attributes, and the desired 'year' as a string.
    Output: DataFrame containing DNI, DHI, GHI, air temperature, and wind speed from the 
    NSRDB Meteosat Prime Meridian dataset.
    """

    API_KEY = 'JkGTQdgblLszU34Nu5qsWwskgkTQ8CwqWQfuNagI'
    wkt_point = f'POINT({Location.longitude} {Location.latitude})'
    url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/msg-iodc-download.csv'

    params = {
        'api_key': API_KEY,
        'wkt': wkt_point,
        'names': year,
        'interval': '60',
        'utc': 'false',
        'attributes': 'dni,dhi,ghi,air_temperature,wind_speed',
        'email': 'basti.gst@outlook.com',
        'full_name': 'Bastien Gaussent',
        'affiliation': 'EPFL',
        'reason': 'Solar modeling',
        'mailing_list': 'false'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text), skiprows=2)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

    #Change the index to standardized timestamp
    df = change_timestamp(df, Location)
    #Rename columns for practicality
    df.rename(columns={'GHI': 'GHI_sat','Wind Speed': 'Wind'}, inplace=True)

    return df

### --- POLLUTION FECTHING --- ###

def convert_UNIX(df, Location, year):
    """
    Converts a DataFrame with UNIX timestamps to localized datetime format,
    and appends datetime components (year, month, day, hour, minute).

    Parameters:
        df (pd.DataFrame): DataFrame containing a 'UNIX' column.
        Location (class): Longitude/Latitude of the location.

    Returns:
        pd.DataFrame: DataFrame with local time index and extracted datetime components.
    """

    #Transform UNIX to normal timestamp
    df = df.sort_values(by='UNIX', ascending=True)
    df['timestamp'] = pd.to_datetime(df['UNIX'], unit='s')
    
    # Extract Year, Day of Year, and Hour from the timestamp
    df['Year'] = df['timestamp'].dt.year
    df['Month'] = df['timestamp'].dt.month
    df['Day'] = df['timestamp'].dt.day  
    df['Hour'] = df['timestamp'].dt.hour
    df['Minute'] = 0
    
    # Drop the timestamp column
    df = df.drop(columns=['UNIX', 'timestamp'])
    df = change_timestamp(df, Location)
    df['timestamp'] = pd.to_datetime(df.index)

    ### Select only the wanted year
    df = df[df['timestamp'].dt.year == year]
    df = df.drop(columns=['timestamp'])
      
    return df 

def get_UNIX_range(Location, year):
    """
    Returns UNIX UTC timestamps for Jan 1, 00:00 and Feb 28, 23:30 in *local time* 
    for a given lat/lon. Returned times are in UTC as required by OpenWeather API.
    """

    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=Location.latitude, lng=Location.longitude)
    if tz_str is None:
        raise ValueError("Could not determine timezone from coordinates.")

    local_tz = pytz.timezone(tz_str)

    # Create local datetime objects
    start_local = local_tz.localize(datetime(year, 1, 1, 0, 0))
    end_local = local_tz.localize(datetime(year+1, 1, 1, 23, 30))  # Note: not leap year

    # Convert to UTC, then to UNIX timestamp
    start_utc_unix = int(start_local.astimezone(pytz.utc).timestamp())
    end_utc_unix = int(end_local.astimezone(pytz.utc).timestamp())

    return start_utc_unix, end_utc_unix

def align_df(df, year, Location):

    """
    Align a DataFrame to a 1-hour datetime index for a given year and timezone.
    Matches timestamp structure (month, day, hour, minute, second), and reindexes
    the result to the new year's hourly time range.

    Parameters:
        df (pd.DataFrame): DataFrame with timezone-aware DatetimeIndex
        year (int): Target year
        tz (str): Timezone string (e.g., 'Asia/Kolkata')

    Returns:
        aligned_df (pd.DataFrame): Reindexed DataFrame aligned to target hourly timestamps
    """
    # Target time range: every 1 hour in the given year
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=Location.latitude, lng=Location.longitude)
    tz = pytz.timezone(tz_str)
    times = pd.date_range(start=f"{year}-01-01 00:00", end=f"{year}-12-31 23:30", freq="1h", tz=tz)

    # Structure key for matching: (month, day, hour, minute, second)
    df_struct = df.index.map(lambda dt: (dt.month, dt.day, dt.hour, dt.minute, dt.second))
    times_struct = times.map(lambda dt: (dt.month, dt.day, dt.hour, dt.minute, dt.second))

    # Create map from structure to original index
    df_map = dict(zip(df_struct, df.index))

    # Find matching indices for each target time
    matching_idx = [df_map.get(struct, None) for struct in times_struct]

    # Keep only matches (drop missing ones)
    mask_valid = [i is not None for i in matching_idx]
    matched_df = df.loc[[i for i in matching_idx if i is not None]].copy()
    matched_times = times[mask_valid]

    # Replace index with target times
    matched_df.index = matched_times

    return matched_df

def formatValidator(df, Location, year):
    """
    Prepares the user input solar data for concatenation with the other data. 
    - Changes the timestamp to standardized
    - Adapts the length of the dataframe
    - Resamples for 30min 
    - Changes the year to correct value
    """
    df = change_timestamp(df, Location)
    df = align_df(df, year, Location)
    df = df.resample('30min').mean()
    df.index = df.index.map(lambda ts: ts.replace(year=year))

    return df

def fetch_pollution(Location, year):
    """
    Fetches hourly PM2.5 and PM10 air pollution data from OpenWeather's
    historical API for a given time range and location.

    Parameters:
        start_unix (int): Start time as UNIX timestamp (UTC).
        end_unix (int): End time as UNIX timestamp (UTC).
        Location (class): Latitude/longitude of the location.

    Returns:
        pd.DataFrame: Cleaned DataFrame with PM2.5, PM10, and local datetime index.
    """
    # MODIFY API TO CORRECT ACCOUNT
    api_key = 'fcc56e7d5838b4b21a971c7af302e544'
    start_unix, end_unix = get_UNIX_range(Location, year)
    
    url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={Location.latitude}&lon={Location.longitude}&start={start_unix}&end={end_unix}&appid={api_key}'
    response = requests.get(url)
    pm25_list = []
    pm10_list = []
    timestamps = []

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Iterate through the available data points (entries)
        for entry in data['list']:
            pm25 = entry['components']['pm2_5']
            pm10 = entry['components']['pm10']
            timestamp = entry['dt']  # Timestamp in UNIX time
            
            # Append the values to the lists
            pm25_list.append(pm25)
            pm10_list.append(pm10)
            timestamps.append(timestamp)
    else:
        print(f"Error: {response.status_code}")

    df = pd.DataFrame({
            'UNIX': timestamps,
            'PM2.5': pm25_list,
            'PM10': pm10_list
        })

    df = convert_UNIX(df, Location, year)
    df.index = df.index.map(lambda ts: ts.replace(year=year-4))

    return df

def fetch_rain_data(Location, year):
    """
    Fetches hourly precipitation data from NASA POWER API 
    for a given time range and location.

    Parameters:
        start_unix (int): Start time as UNIX timestamp (UTC).
        end_unix (int): End time as UNIX timestamp (UTC).
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        pd.DataFrame: Cleaned DataFrame with PM2.5, PM10, and local datetime index.
    """

  # Define the API endpoint and parameters
    base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    start_date = f"{year}&0101"  # Start date (YYYYMMDD format)
    end_date = f"{year}&1231"    # End date (single day for a smaller range)
    parameters ="PRECTOTCORR" 
    community = "RE"

    url = f"{base_url}?latitude={Location.latitude}&longitude={Location.longitude}&start={start_date}&end={end_date}&parameters={parameters}&community={community}&format=CSV"
    
    response = requests.get(url)

    if response.status_code == 200:
    
        header_end_index = response.text.find("-END HEADER-") + len("-END HEADER-")
        data_content = response.text[header_end_index:].strip()  # Get everything after the header
    
        data_cl = pd.read_csv(io.StringIO(data_content))
    
    else:
        
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")

    data_cl.rename(columns={
                     'PRECTOTCORR': 'Rain',                  
                     'MO': 'Month',
                     'YEAR': 'Year',
                     'DY': 'Day',
                     'HR': 'Hour'}, inplace=True)
    
    data_cl['Minute'] = 0 
    df = change_timestamp(data_cl, Location)

    return df

def solarPositions(df, Location, year):
    """
    Adds solar zenith and azimuth angles to the DataFrame, based on location and year.
    
    Parameters:
    - df: DataFrame with 30-min index (will be overwritten if not)
    - Location: object with .latitude and .longitude
    - year: int

    Returns:
    - df: with columns 'Solar Zenith' and 'Solar Azimuth' added
    - solar_position: full solar position DataFrame (optional)
    """

    # --- Time and Location ---
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=Location.longitude, lat=Location.latitude)

    # Ensure correct datetime index
    times = pd.date_range(f"{year}-01-01 00:00", f"{year}-12-31 23:30", freq="30min", tz=tz)
    df = df.copy()
    df = df.reindex(times)

    # --- Compute solar position ---
    alt = pvlib.location.lookup_altitude(Location.latitude, Location.longitude)
    solar_pos = pvlib.solarposition.get_solarposition(times, Location.latitude, Location.longitude, altitude=alt)

    # --- Add to DataFrame ---
    df["Solar Zenith"] = solar_pos["apparent_zenith"].values
    df["Solar Azimuth"] = solar_pos["azimuth"].values

    return df

def fetch_dataFrame(Location, year, df_solar, progress_callback):
    """
    Acquires the data from the different APIs, combined them into a unified dataframe and resamples them
    for a granularity of 30min
    """
    if df_solar is None:
        df_irr = fetch_irradiation(Location, year)  #Rain data from 2017 to 2019
        print("Using API solar data")
    else:
        df_irr = formatValidator(df_solar, Location, year)
        print("Using user input solar data")

    progress_callback(11)
    df_pol = fetch_pollution(Location, year+4)  #PM data from 2021 to 2023
    progress_callback(17)
    df_rain = fetch_rain_data(Location, year)   #Rain data from 2017 to 2019
    progress_callback(23)
    #Concatenate and re_sample
    df_combined = pd.concat([df_irr, df_pol, df_rain])
    df_fin = df_combined.resample('30min').mean()
    df_fin = df_fin.interpolate(method='linear', limit_direction='both')
    progress_callback(29)
    df_last = solarPositions(df_fin, Location, year) #Acquires solar positions and zenith
    progress_callback(35)
    
    return  df_last

### --- DATA COMPLETION --- ###

def PV_params(Panels, Location):
 
    PV_Length = math.sqrt(Panels.area / 1.65)
    PV_height = np.sin(np.radians(abs(Location.latitude)))*PV_Length 
    R_dist = Panels.string_dist + np.cos(np.radians(abs(Location.latitude)))*PV_Length
    GCR = PV_Length / R_dist
    
    return GCR, R_dist, PV_height

def diff_shadow(df, Panels, Location):
    """
    Adjusts the diffuse horizontal irradiance (DHI) in a DataFrame to account for
    diffuse shading losses caused by row-to-row shadowing in a solar panel array. Model based on PVLib
    """

    # --- Location and Time ---
    '''timezone_finder = TimezoneFinder()
    tz = timezone_finder.timezone_at(lng=Location.longitude, lat=Location.latitude)
    times1 = pd.date_range( f'{year}-1-1 0:00', f'{year}-12-31 23:00', freq='30min', tz=tz)'''

    # --- System parameters ---
    GCR, R_dist, PV_height = PV_params(Panels, Location)
   
    # --- Diffuse Irradiance Loss caused by row to row sky diffuse shading --- 
    psi = shading.masking_angle_passias(abs(Location.latitude), GCR) #The elevation angle below which diffuse irradiance is blocked.
    shading_loss = shading.sky_diffuse_passias(psi)
    
    df['DHI'] = df['DHI'] * (1 + (1 - shading_loss) * (Panels.string_num - 1)) / Panels.string_num if Panels.string_num > 1 else df['DHI']
    
    return df

def direct_shadow(df, Panels, Location):
    """
    Applies a correction to the Direct Normal Irradiance (DNI) in the input DataFrame 
    to account for row-to-row shading losses caused by direct (beam) irradiance blocking 
    in multi-row PV systems. Model based on PVLib
    """

    # --- System parameters ---
    PV_Length = math.sqrt(Panels.area / 1.65)
    GCR, R_dist, PV_height = PV_params(Panels, Location)

    #Finded projected zenith angle
    psza = pvlib.shading.projected_solar_zenith_angle(df["Solar Zenith"], df["Solar Azimuth"], abs(Location.latitude), 180)

    shaded_fraction_PV = np.where(
        psza < 0,  # Only apply shading when sun is in front of the east-most row
        pvlib.shading.shaded_fraction1d(
            df["Solar Zenith"],
            df["Solar Azimuth"],
            axis_azimuth=180,               # South-facing
            shaded_row_rotation=abs(Location.latitude),    # Same tilt for both rows
            axis_tilt=0,
            collector_width=PV_Length * np.cos(np.radians(abs(Location.latitude))),
            pitch=R_dist,                   # Horizontal row spacing
            surface_to_axis_offset=0,
            cross_axis_slope=0,
            shading_row_rotation=abs(Location.latitude),
        ),
        0
    )

    df['DNI'] = df['DNI'] * (1 + (1 - shaded_fraction_PV) * (Panels.string_num - 1)) / Panels.string_num  if Panels.string_num > 1 else df['DNI']

    return df

def horizon_shading(df, Location):
    """
    Adjusts the Direct Normal Irradiance (DNI) in the DataFrame to account for shading
    caused by the local horizon (e.g., mountains, buildings, or terrain). Model based on PVLib
    """
    horizon_profile, _ = pvlib.iotools.get_pvgis_horizon(Location.latitude, Location.longitude)

    # --- Modifying the DHI component ---
    horizon_elevation_data = np.interp(df["Solar Azimuth"], horizon_profile.index, horizon_profile)
    horizon_elevation_data = pd.Series(horizon_elevation_data, df.index)
    df['DNI'] = np.where(df["Solar Zenith"] > horizon_elevation_data, df['DNI'], 0)
    
    return df

def soiling_effect(df, Location, Panels):
    """
    Applies the HSU soiling loss model to estimate the impact of particulate matter
    (PM2.5 and PM10) and rainfall on solar panel performance over time.
    """

    cleaning_threshold = Panels.rainthresh
    cleaning_interval = Panels.clean_freq

    # --- Define useful data structures --- 
    depo_veloc = {'2_5': 0.0009, '10': 0.004}  # default values from [1] (m/s)
    rain_accum_period = pd.Timedelta('30min')     # default
       
    rainfall = df['Rain'].fillna(0)
    pm2_5 = df['PM2.5'] * 10e-6 #PM need be in g/m3
    pm10 = df['PM10'] * 10e-6 

    # --- Preparation of manual cleaning breakpoints --- 
    start_date = rainfall.index.min()
    end_date = rainfall.index.max()

    cleaning_dates = pd.date_range(start=start_date, end=end_date, freq=cleaning_interval, tz=df.index.tz)
    cleaning_dates = cleaning_dates.insert(0, start_date)  # ensure it starts at the beginning
    if cleaning_dates[-1] < end_date:
        cleaning_dates = cleaning_dates.append(pd.DatetimeIndex([end_date]))

    #cleaning_dates = cleaning_dates[~cleaning_dates.index.duplicated(keep='first')]
    soiling_segments = []

    # --- Loop the HSU Soiling model ---
    for i in range(len(cleaning_dates)-1):
        seg_start = cleaning_dates[i]
        seg_end = cleaning_dates[i + 1]
    
        rainfall_seg = rainfall[seg_start:seg_end]
        pm2_5_seg = pm2_5[seg_start:seg_end]
        pm10_seg = pm10[seg_start:seg_end]
    
        soiling_seg = soiling.hsu(
            rainfall_seg,
            cleaning_threshold,
            abs(Location.latitude),
            pm2_5_seg,
            pm10_seg,
            depo_veloc=depo_veloc,
            rain_accum_period=rain_accum_period
        )
    
        # Append to the list
        soiling_segments.append(soiling_seg)
    
    # Concatenate all the segments into a single series
    soiling_ratio = pd.concat(soiling_segments)
    
    # Optional: sort index if needed
    soiling_ratio = soiling_ratio.sort_index()
    soiling_ratio.name = 'Soiling ratio'

    df = pd.concat([df, soiling_ratio], axis=1)
    df = df[~df.index.duplicated(keep='first')]

    return df

def compute_ghi(df):
    """ 
    Computes Global Horizontal Irradiance (GHI) based on DHI, DNI, and solar zenith angle.
    """
        
    df['GHI'] = df['DHI'] + np.cos(np.radians(df["Solar Zenith"].values))*df['DNI']

    return df

def fetch_POA(df, Location):
    """
    Calculates POA using 'GHI' if available, otherwise falls back to 'GHI_sat'.
    Assumes solar position columns are already present in df. Compute POA
    """

    ghi_col = 'GHI'

    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=abs(Location.latitude),
        surface_azimuth=180,
        dni=df['DNI'].values,
        ghi=df[ghi_col].values,
        dhi=df['DHI'].values,
        solar_zenith=df["Solar Zenith"].values,
        solar_azimuth=df["Solar Azimuth"].values
    )

    df['POA'] = POA_irradiance['poa_global']
    return df

def cell_temp(df):
    """
    Estimates the PV cell temperature using the PVsyst model and default coefficients 
    for land-based systems. The resulting temperature is added to the DataFrame.
    """
    
    # --- Cell Temperature using the PVSyst default values ---
    heat_loss_coeffs = {'default_PVSyst_coeffs_for_land_systems': [29.0, 0, 'C8', 'solid']}
    T_cell = pvlib.temperature.pvsyst_cell(
            poa_global=df['POA'],
            temp_air=df['Temperature'],
            wind_speed=df['Wind'],
            u_c=heat_loss_coeffs['default_PVSyst_coeffs_for_land_systems'][0],
            u_v=heat_loss_coeffs['default_PVSyst_coeffs_for_land_systems'][1],
        )
    df['Cell Temperature'] = T_cell

    return df

def fetch_power(df, Panels):

    #ASSUMED FIXED # to review
    #Takes into account shading from neighboring elements, PV mismatch, Nameplate rating and Light Induced degradation
    df['Output Power'] = pvlib.pvsystem.pvwatts_dc(df['POA'], df['Cell Temperature'], Panels.power * Panels.string_num, Panels.alpha) * Panels.eta_tot * df['Soiling ratio']

    return df

def compute_power_slow(df, Panels, Location):

    df = horizon_shading(df, Location)

    df = diff_shadow(df, Panels, Location)

    df = direct_shadow(df, Panels, Location)

    df = soiling_effect(df, Location, Panels)

    df = compute_ghi(df)

    df = fetch_POA(df, Location)

    df = cell_temp(df)

    df = fetch_power(df, Panels)

    return df

def compute_power_fast(df, Panels, Location):

    df = soiling_effect(df, Location, Panels)
    
    df = compute_ghi(df)

    df = fetch_POA(df, Location)

    df = cell_temp(df)

    df = fetch_power(df, Panels)

    return df

def ENS_calc_slow(df, PCU, Battery):
    """
    Slow but improved ENS calculation using a step-by-step BatteryModel simulation.
    """
    dt = 0.5 # time interval: 30min = 0.5h
    batt_energy_min = Battery.SOC_min * Battery.C_nom * Battery.V_nom * Battery.n_para * Battery.n_series

    # --- new batt_power column ---
    # Calculs préalables
    PV_to_load = df["Output Power"] * PCU.eta_pv_to_load
    power_diff = PV_to_load - df["Load Power"]
    # Condition : surplus PV → charge batterie
    charge_cond = power_diff >= 0
    charge_power = (df["Output Power"] - df["Load Power"]/PCU.eta_pv_to_load) * PCU.eta_pv_to_batt
    # Condition : déficit PV → décharge batterie
    discharge_power = (df["Load Power"] - PV_to_load) / PCU.eta_batt_to_load
    # Assemblage dans une seule colonne
    df["Battery Power"] = np.where(charge_cond, charge_power, -discharge_power)

    # --- Init any important values
    LOL_count = 0.
    ENS_count = 0.
    battery_left = [0 for _ in range(len(df))]
    battery_soc = [0 for _ in range(len(df))]
    battery_cycle = [0 for _ in range(len(df))]
    battery_soh = [0 for _ in range(len(df))]
    cell_volt = [0 for _ in range(len(df))]
    model = BatteryModel(Battery)
    
    # Convert to NumPy for speed
    load_power = df["Load Power"].values
    output_power = df["Output Power"].values
    battery_power = df["Battery Power"].values
    temperature = df["Temperature"].values

    battery_left[0], battery_soc[0], battery_cycle[0], battery_soh[0], cell_volt[0] = model.getInfo()

    for i in range(len(df)-1):
        
        #Model maximum charge controller current
        V_pack = cell_volt[i] * Battery.n_series
        I_charging = battery_power[i] / V_pack

        if I_charging > PCU.max_charge_current and battery_power[i]>0:
            #print(f"Power was clipped from {battery_power[i]} to {PCU.max_charge_current * V_pack}")
            battery_power[i] = PCU.max_charge_current * V_pack #Clipped to max current

        #Run that model  
        model.RunModel(temperature[i], battery_power[i])
        battery_left[i + 1], battery_soc[i + 1], battery_cycle[i+1], battery_soh[i+1], cell_volt[i+1] = model.getInfo()

        # Check for NaN and exit if any variable is NaN
        if (np.isnan(battery_left[i + 1]) or
            np.isnan(battery_soc[i + 1]) or
            np.isnan(battery_cycle[i + 1])):
            print(f"NaN detected at step {i+1}. Stopping execution.")
            exit(1)

        #print(f"Step {i+1}: Battery Left = {battery_left[i+1]:.2f}%, SOC = {battery_soc[i+1]:.2f}%, Cycle = {battery_cycle[i+1]:.0f}")
        # Check for NaN and exit if any variable is NaN

        ENS_count += max(0,load_power[i] * dt - output_power[i] * PCU.eta_pv_to_load * dt - PCU.eta_batt_to_load * (max(0,battery_left[i] - battery_left[i+1])))
    
    LOLP_ratio = LOL_count / (df["Load Power"] > 0).sum()
    ENS_ratio = ENS_count/ (df["Load Power"].sum()*dt) # *dt: conversion W -> Wh
    print(f"Source computed LOLP is {LOLP_ratio}")
    print(f"Total Wh needed is {df["Load Power"].sum()*dt}")
    print(f"The total ENS count is {ENS_count}")
    

    # Write results back to DataFrame
    df["Battery Left"] = battery_left
    df["Battery SOC"] = battery_soc
    df["Cycle"] = battery_cycle
    df["Battery SOH"] = battery_soh

    return df, LOLP_ratio, ENS_ratio


def ENS_calc_fast(df, PCU, BatteryFast):
    
    dt = 0.5 # time interval: 30min = 0.5h
    batt_energy_min = BatteryFast.SOC_min * BatteryFast.C_nom * BatteryFast.V_nom

    # --- new batt_power column ---
    # Calculs préalables
    PV_to_load = df["Output Power"] * PCU.eta_pv_to_load
    power_diff = PV_to_load - df["Load Power"]
    # Condition : surplus PV → charge batterie
    charge_cond = power_diff >= 0
    charge_power = (df["Output Power"] - df["Load Power"]/PCU.eta_pv_to_load) * PCU.eta_pv_to_batt
    # Condition : déficit PV → décharge batterie
    discharge_power = (df["Load Power"] - PV_to_load) / PCU.eta_batt_to_load
    # Assemblage dans une seule colonne
    df["Battery Power"] = np.where(charge_cond, charge_power, -discharge_power)

    LOL_count = 0
    ENS_count = 0
    model = BatteryModel_fast(BatteryFast)
    # Convert to NumPy for speed
    load_power = df["Load Power"].values
    output_power = df["Output Power"].values
    battery_power = df["Battery Power"].values
    temperature = df["Temperature"].values
    bat_SOC, bat_left = model.RunModel_fast(temperature,battery_power)

    for i in range(len(df)-1):
        ENS_count += max(0,load_power[i] * dt - output_power[i] * PCU.eta_pv_to_load * dt - PCU.eta_batt_to_load * (max(0,bat_left[i] - bat_left[i+1])))

    LOLP_ratio = LOL_count / (df["Load Power"] > 0).sum()
    ENS_ratio = ENS_count / (df["Load Power"].sum()*dt) # *dt: conversion W -> Wh

    return df, LOLP_ratio, ENS_ratio

### Optimization Tool ###

def SearchSpace(df):

    ghi_col = 'GHI'
    E_daily = (df["Load Power"].resample("1D").mean() * 24).mean()

    step_bat = 25; step_pv = 25; DOD_max = 0.8; eta_bat = 0.5; eta_pv = 0.75
    PSH = ((df[ghi_col] * 0.5).resample("1D").sum()).mean() / 1000

    # Battery bounds
    Cbat_min = round((0.5 * E_daily) / (DOD_max * eta_bat * step_bat)) * step_bat
    Cbat_max = round((2 * E_daily) / (DOD_max * eta_bat * step_bat)) * step_bat

    # PV bounds
    Ppv_min = round((E_daily / (PSH * eta_pv * step_pv))) * step_pv
    Ppv_max = round((2.75* E_daily / (PSH * eta_pv * step_pv))) * step_pv

    print(f"E_daily: {E_daily:.2f} Wh")
    print(f"PSH: {PSH:.2f} h")
    #print(f"Cbat_min = {Cbat_min}, Cbat_max = {Cbat_max}")
    #print(f"Ppv_min = {Ppv_min}, Ppv_max = {Ppv_max}")
    
    return Cbat_min, Cbat_max, Ppv_min, Ppv_max

# Dummy stand-in fitness function until user provides actual LOLP and cost model

def addLoad(tables, year, Location):
    
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=Location.longitude, lat=Location.latitude)
    # Define date ranges for each season (India-style)
    season_ranges = [
        (datetime(year, 1, 1), datetime(year, 2, 28)),   # Winter
        (datetime(year, 3, 1), datetime(year, 5, 31)),   # Spring
        (datetime(year, 6, 1), datetime(year, 9, 30)),   # Monsoon
        (datetime(year, 10, 1), datetime(year, 12, 31))  # Summer
    ]

    # Create full datetime index for the year (30-minute intervals)
    full_index = pd.date_range(start=datetime(year, 1, 1),
                               end=datetime(year, 12, 31, 23, 00),
                               freq="30min",
                               tz=pytz.timezone(tz))
    
    total_power = pd.Series(0, index=full_index)

    for table_idx, (df, (start_date, end_date)) in enumerate(zip(tables, season_ranges)):
        date = start_date
        while date <= end_date:
            for _, row in df.iterrows():
                try:
                    power = float(row["Power [W]"])
                    from_time = datetime.strptime(row["From [xx:xx XM]"].strip(), "%I:%M %p").time()
                    to_time   = datetime.strptime(row["To [xx:xx XM]"].strip(), "%I:%M %p").time()

                    # Combine date with times, and localize to timezone
                    start_dt = datetime.combine(date, from_time)
                    end_dt   = datetime.combine(date, to_time)
                    if end_dt <= start_dt:
                        end_dt += timedelta(days=1)

                    start_dt = pytz.timezone(tz).localize(start_dt)
                    end_dt   = pytz.timezone(tz).localize(end_dt)

                    # Get 30min intervals between start and end
                    ts_range = pd.date_range(start=start_dt, end=end_dt - timedelta(seconds=1), freq="30min", tz=pytz.timezone(tz))

                    total_power.loc[ts_range] += power

                except Exception as e:
                    print(f"Skipping row due to error: {e}")
            date += timedelta(days=1)

    df_power = total_power.to_frame(name="Load Power")

    return Load("My Load", df_power)

def findMaxSyst(df, Location, pv_eff,  cleaning_freq, rain_thresh, eta_cable, step_pv=25, step_bat=100):
    _, guess_bat, _, guess_pv= SearchSpace(df)
    min_found = None
    for scale in np.linspace(1.0, 2.5, 400):  # Tune range if needed
        P_pv = int(scale * guess_pv // step_pv) * step_pv
        C_bat = int(scale * guess_bat // step_bat) * step_bat

        panel = Panels(power=P_pv, eta_tot= pv_eff, clean_freq=cleaning_freq, rainthresh = rain_thresh)
        pcu = PCU(eta_cable = eta_cable)
        mybat = BatteryFast(C_nom=C_bat / 12, SOC_min=0.2, Soc_init=0.5)
        df_fast = compute_power_fast(df, panel, Location)
        _, _, ENS_ratio = ENS_calc_fast(df_fast, pcu, mybat)
        print(f"Trying P_pv = {P_pv}, C_bat = {C_bat} → ENS = {ENS_ratio}")

        if ENS_ratio < 0.005:
            min_found = (P_pv, C_bat)
            break

    if not min_found:
        raise ValueError("No 0-ENS system found in range")

    # Optional: refine by greedy shrinking
    while True:
        test_P = min_found[0] - step_pv
        test_C = min_found[1] - step_bat
        pcu = PCU()
        panel = Panels(power=test_P, eta_tot=pv_eff, clean_freq=cleaning_freq, rainthresh = rain_thresh)
        mybat = BatteryFast(C_nom=test_C / 12, SOC_min=0.2, Soc_init=0.5)
        df_fast = compute_power_fast(df, panel, Location)
        _, _, ENS_ratio = ENS_calc_fast(df_fast, pcu, mybat)

        if ENS_ratio > 0.005:
            break
        min_found = (test_P, test_C)

    return min_found

# Define the NSGA-II problem
class SolarParetoProblem(Problem):

    def __init__(self, df, location, price_max, step_pv, step_bat, pv_bounds, bat_bounds, eta_tot, cleaning_freq, rain_thresh, price_W_pv=31, price_Wh_bat=15):
        self.df = df
        self.location = location
        self.step_pv = step_pv
        self.step_bat = step_bat
        self.price_W_pv = price_W_pv
        self.price_Wh_bat = price_Wh_bat
        self.pv_bounds = pv_bounds
        self.bat_bounds = bat_bounds
        self.price_max = price_max
        self.eta_tot = eta_tot
        self.rain_thresh = rain_thresh
        self.clean_freq = cleaning_freq

        super().__init__(
            n_var=2,
            n_obj=2,
            n_constr=0,
            xl=np.array([pv_bounds[0], bat_bounds[0]]),
            xu=np.array([pv_bounds[1], bat_bounds[1]]),
            type_var=np.int64
        )

    def _evaluate(self, X, out, *args, **kwargs):
        f1 = []  # ENS
        f2 = []  # Cost

        for P_pv, C_bat in X:
            P_pv = max(self.step_pv, int(P_pv // self.step_pv) * self.step_pv)
            C_bat = max(self.step_bat, int(C_bat // self.step_bat) * self.step_bat)

            panel = Panels(power=P_pv, eta_tot = self.eta_tot, clean_freq=self.clean_freq, rainthresh=self.rain_thresh)
            pcu = PCU()
            battery = BatteryFast(C_nom=C_bat / 12, SOC_min=0.2, Soc_init=0.5)

            df_fast = compute_power_fast(self.df, panel, self.location)
            _, _, ENS_ratio = ENS_calc_fast(df_fast, pcu, battery)
            cost = (P_pv * self.price_W_pv + C_bat * self.price_Wh_bat + inverter_price(self.df["Load Power"].max()*1.2))/self.price_max

            f1.append(ENS_ratio)
            f2.append(cost)

        out["F"] = np.column_stack([f1, f2])

# Define and run the optimizer
def run_nsga2_pareto(df, location, price_max, pv_bounds, bat_bounds, 
                     eta_tot, cleaning_freq, rain_thresh,  price_W_pv, price_Wh_bat, step_pv=25, step_bat=100, 
                     pop_size=100, n_gen=15, progress_callback=None):
    
    problem = SolarParetoProblem(df, location, price_max, step_pv, step_bat, 
                                 pv_bounds, bat_bounds, eta_tot, cleaning_freq, rain_thresh, price_W_pv = price_W_pv, price_Wh_bat = price_Wh_bat)

    algorithm = NSGA2(
        pop_size=pop_size,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    termination = get_termination("n_gen", n_gen)

    def my_progress_callback(algorithm):
        current_gen = algorithm.n_gen
        progress = int(40 + current_gen*4)
        if progress_callback:
            progress_callback(progress)

    res = minimize(
        problem,
        algorithm,
        termination,
        seed=1,
        save_history=True,
        verbose=True,
        callback=my_progress_callback
    )

    pareto_df = pd.DataFrame(res.X, columns=["P_pv", "C_bat"])
    pareto_df["ENS"] = res.F[:, 0]
    pareto_df["Cost"] = res.F[:, 1]

    return pareto_df

def inverter_price(load_w):
    ##Fitted power load price of PCU/Load capacity
    return 299.82 * load_w**0.635

def charge_current(load_max, V_pack_nom):
    charge_current = (0.97 * load_max + 5.67) / V_pack_nom
    return charge_current

def optimizer(longitude, latitude, tabs, price_W_pv, price_Wh_bat, eta_tot, 
              cleaning_freq, rain_thresh, eta_cable, progress_callback, eta_load, df_solar = None):
    #Define year
    year = 2018
    #Define location
    loc = Location(longitude, latitude)
    #Modify the load
    myload = addLoad(tabs,year,loc)
    #Fetch the dataframe and concad with load
    df = fetch_dataFrame(loc, 2018, df_solar, progress_callback)
    df = compute_ghi(df)
    #Merge the load and add load efficiency
    df = pd.concat([df, myload.df], axis=1)
    df["Load Power"] = df["Load Power"] / (eta_load / 100)
    max_load = df["Load Power"].max() * 1.2 #Added 20% of extra PCU capacity margin
    #Fetch the smallest system with ENS = 0
    Ppv_max, Cbat_max = findMaxSyst(df, loc, eta_tot, cleaning_freq, rain_thresh, eta_cable)
    price_max = price_W_pv * Ppv_max + price_Wh_bat* Cbat_max + inverter_price(max_load)
    progress_callback(40)
    #Run the Optimization and get a dataframe
    pareto_points = run_nsga2_pareto(df, loc, price_max,(0.1*Ppv_max, Ppv_max), (Cbat_max*0.1, Cbat_max), eta_tot, 
                                     cleaning_freq, rain_thresh, price_W_pv, price_Wh_bat, step_pv=25, 
                                     step_bat=100, progress_callback = progress_callback)
    pareto_points = pd.DataFrame(pareto_points, columns=["P_pv", "C_bat", "ENS", "Cost"])

    return pareto_points

def repeat_df(df, num_years, freq="30min"):
    """
    Repeat a time-indexed DataFrame for a given number of years, filling missing timestamps.

    """
    dfs = []
    for year in range(num_years):
        offset = pd.DateOffset(years=year)
        df_offset = df.copy()
        df_offset.index = df.index + offset
        dfs.append(df_offset)

    df_repeated = pd.concat(dfs)
    full_index = pd.date_range(
        start=df_repeated.index.min(),
        end=df_repeated.index.max(),
        freq=freq
    )
    df_repeated = df_repeated.reindex(full_index)
    df_repeated.interpolate(method="time", inplace=True)

    print(df_repeated.head())
    print(df_repeated.tail(100))

    return df_repeated

def batteryAging(df, PCU, Battery, design_year = 15):
    #Find the df of the battery over designed years
    df = repeat_df(df, design_year)
    bat_df,_ ,_ = ENS_calc_slow(df, PCU, Battery)

    #Find the expected life of the battery
    threshold = 0.8
    threshold_indices = bat_df.index[bat_df["Battery Left"] < threshold]

    if len(threshold_indices) > 0:
        first_index = threshold_indices[0]
        time_elapsed_hours = (first_index - bat_df.index[0]).total_seconds() / 3600
        expected_time = str(round(time_elapsed_hours / (24 * 365),1))
    else:
        expected_time = f'+{design_year}'


    return  bat_df[["Cycle", "Battery SOH"]], expected_time


def verifier(longitude, latitude, tabs, power, area, 
            bat_capa, bat_lifetime, bat_cycle, bat_height, bat_series, 
            bat_mass, bat_para, pv_num, soc_min, pcu_charge, pcu_inv, alpha, cleaningfreq,
            rainthresh, eta_tot, pcu_current, eta_cable, progress_callback, eta_load, df_solar = None):
    
    # -- Define useful instances ---
    year = 2018
    
    loc = Location(longitude, latitude)

    mybat = Battery(C_nom = bat_capa, SOC_min = soc_min/100, 
                    Mass = bat_mass, Bat_height = bat_height, 
                    Lifetime = bat_lifetime, Ziec = bat_cycle, 
                    Soc_init = 0.5, n_para = bat_para, 
                    n_serie = bat_series)
    
    pcu = PCU(eta_cable = eta_cable, max_charge_current = pcu_current, 
              pack_voltage = 12*bat_series, eta_inverter = pcu_inv/100, 
              eta_CC = pcu_charge/100)
    
    mypv = Panels(power = power, eta_tot = eta_tot, 
                  name=None, alpha=alpha/100, 
                  area=area, string_num=pv_num, 
                  string_dist=1, clean_freq = cleaningfreq, 
                  rainthresh = rainthresh)
    
    # -- Fetch ENS and LOLP
    myload = addLoad(tabs,year,loc)
    df = fetch_dataFrame(loc, 2018, df_solar, progress_callback)
    df = pd.concat([df, myload.df], axis=1)
    df["Load Power"] = df["Load Power"] / (eta_load / 100)
    df = compute_power_slow(df, mypv, loc)
    progress_callback(52)
    df, LOLP_ratio, ENS_ratio = ENS_calc_slow(df, pcu, mybat)
    progress_callback(64)
    
    # -- Fetch battery aging information
    pcu_aging = PCU(eta_cable = eta_cable, max_charge_current=pcu_current, 
                    pack_voltage = 12*bat_series, eta_inverter = pcu_inv/100, 
                    eta_CC = pcu_charge/100)
    
    mybat_aging = Battery(C_nom = bat_capa, SOC_min = soc_min/100, 
                          Mass = bat_mass, Bat_height = bat_height, 
                          Lifetime = bat_lifetime, Ziec = bat_cycle, 
                          Soc_init = 0.5, n_para = bat_para, 
                          n_serie = bat_series)
    
    bat_df, expected_time = batteryAging(df, pcu_aging, mybat_aging)
    progress_callback(93)
    print(f"Source verifier computed ENS is {ENS_ratio}")
    return df, LOLP_ratio, ENS_ratio, bat_df, expected_time




'''loc = Location(latitude = 23.49, longitude = 93.34)
panel_slow = Panels(name="Panneau123", power=4400, alpha=-0.29/100, area =1.039 * 2.047, string_num=4, string_dist=1, price=1000)
mybat_slow = Battery(C_nom = 500, SOC_min = 0.2 , Mass = 30.2 , Bat_height = 0.216, Lifetime = 20, Ziec = 1500, Soc_init=0.5, n_para = 3, n_serie = 1)
mypcu_slow = PCU("company", "model", 5000, "MPPT", 1, 48, 0.92, 0.88)
df = pd.DataFrame(index=pd.date_range("2018-01-01 00:00", "2018-12-31 23:00", freq="30min", tz="Asia/Kolkata"))
df["Load Power"] = df.index.to_series().apply(lambda ts: 1500 if 3 <= ts.hour < 10 else 0)
myload = Load("Load", df)
df = fetch_dataFrame(loc, 2018, progress_callback)
print("Done fetching")
df = pd.concat([df, myload.df], axis=1)
df = compute_power_slow(df, panel_slow, loc)
print("Done computing power")
#df, LOLP, ENS = ENS_calc_slow(df, mypcu_slow, mybat_slow)
design_year = 5
print('Done with ENS')
#mybat_slow2 = Battery(C_nom = 100, SOC_min = 0.2 , Mass = 30.2 , Bat_height = 0.216, Lifetime = 20, Ziec = 1500, Soc_init=0.5, n_para = 3, n_serie = 1)
#mypcu_slow2 = PCU("company", "model", 5000, "MPPT", 1, 48, 0.92, 0.88)
bat_df, expected_time = batteryAging(df, design_year, mypcu_slow, mybat_slow)
#print(LOLP, ENS)
print(expected_time)


    # Create the figure
fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot cycle count
ax1.plot(bat_df.index, bat_df["Cycle"], label="State of Health", color='blue')
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Number of Cycles", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, which='both', linestyle='--', alpha=0.7)
ax1.axhline(y=0.8, color='red', linestyle='--', linewidth=2)

    # Titles and legend
plt.title(f"Battery Aging Over {design_year} Years")
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
plt.tight_layout()
plt.show()'''
#Ppv_max, Cbat_max = findMaxSyst(df, loc)
#price_W_pv=31; price_Wh_bat=15
#price_max = price_W_pv * Ppv_max + price_Wh_bat* Cbat_max

#samples = biased_sample_systems(n_samples, Ppv_bounds=(50, Ppv_max), Cbat_bounds=(100, Cbat_max))
#evaluated = evaluate_systems(samples, df, loc, price_max, price_W_pv, price_Wh_bat)
#pareto_points = pareto_front(evaluated)
#pareto_points = run_nsga2_pareto(df, loc, price_max,(0.1*Ppv_max, Ppv_max), (Cbat_max*0.1, Cbat_max), step_pv=50, step_bat=200)
#pareto_points = pd.DataFrame(pareto_points, columns=["P_pv", "C_bat", "ENS", "Cost"])
#print(pareto_points)
'''
def progress_callback(val):
    return

loc = Location(latitude = 23.49, longitude = 93.34)
panel_slow = Panels(name="Panneau123", power=440, alpha=-0.29/100, area =1.039 * 2.047, string_num=4, string_dist=1, price=1000)
mybat_slow = Battery(C_nom = 100, SOC_min = 0.2 , Mass = 30.2 , Bat_height = 0.216, Lifetime = 20, Ziec = 1500, V_nom = 12, Soc_init=0.5)
mypcu_slow = PCU("company", "model", 5000, "MPPT", 1, 48, 0.92, 0.88)

#mybat_fast = BatteryFast(C_nom = 100, SOC_min = 0.2, Soc_init=0.5)
#panel_fast = Panels(power=440)
#mypcu_fast = PCU()
#mode = SystemMode.FULL_RELIABILITY

df_1 = pd.DataFrame(index=pd.date_range("2018-01-01 00:00", "2018-01-01 23:00", freq="30min", tz="Asia/Kolkata"))
df_1["Load Power"] = df_1.index.to_series().apply(lambda ts: 1000 if 6 <= ts.hour < 10 else 0)
myload = Load("Load", df_1)
df = fetch_dataFrame(loc, 2018, progress_callback)
df = pd.concat([df, myload.df], axis=1)
df = compute_power_slow(df,panel_slow, loc)
df, LOLP, ENS = ENS_calc_slow(df, mypcu_slow, mybat_slow)
print(print(list(df.columns)))
print(f"The LOLP is given as {LOLP} and the ens as {ENS}")

'''
#df_results = SolarPareto(myload, loc, 2018, mode)
# Get cost and ENS columns
#pareto_points = pareto_front(df_results)

'''import plotly.express as px
import pandas as pd
import plotly.io as pio

pio.renderers.default = "vscode" 

# Ensure no SettingWithCopyWarning
pareto_points = pareto_points.copy()

# Create hover text column
pareto_points["System Details"] = pareto_points.apply(
    lambda row: f"P_pv: {int(row.P_pv)} W<br>C_bat: {int(row.C_bat)} Wh", axis=1
)


# Create Plotly scatter plot
fig = px.scatter(pareto_points, x="ENS", y="Cost")


# Optional: zoom in on ENS axis
fig.update_layout(
    xaxis=dict(range=[0, 0.15]),
    template="simple_white"
)

# If you're in VS Code script, force open in browser
fig.show()'''

'''

df= fetch_dataFrame(loc, 2018)
df = addLoad(df, myload)
df_fast = compute_power_fast(df, panel_fast, loc)
df_slow = compute_power_slow(df, panel_slow, loc)

import pandas as pd
import matplotlib.pyplot as plt

# Ensure the indices align (especially if time-indexed)
df_fast = df_fast.sort_index()
df_slow = df_slow.sort_index()

# Create a new DataFrame to store comparison
comparison_df = pd.DataFrame({
    "Power Fast": df_fast["Output Power"],
    "Power Slow": df_slow["Output Power"]
})

# Compute difference and relative error
comparison_df["Absolute Difference (W)"] = comparison_df["Power Fast"] - comparison_df["Power Slow"]
comparison_df["Relative Difference (%)"] = 100 * comparison_df["Absolute Difference (W)"] / comparison_df["Power Slow"].replace(0, 1e-6)  # avoid division by zero

# Plotting
plt.figure(figsize=(12, 5))
plt.plot(comparison_df.index, comparison_df["Power Fast"], label="Power Fast", alpha=0.7)
plt.plot(comparison_df.index, comparison_df["Power Slow"], label="Power Slow", alpha=0.7)
plt.title("Comparison of Output Power")
plt.xlabel("Time")
plt.ylabel("Output Power (W)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot difference
plt.figure(figsize=(12, 4))
plt.plot(comparison_df.index, comparison_df["Absolute Difference (W)"], label="Absolute Difference", color='red')
plt.title("Absolute Difference in Output Power (Fast - Slow)")
plt.xlabel("Time")
plt.ylabel("Power Difference (W)")
plt.grid(True)
plt.tight_layout()
plt.show()

df_fast, LOLP_fast, ENS_fast = ENS_calc_fast(df_fast, mypcu_fast, mybat_fast)
df_slow, LOLP_slow, ENS_slow = ENS_calc_slow(df_slow, mypcu_slow, mybat_slow)

print("\n--- ENS and LOLP Comparison ---")
print(f"{'Metric':<10} | {'Fast Model':>12} | {'Slow Model':>12} | {'Difference':>12}")
print("-" * 50)
print(f"{'LOLP':<10} | {LOLP_fast:12.4%} | {LOLP_slow:12.4%} | {(LOLP_slow - LOLP_fast):12.4%}")
print(f"{'ENS':<10} | {ENS_fast:12.4%} | {ENS_slow:12.4%} | {(ENS_slow - ENS_fast):12.4%}")


'''
#df_fast, LOLP_fast, ENS_fast = ENS_calc_fast(df_fast, myload, mypcu, mybat_fast)
#df_slow, LOLP_slow, ENS_slow = ENS_calc_slow(df_slow, myload, mypcu, mybat_slow)
'''



loc = Location(latitude = 23.49, longitude = 93.34)
panel = Panels(name="Panneau123", power=440, alpha=-0.29/100, area =1.039 * 2.047, string_num=4, string_dist=1, price=1000)
mybat = Battery(C_nom = 100, DOD_min = 0.2 , Mass = 30.2 , Bat_height = 0.216, Lifetime = 20, Ziec = 1500, V_nom = 12, Soc_init=0.5)
mypcu = PCU("company", "model", 5000, "MPPT", 1, 48, 0.92, 0.88)
myload = Load("Load", load_pattern, "06:00 AM", "10:00 AM")
df = fetch_dataFrame(loc, 2018)
df = compute_power(df, panel, loc, 2018)

#loc = Location(latitude = 23.49, longitude = 93.34)
#panel = Panels(name="Panneau123", power=440, alpha=-0.29/100, area =1.039 * 2.047, string_num=4, string_dist=1, price=1000)
#mybat = Battery(C_nom = 100, DOD_min = 0.2 , Mass = 30.2 , Bat_height = 0.216, Lifetime = 20, Ziec = 1500, V_nom = 12, Soc_init=0.5)
#mypcu = PCU("company", "model", 5000, "MPPT", 1, 48, 0.92, 0.88)
#myload = Load("Load", 1000, "06:00 AM", "10:00 AM")
#df = fetch_dataFrame(loc, 2018)
#df = compute_power(df, panel, loc, 2018)
#lolp = LOLP_calculation(df['Output Power'],df['Temperature'], myload, mypcu, mybat)'''