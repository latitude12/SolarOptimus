import Pareto
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
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import Timestamp
from concurrent.futures import ThreadPoolExecutor
import time
 
### --- DEFINITION OF USEFUL CLASSES --- ###

class Panels:
    def __init__(self, power, eta_tot, name = None, alpha = None, string_num = 1, 
                 string_dist = None, clean_freq = 12, rainthresh = 7):
        
        self.name = name 
        self.eta_tot = eta_tot # Total efficiency of the panel between [0-1]
        self.power = power # Peak power [W]
        self.string_num = string_num # Number of strings parallel
        self.string_dist = string_dist # Distance between strings [m]
        self.clean_freq = f'{clean_freq}W' # Cleaning frequency in weeks
        self.rainthresh = rainthresh # Rainfall threshold for cleaning in [mm]
        self.area = self.power / (0.18 * 1000) # [m^2]

        if alpha is not None: # Temperature coefficient [1/K]
            self.alpha = alpha
        else:
            self.alpha = -33/10000 

class Load:
    def __init__(self, name, loadProfile):
        self.name = name
        self.loadProfile = loadProfile 

class Location:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class PCU:
    def __init__(self, eta_cable = 2, max_charge_current = None, capacity = None, 
                 pack_voltage = None, eta_CC = 0.93, eta_inverter = 0.87):
        
        self.capacity = capacity # Maximum power capacity to load [W]
        self.pack_voltage = pack_voltage # 12, 24, 48, 96, 120, 240 V of battery pack
        self.eta_pv_to_load = eta_CC ** 0.5 * eta_inverter * ((1 - eta_cable / 100) ** 2)# [0-1]
        self.eta_pv_to_batt = eta_CC * ((1 - eta_cable / 100) **2) # [0-1]
        self.eta_batt_to_load = eta_inverter * ((1 - eta_cable / 100) ** 2) # [0-1]
        self.max_charge_current = max_charge_current # in [A]

# --- GLOBAL CACHE ---

_last_fetch_args = {
    "longitude": None,
    "latitude": None,
    "df_result": None,
    "file_present": False, 
    "design_year": None
}

### --- DATA FETCHING --- ###

def change_timestamp(df, local_tz):
    """
    Input: 
    - df: pd.DataFrame, columns: Year, Month, Day, Hour, Minute, ...
    - local_tz: pytz timezone object
    Output: 
    - df: pd.DataFrame, time-zone sensitive timestamp
    Function:
    - Converts Year, Month, Day, Hour, Minute columns to a single datetime index
    """
    
    df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])
    df.set_index('datetime', inplace=True)
    df.index.name = None
    df.drop(columns = ['Year', 'Month', 'Hour', 'Minute', 'Day'], inplace=True)
    df.index = df.index.tz_localize(local_tz) 
    
    return df

def fetch_irradiation(Location, design_year, local_tz):
    """
    Input: 
    - Location: class object
    - design_year: int, number of years to consider for design
    - local_tz: pytz timezone object
    Output:
    - data_frame: pd.DataFrame, columns 'GHI', 'DHI', 'DNI', time-zone aware index
    Function:
    - Fetches solar irradiation data from the CAMS API for a given location and time range.
    """

    try:
        end_year = datetime.now().year
        start_year = max(2004, end_year - design_year)
        # Convert to strings in YYYY-MM-DD format
        start_date_str = f"{start_year}-01-01"
        end_date_str = f"{end_year-1}-12-31"

        # Fetch the dataframe at CAMS using PVLIB's iotools
        data_frame, _ = pvlib.iotools.get_cams(
                        Location.latitude, Location.longitude,
                        start_date_str, end_date_str,
                        email = 'bastien.gaussent@epfl.ch',
                        identifier='cams_radiation', time_step='1h', 
                        time_ref='TST', verbose=False, map_variables=True, 
                        url='api.soda-solardata.com', timeout=60)
        
    
        data_frame.drop(columns=['Observation period', 'ghi_extra', 'ghi_clear', 'bhi',
                                'bhi_clear', 'dhi_clear', 'dni_clear', 'Reliability'], inplace=True)
        
        data_frame.rename(columns={
                        'ghi': 'GHI',
                        'dhi': 'DHI',
                        'dni': 'DNI' }, inplace=True)

        data_frame.index = data_frame.index.tz_convert(None)
        data_frame.index = data_frame.index.tz_localize(local_tz)

        return data_frame
    
    except Exception as e:
        print(f"[ERROR] Rain API failed: {e}")
        return None  

def convert_UNIX(df, local_tz, year):
    """
    Input: 
    - df: pd.DataFrame, index UNIX timestamps
    - local_tz: pytz timezone object
    - year: int, year to filter the data
    Output:
    - df: pd.DataFrame, with localized time-zone sensitive datetime index
    Function:
    -  Converts a DataFrame with UNIX timestamps to localized datetime format
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
    df = df.drop(columns = ['UNIX', 'timestamp'])
    df = change_timestamp(df, local_tz)
    df['timestamp'] = pd.to_datetime(df.index)

    ### Select only the wanted year
    df = df[df['timestamp'].dt.year == year]
    df = df.drop(columns = ['timestamp'])
      
    return df 

def get_UNIX_range(year, local_tz):
    """
    Input:
    - year: int, year for which to get the UNIX timestamps
    - local_tz: pytz timezone object
    Output:
    - start_utc_unix: int, UNIX timestamp for Jan 1, 00:00 in UTC
    - end_utc_unix: int, UNIX timestamp for Feb 28, 23:30 in UTC
    Function:
    - Returns UNIX UTC timestamps for Jan 1, 00:00 and Feb 28, 23:30 in *local time* 
      for a given zone. Returned times are in UTC as required by OpenWeather API.
    """

    # Create local datetime objects
    start_local = local_tz.localize(datetime(year, 1, 1, 0, 0))
    end_local = local_tz.localize(datetime(year+1, 1, 1, 23, 30))  # Note: not leap year

    # Convert to UTC, then to UNIX timestamp
    start_utc_unix = int(start_local.astimezone(pytz.utc).timestamp())
    end_utc_unix = int(end_local.astimezone(pytz.utc).timestamp())

    return start_utc_unix, end_utc_unix

def align_df(df, year, Location):
    """
    Input: 
    - df: pd.DataFrame, with timezone-aware DatetimeIndex
    - year: int, target year for alignment
    - Location: class object
    Output: 
    - matched_df: pd.DataFrame, reindexed to match hourly timestamps of the target year
    Function:
    - Align a DataFrame to a 1-hour datetime index for a given year and timezone.
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

def formatValidator(df, Location, design_year, local_tz):
    """
    Input: 
    - df: user input DataFrame with solar data
    - Location: class object
    - design_year: int, number of years to consider for design
    - local_tz: pytz timezone object
    Ouput: 
    - df: pd.DataFrame, with standardized timestamp and aligned to the target year
    Function: 
    - Prepares the user input solar data for concatenation with the other data. 
    """

    year = datetime.now().year -1
    df = change_timestamp(df, local_tz)
    df.index = df.index.map(lambda ts: ts.replace(year=year))
    df = align_df(df, year, Location)
    df = repeat_df(df, design_year, freq="1h")

    return df

def fetch_pollution(Location, design_year, local_tz):
    """
    Input: 
    - Location: class object
    - design_year: int, number of years to consider for design
    - local_tz: pytz timezone object
    Output:
    - df: pd.DataFrame, columns PM2.5, PM10, and local datetime index
    Function: 
    - Fetches hourly PM2.5 and PM10 air pollution data from OpenWeather's historical API
    """

    try:
        year = datetime.now().year - 1 
        api_key = 'fcc56e7d5838b4b21a971c7af302e544'
        start_unix, end_unix = get_UNIX_range(year, local_tz)
        
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

        df = convert_UNIX(df, local_tz, year)
        df = repeat_df(df, design_year, freq="1h")
        return df
    
    except Exception as e:
        print(f"[ERROR] Pollution API failed: {e}")
        return None  # safe fallback

def fetch_wheather_data(Location, design_year, local_tz):
    """
    Input:
    - Location: clas object
    - design_year: int, number of years to consider for design
    - local_tz: pytz timezone object
    Ouptut:
    - df: pd.DataFrame, with columns Rain, Temperature, Wind, and local datetime index
    Function:
    - Fetches hourly weather data (rain, temperature, wind) from NASA's POWER API
    """

    try:
        base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        end_year = datetime.now().year
        start_year = end_year - design_year
        # Convert to strings in YYYY-MM-DD format
        start_date_str = f"{start_year}0101"
        end_date_str = f"{end_year-1}1231"
        parameters ="PRECTOTCORR,T2M,WS10M"
        community = "RE"

        url = f"{base_url}?latitude={Location.latitude}&longitude={Location.longitude}&start={start_date_str}&end={end_date_str}&parameters={parameters}&community={community}&format=CSV"
        
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
                        'T2M': 'Temperature',
                        'WS10M': 'Wind',               
                        'MO': 'Month',
                        'YEAR': 'Year',
                        'DY': 'Day',
                        'HR': 'Hour'}, inplace=True)
        
        data_cl['Minute'] = 0
        df = change_timestamp(data_cl, local_tz)

        return df
    
    except Exception as e:
        print(f"[ERROR] Weather API failed: {e}")
        return None

def solarPositions(df, Location):
    """
    Input:
    - df: pd.DataFrame with timezone-aware datetime index
    - Location: class object
    Output:
    - df: pd.DataFrame with 'Solar Zenith' and 'Solar Azimuth' columns added
    Function:
    - Adds solar zenith and azimuth angles to the DataFrame using pvlib's solar position calculations.
    """

    df = df.copy()

    # Compute altitude (elevation above sea level)
    alt = pvlib.location.lookup_altitude(Location.latitude, Location.longitude)

    # --- Solar position calculation ---
    solar_pos = pvlib.solarposition.get_solarposition(
        df.index, 
        Location.latitude, 
        Location.longitude, 
        altitude=alt
    )

    # Add columns to DataFrame
    df["Solar Zenith"] = solar_pos["apparent_zenith"].values
    df["Solar Azimuth"] = solar_pos["azimuth"].values

    return df

def fetch_dataFrame(Location, design_year, df_solar, progress_callback):
    """
    Input:
    - Location: class object with longitude and latitude
    - design_year: int, number of years to consider for design
    - df_solar: pd.DataFrame, optional user-provided solar data
    - progress_callback: function to update progress bar in UI
    Output: 
    - df_last: pd.DataFrame, columns 'GHI', 'DHI', 'DNI', 'PM2.5', 'PM10', 'Rain', 
                                     'Temperature', 'Wind', 'Solar Zenith', 'Solar Azimuth'
    Function:
    - Acquires the data from  APIs, combined them into one dataframe and resamples them for a granularity of 30min
    """

    global _last_fetch_args

    # --- Check if the data is already cached ---
    if (_last_fetch_args["longitude"] == Location.longitude and
        _last_fetch_args["latitude"] == Location.latitude and
        _last_fetch_args["design_year"] == design_year and
        _last_fetch_args["file_present"] == (df_solar is not None) and  
        _last_fetch_args["df_result"] is not None):
        print("Reusing cached solar/weather dataframe")
        progress_callback(35)
        return _last_fetch_args["df_result"]

    # --- Otherwise fetch new data ---
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=Location.latitude, lng=Location.longitude)
    local_tz = pytz.timezone(tz_str)

    if df_solar is None:
        print("Using API solar data")
        _last_fetch_args["file_present"] = False
        with ThreadPoolExecutor(max_workers=3) as executor:
            fut_irr = executor.submit(fetch_irradiation, Location, design_year, local_tz)
            fut_pol = executor.submit(fetch_pollution, Location, design_year, local_tz)
            fut_rain = executor.submit(fetch_wheather_data, Location, design_year, local_tz)
            df_irr = fut_irr.result()
            df_pol = fut_pol.result()
            df_rain = fut_rain.result()

    else:
        print("Using user input solar data")
        _last_fetch_args["file_present"] = True
        df_irr = formatValidator(df_solar, Location, design_year, local_tz)
        with ThreadPoolExecutor(max_workers=2) as executor:
            fut_pol = executor.submit(fetch_pollution, Location, design_year, local_tz)
            fut_rain = executor.submit(fetch_wheather_data, Location, design_year, local_tz)
            df_pol = fut_pol.result()
            df_rain = fut_rain.result()
        
    progress_callback(11)

    if df_irr is None or df_pol is None or df_rain is None:
        print("Error fetching data from APIs. Please check your internet connection or API keys.")
        return "API Error: try again"
    
    progress_callback(23)
    
    # --- Data cleaning and preparation ---
    df_combined = pd.concat([df_irr, df_pol, df_rain], axis=1)
    df_fin = df_combined.resample('30min').mean()
    df_fin = df_fin.interpolate(method='linear', limit_direction='both')
    progress_callback(29)
    df_last = solarPositions(df_fin, Location) #Acquires solar positions and zenith
    df_last.interpolate(method="linear", limit_direction="both", inplace=True)
    df_last.ffill(inplace=True)  # forward fill
    df_last.bfill(inplace=True)  # backward fill
    progress_callback(35)

    # --- Update the global cache ---
    _last_fetch_args = {
        "longitude": Location.longitude,
        "latitude": Location.latitude,
        "design_year": design_year,
        "df_result": df_last,
        "file_present": df_solar is not None,
        "design_year": design_year
    }
    
    return  df_last

### --- DATA COMPLETION --- ###

def PV_params(Panels, Location):
    """
    Input:
    - Panels: class object
    - Location: class object
    Output: 
    - GCR: float, Ground Coverage Ratio
    - R_dist: float, distance between rows 
    """
 
    PV_Length = math.sqrt(Panels.area / 1.65)
    R_dist = Panels.string_dist + np.cos(np.radians(abs(Location.latitude))) * PV_Length
    GCR = PV_Length / R_dist
    
    return GCR, R_dist

def diff_shadow(df, Panels, Location):
    """
    Input:
    - df: pd.DataFrame with columns 'DHI'...
    - Panels: class object
    - Location: class object
    Output: 
    - df: pd.DataFrame with adjusted 'DHI' column
    Function: 
    - Adjusts the Diffuse Horizontal Irradiance (DHI) in df for 
      diffuse shading losses caused by row-to-row shadowing. Model based on PVLib
    """

    GCR, _ = PV_params(Panels, Location)
   
    # --- Diffuse Irradiance Loss caused by row to row sky diffuse shading --- 
    psi = shading.masking_angle_passias(abs(Location.latitude), GCR) 
    shading_loss = shading.sky_diffuse_passias(psi)
    
    adjusted_power = df['DHI'] * (1 + (1 - shading_loss) * (Panels.string_num - 1)) / Panels.string_num
    df['DHI'] = adjusted_power if Panels.string_num > 1 else df['DHI']
    
    return df

def direct_shadow(df, Panels, Location):
    """
    Input:
    - df: pd.DataFrame with columns 'DNI', 'Solar Zenith', 'Solar Azimuth'...
    - Panels: class object
    - Location: class object
    Output: 
    - df: pd.DataFrame with adjusted 'DNI' column
    Function: 
    - Applies a correction to Direct Normal Irradiance (DNI) in df for row-to-row shading losses 
      caused by direct irradiance blocking in multi-row PV systems. Model based on PVLib
    """

    PV_Length = math.sqrt(Panels.area / 1.65)
    GCR, R_dist = PV_params(Panels, Location)

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

    adjusted_power = df['DNI'] * (1 + (1 - shaded_fraction_PV) * (Panels.string_num - 1)) / Panels.string_num
    df['DNI'] = adjusted_power if Panels.string_num > 1 else df['DNI']

    return df

def horizon_shading(df, Location):
    """
    Input: 
    - df: pd.DataFrame with columns 'DNI', 'Solar Zenith', 'Solar Azimuth'...
    - Location: class object
    Output:
    - df: pd.DataFrame with adjusted 'DNI' column
    Function: 
    - Adjusts the Direct Normal Irradiance (DNI) in df for shading caused by the local horizon
      Model based on PVLib
    """

    horizon_profile, _ = pvlib.iotools.get_pvgis_horizon(Location.latitude, Location.longitude)
    horizon_elevation_data = np.interp(df["Solar Azimuth"], horizon_profile.index, horizon_profile)
    horizon_elevation_data = pd.Series(horizon_elevation_data, df.index)
    
    df['DNI'] = np.where(df["Solar Zenith"] > horizon_elevation_data, df['DNI'], 0)
    
    return df

def soiling_effect(df, Location, Panels):
    """
    Input: 
    - df: pd.DataFrame with columns 'Rain', 'PM2.5', 'PM10'...
    - Location: class object
    - Panels: class object
    Output:
    - df: pd.DataFrame with 'Soiling ratio' column added
    Function:
    - Applies the HSU soiling loss model to estimate the impact of particulate matter
      (PM2.5 and PM10) and rainfall on solar panel performance over time.
    """

    cleaning_threshold = Panels.rainthresh
    cleaning_interval = Panels.clean_freq

    # --- Define useful data structures --- 
    depo_veloc = {'2_5': 0.0009, '10': 0.004} # Default values from [1] (m/s)
    rain_accum_period = pd.Timedelta('30min') 
       
    rainfall = df['Rain'].fillna(0)
    pm2_5 = df['PM2.5'] * 10e-6 #PM need be in g/m3
    pm10 = df['PM10'] * 10e-6 

    # --- Preparation of manual cleaning breakpoints --- 
    start_date = rainfall.index.min()
    end_date = rainfall.index.max()

    cleaning_dates = pd.date_range(start=start_date, end=end_date, freq=cleaning_interval, tz=df.index.tz)
    cleaning_dates = cleaning_dates.insert(0, start_date) 
    cleaning_dates = cleaning_dates.drop_duplicates(keep='first')
    
    if cleaning_dates[-1] < end_date:
        cleaning_dates = cleaning_dates.append(pd.DatetimeIndex([end_date]))

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
    Input: 
    - df: pd.DataFrame with columns 'DHI', 'DNI', 'Solar Zenith'
    Output:
    - df: pd.DataFrame with 'GHI' column added
    """
        
    df['GHI'] = df['DHI'] + np.cos(np.radians(df["Solar Zenith"].values))*df['DNI']

    return df

def fetch_POA(df, Location):
    """
    Input: 
    - df: pd.DataFrame with columns 'DNI', 'DHI', 'GHI', 'Solar Zenith', 'Solar Azimuth'
    - Location: class object
    Output:
    - df: pd.DataFrame with 'POA' column added
    Function: 
    - Computes the Plane of Array (POA) irradiance using the total irradiance model from pvlib.
      The resulting POA irradiance is added to the DataFrame as a new column.
    """

    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=abs(Location.latitude),
        surface_azimuth=180,
        dni=df['DNI'].values,
        ghi=df['GHI'].values,
        dhi=df['DHI'].values,
        solar_zenith=df["Solar Zenith"].values,
        solar_azimuth=df["Solar Azimuth"].values
    )

    df['POA'] = POA_irradiance['poa_global']
    return df

def cell_temp(df):
    """
    Input: 
    - df: pd.DataFrame with columns 'POA', 'Temperature', 'Wind'
    Output: 
    - df: pd.DataFrame with 'Cell Temperature' column added
    Function: 
    - Estimates the PV cell temperature using the PVsyst model and default coefficients 
      for land-based systems. The resulting temperature is added to the DataFrame.
    """
    
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
    """
    Input: 
    - df: pd.DataFrame with columns 'POA', 'Cell Temperature', 'Soiling ratio'
    - Panels: class object
    Output:
    - df: pd.DataFrame with 'Output Power' column added
    Function:
    - Computes the DC output power of the PV system using the PVWatts DC model from pvlib.
      Takes in account a fixed PV losses and soiling ratio
    """    

    #ASSUMED FIXED # to review
    #Takes into account shading from neighboring elements, PV mismatch, Nameplate rating and Light Induced degradation
    df['Output Power'] = pvlib.pvsystem.pvwatts_dc(df['POA'], df['Cell Temperature'], Panels.power * Panels.string_num, Panels.alpha) * Panels.eta_tot * df['Soiling ratio']

    return df

def compute_power_slow(df, Panels, Location):
    """
    Input: 
    - df: pd.DataFrame with columns 'DNI', 'DHI', 'GHI', 'Solar Zenith', 'Solar Azimuth', 'Temperature', 'Wind'
    - Panels: class object
    - Location: class object
    Output:
    - df: pd.DataFrame with 'Output Power' column added
    Function:
    - Computes the DC output power of the PV system using a step-by-step simulation. Slow but accurate
    """

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
    """
    Input: 
    - df: pd.DataFrame with columns 'DNI', 'DHI', 'GHI', 'Solar Zenith', 'Solar Azimuth', 'Temperature', 'Wind'
    - Panels: class object
    - Location: class object
    Output:
    - df: pd.DataFrame with 'Output Power' column added
    Function:
    - Computes the DC output power of the PV system using a step-by-step simulation. Fast but less accurate
    """

    df = soiling_effect(df, Location, Panels)
    
    df = compute_ghi(df)

    df = fetch_POA(df, Location)

    df = cell_temp(df)

    df = fetch_power(df, Panels)

    return df

def ENS_calc_slow(df, PCU, Battery):
    """
    Input: 
    - df: pd.DataFrame with columns 'Output Power', 'Load Power', 'Temperature' ...
    - PCU: class object
    - Battery: class object
    Output:
    - df: pd.DataFrame with 'Battery Left', 'Battery SOC', 'Cycle', 'Battery SOH' columns added
    - ENS_ratio: float, Energy Not Supplied ratio
    Function: 
    - Simulates the energy flows in the system including battery dynamics. Computes the ENS.
    - Uses a detailed battery model for accurate simulation.
    """
    dt = 0.5 # time interval: 30min = 0.5h

    # --- Compute the power entering/leaving the battery ---
    PV_to_load = df["Output Power"] * PCU.eta_pv_to_load
    power_diff = PV_to_load - df["Load Power"]
    charge_cond = power_diff >= 0
    charge_power = (df["Output Power"] - df["Load Power"]/PCU.eta_pv_to_load) * PCU.eta_pv_to_batt
    discharge_power = (df["Load Power"] - PV_to_load) / PCU.eta_batt_to_load
    df["Battery Power"] = np.where(charge_cond, charge_power, -discharge_power)

    # --- Initialize battery model and variables ---
    ENS_count = 0.
    n = len(df)
    battery_left = np.zeros(n)
    battery_soc = np.zeros(n)
    battery_cycle = np.zeros(n)
    battery_soh = np.zeros(n)
    cell_volt = np.zeros(n)
    model = BatteryModel(Battery)
    
    # Convert to NumPy for speed
    load_power = df["Load Power"].values
    output_power = df["Output Power"].values
    battery_power = df["Battery Power"].values
    temperature = df["Temperature"].values

    battery_left[0], battery_soc[0], battery_cycle[0], battery_soh[0], cell_volt[0] = model.getInfo()

    for i in range(len(df) -1 ):
        
        #Model maximum charge controller current
        V_pack = cell_volt[i] * Battery.n_series
        I_charging = battery_power[i] / V_pack

        if I_charging > PCU.max_charge_current and battery_power[i] > 0:
            battery_power[i] = PCU.max_charge_current * V_pack #Clipped to max current

        #Run battery model
        model.RunModel(temperature[i], battery_power[i])
        battery_left[i + 1], battery_soc[i + 1], battery_cycle[i+1], battery_soh[i+1], cell_volt[i+1] = model.getInfo()

        ENS_count += max(0,load_power[i] * dt - output_power[i] * PCU.eta_pv_to_load * dt - PCU.eta_batt_to_load * (max(0,battery_left[i] - battery_left[i+1])))
    
    ENS_ratio = ENS_count/ (df["Load Power"].sum()*dt) # *dt: conversion W -> Wh

    df["Battery Left"] = battery_left
    df["Battery SOC"] = battery_soc
    df["Cycle"] = battery_cycle
    df["Battery SOH"] = battery_soh

    return df, ENS_ratio
 
 # MARK

def ENS_calc_fast(df, PCU, BatteryFast):
    """
    Input: 
    - df: pd.DataFrame with columns 'Output Power', 'Load Power', 'Temperature' ...
    - PCU: class object
    - BatteryFast: class object
    Output:
    - df: pd.DataFrame with 'Battery Left', 'Battery SOC', 'Cycle', 'Battery SOH' columns added
    - ENS_ratio: float, Energy Not Supplied ratio
    Function: 
    - Simulates the energy flows in the system including battery dynamics.
    - Computes ENS fast. Adapted for optimization.
    """
    
    dt = 0.5 # time interval: 30min = 0.5h
    df = df[["Output Power", "Load Power", "Temperature"]].copy()

    # --- Compute the power entering/leaving the battery ---
    PV_to_load = df["Output Power"] * PCU.eta_pv_to_load
    power_diff = PV_to_load - df["Load Power"]
    charge_cond = power_diff >= 0
    charge_power = (df["Output Power"] - df["Load Power"]/PCU.eta_pv_to_load) * PCU.eta_pv_to_batt
    discharge_power = (df["Load Power"] - PV_to_load) / PCU.eta_batt_to_load
    df["Battery Power"] = np.where(charge_cond, charge_power, -discharge_power)

    ENS_count = 0
    model = BatteryModel_fast(BatteryFast)
    
    # Convert to NumPy for speed
    load_power = df["Load Power"].values
    output_power = df["Output Power"].values
    battery_power = df["Battery Power"].values
    temperature = df["Temperature"].values

    _, bat_left = model.RunModel_fast(temperature, battery_power)

    # Compute energy demand and supply components (vectorized)
    demand = load_power[:-1] * dt
    pv_contribution = output_power[:-1] * PCU.eta_pv_to_load * dt
    battery_contribution = PCU.eta_batt_to_load * np.maximum(0, bat_left[:-1] - bat_left[1:])

    # ENS = demand - (pv + battery), clipped to ≥ 0
    ens_step = np.maximum(0, demand - pv_contribution - battery_contribution[:-1])
    ENS_count = ens_step.sum()
    ENS_ratio = ENS_count / (np.sum(load_power) * dt)
    
    return ENS_ratio

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

    #print(f"Cbat_min = {Cbat_min}, Cbat_max = {Cbat_max}")
    #print(f"Ppv_min = {Ppv_min}, Ppv_max = {Ppv_max}")
    
    return Cbat_min, Cbat_max, Ppv_min, Ppv_max

# Dummy stand-in fitness function until user provides actual LOLP and cost model

def addLoad(tables, design_years, Location):
    """
    Build a multi-year load profile by repeating seasonal daily tables over `design_years` years,
    starting from (current year - 1) and going backward.

    Parameters:
        tables (list of DataFrames): Seasonal tables with time ranges and power.
        design_years (int): Number of years to repeat backward from last full year.
        Location (object): Must have `latitude` and `longitude` attributes.

    Returns:
        Load object with multi-year DataFrame of load power.
    """

    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lng=Location.longitude, lat=Location.latitude)
    local_tz = pytz.timezone(tz_str)

    end_year = datetime.now().year - 1
    start_year = end_year - design_years + 1

    all_years_power = []

    for year in range(start_year, end_year + 1):
        # Define season ranges for this year
        season_ranges = [
            (datetime(year, 1, 1), datetime(year, 2, 28)),   # Winter
            (datetime(year, 3, 1), datetime(year, 5, 31)),   # Spring
            (datetime(year, 6, 1), datetime(year, 9, 30)),   # Monsoon
            (datetime(year, 10, 1), datetime(year, 12, 31))  # Summer
        ]

        # Create full datetime index for this year (30-minute intervals)
        full_index = pd.date_range(start=datetime(year, 1, 1),
                                   end=datetime(year, 12, 31, 23, 30),
                                   freq="30min",
                                   tz=local_tz)

        total_power = pd.Series(0, index=full_index)

        for df, (start_date, end_date) in zip(tables, season_ranges):
            date = start_date
            while date <= end_date:
                for _, row in df.iterrows():
                    try:
                        power = float(row["Power [W]"])
                        from_time = datetime.strptime(row["From [xx:xx XM]"].strip(), "%I:%M %p").time()
                        to_time   = datetime.strptime(row["To [xx:xx XM]"].strip(), "%I:%M %p").time()

                        start_dt = datetime.combine(date, from_time)
                        end_dt   = datetime.combine(date, to_time)
                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)

                        start_dt = local_tz.localize(start_dt)
                        end_dt   = local_tz.localize(end_dt)

                        ts_range = pd.date_range(start=start_dt, end=end_dt - timedelta(seconds=1), freq="30min", tz=local_tz)
                        total_power.loc[ts_range] += power

                    except Exception as e:
                        print(f"[{year}] Skipping row due to error: {e}")
                date += timedelta(days=1)

        all_years_power.append(total_power)

    # Combine all years into one DataFrame
    df_power = pd.concat(all_years_power).to_frame(name="Load Power")
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
        ENS_ratio = ENS_calc_fast(df_fast, pcu, mybat)
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
        ENS_ratio = ENS_calc_fast(df_fast, pcu, mybat)

        if ENS_ratio > 0.005:
            break
        min_found = (test_P, test_C)

    return min_found

def inverter_price(load_w):
    ##Fitted power load price of PCU/Load capacity
    return 299.82 * load_w**0.635

def optimizer(longitude, latitude, tabs, price_W_pv, price_Wh_bat, eta_tot, 
              cleaning_freq, rain_thresh, eta_cable, progress_callback, eta_load, design_year, df_solar = None):

    t1 = time.perf_counter()
    #Define location
    loc = Location(longitude, latitude)
    #Modify the load
    myload = addLoad(tabs,design_year, loc)
    t2 = time.perf_counter()
    print(f"[INIT] Setup time: {t2 - t1:.4f} s")
    #Fetch the dataframe and concad with load
    t3 = time.perf_counter()
    df = fetch_dataFrame(loc, design_year, df_solar, progress_callback)
    t4 = time.perf_counter()
    print(f"[DATA] Fetch_data: {t4 - t3:.4f} s")
    
    if isinstance(df, str):
        return df
    
    t5 = time.perf_counter()
    df = compute_ghi(df)
    t6 = time.perf_counter()
    print(f"[GHI] Compute GHI: {t6 - t5:.4f} s")
    #Merge the load and add load efficiency
    df = pd.concat([df, myload.loadProfile], axis=1)
    df["Load Power"] = df["Load Power"] / (eta_load / 100)
    max_load = df["Load Power"].max() * 1.2 #Added 20% of extra PCU capacity margin
    #Fetch the smallest system with ENS = 0
    t7 = time.perf_counter()
    Ppv_max, Cbat_max = findMaxSyst(df, loc, eta_tot, cleaning_freq, rain_thresh, eta_cable)
    print(f"[MAX] Find max system: Ppv_max = {Ppv_max}, Cbat_max = {Cbat_max}")
    price_max = price_W_pv * Ppv_max + price_Wh_bat* Cbat_max + inverter_price(max_load)
    t8 = time.perf_counter()
    print(f"[PRICE] Find maximum price: {t8 - t7:.4f} s")
    progress_callback(40)
    #Run the Optimization and get a dataframe
    t9 = time.perf_counter()
    pareto_points = Pareto.run_nsga2_pareto(df, loc, price_max,(0.1*Ppv_max, Ppv_max), (Cbat_max*0.1, Cbat_max), eta_tot, 
                                     cleaning_freq, rain_thresh, price_W_pv, price_Wh_bat, step_pv=25, 
                                     step_bat=100, progress_callback = progress_callback)
    pareto_points = pd.DataFrame(pareto_points, columns=["P_pv", "C_bat", "ENS", "Cost"])
    t10 = time.perf_counter()
    print(f"[PARETO] Find pareto points: {t10 - t9:.4f} s")

    return pareto_points

def safe_replace_year(ts: Timestamp, new_year: int) -> Timestamp:
    """
    Safely replaces the year in a timestamp, handling leap day issues.
    If the date is February 29 and the new year is not a leap year,
    it shifts the date to March 1.
    """
    try:
        return ts.replace(year=new_year)
    except ValueError:
        if ts.month == 2 and ts.day == 29:
            return ts.replace(year=new_year, month=3, day=1)
        else:
            raise

def repeat_df(df, num_repeats, freq="30min"):
    """
    Repeats a multi-year DataFrame backward in time by shifting the entire dataset.

    Parameters:
        df (pd.DataFrame): Original time-indexed DataFrame (multi-year).
        num_repeats (int): Number of total copies (including the original).
        freq (str): Frequency for interpolation.

    Returns:
        pd.DataFrame: Concatenated multi-year DataFrame.
    """
    df = df.copy()
    tz = df.index.tz
    years_covered = sorted({ts.year for ts in df.index})
    duration_years = years_covered[-1] - years_covered[0] + 1
    start_year = df.index[0].year

    dfs = []

    for i in reversed(range(num_repeats)):
        shift_years = duration_years * (num_repeats - 1 - i)
        target_year = start_year - shift_years

        def shift_year(ts):
            try:
                return ts.replace(year=ts.year - shift_years)
            except ValueError:
                # Handles leap year issues (Feb 29 → Feb 28)
                return ts.replace(month=2, day=28, year=ts.year - shift_years)

        df_shifted = df.copy()
        if shift_years > 0:
            df_shifted.index = df.index.map(shift_year)
        dfs.append(df_shifted)

    df_repeated = pd.concat(dfs).sort_index()

    # Remove duplicates from Feb 29 conflict
    df_repeated = df_repeated[~df_repeated.index.duplicated(keep='first')]

    # Reindex to fill small gaps
    full_index = pd.date_range(
        start=df_repeated.index.min(),
        end=df_repeated.index.max(),
        freq=freq,
        tz=tz
    )
    df_repeated = df_repeated.reindex(full_index)
    df_repeated.interpolate(method="time", inplace=True)

    return df_repeated

def drop_last_n_years(df, n=5):
    last_timestamp = df.index.max()
    cutoff_year = last_timestamp.year - n + 1
    return df[df.index.year < cutoff_year]

def batteryAging(df, PCU, Battery, design_year=15):
    """
    Extends battery simulation beyond design life using same input pattern,
    continuing from the final battery state.

    Parameters:
        df (pd.DataFrame): Full simulation result from ENS_calc_slow over design_years.
        PCU (object): The PCU used in the simulation.
        Battery (object): Battery object, which can be copied or reset.
        design_year (int): The number of design years originally simulated.

    Returns:
        bat_df_ext (DataFrame): Battery SOH and cycle trace (entire extended simulation).
        expected_time (str): Estimated life (e.g. '17.3' or '+45').
    """

    # STEP - Extract the signal data to run PCU + Battery simulation
    signal_df = df[["Load Power", "Output Power", "Temperature"]]
    base_year_duration = (signal_df.index[-1] - signal_df.index[0]).total_seconds()
    base_years = base_year_duration / (3600 * 24 * 365)

    # STEP — create extension df (e.g. 2× more years) total df will be of size (extension_factor + 1) years
    extension_factor = 2
    df_extension = repeat_df(signal_df, extension_factor)

    # STEP — simulate only the new years using final battery state
    bat_df_full, _ = ENS_calc_slow(df_extension, PCU, Battery)
    bat_df_full.sort_index(inplace=True)
    bat_df_full = bat_df_full[~bat_df_full.index.duplicated(keep='first')]

    # STEP — determine when battery SOH drops below threshold
    threshold = 0.8
    below_thresh = bat_df_full[bat_df_full["Battery Left"] < threshold]
    if not below_thresh.empty:
        first_failure = below_thresh.index[0]
        hours_to_fail = (first_failure - bat_df_full.index[0]).total_seconds() / 3600
        expected_life_years = round(hours_to_fail / (24 * 365), 1)
        expected_time = str(expected_life_years)
    else:
        expected_time = f'+{int(base_years * (1 + extension_factor))}'

    return bat_df_full[["Cycle", "Battery SOH"]], expected_time


def gross_mass(capacity):
    return 0.275*capacity + 3.13

def gross_height(capacity):
    return (0.293*capacity + 171.31)*10


def verifier(longitude, latitude, tabs, power, bat_capa, bat_lifetime, bat_cycle, 
            bat_series, bat_para, pv_num, soc_min, pcu_charge, pcu_inv, alpha, cleaningfreq,
            rainthresh, eta_tot, pcu_current, eta_cable, progress_callback, eta_load, design_year, 
            df_solar = None):
    
    # -- Define useful instances ---
    
    loc = Location(longitude, latitude)

    mybat = Battery(C_nom = bat_capa, SOC_min = soc_min/100, 
                    Mass = gross_mass(bat_capa), Bat_height = gross_height(bat_capa), 
                    Lifetime = bat_lifetime, Ziec = bat_cycle, 
                    Soc_init = 0.5, n_para = bat_para, 
                    n_serie = bat_series)
    
    pcu = PCU(eta_cable = eta_cable, max_charge_current = pcu_current, 
              pack_voltage = 12*bat_series, eta_inverter = pcu_inv/100, 
              eta_CC = pcu_charge/100)
    
    mypv = Panels(power = power, eta_tot = eta_tot, 
                  name=None, alpha=alpha/100, string_num=pv_num, 
                  string_dist=1, clean_freq = cleaningfreq, 
                  rainthresh = rainthresh)

    # -- Fetch ENS and LOLP
    myload = addLoad(tabs,design_year,loc)
    df = fetch_dataFrame(loc, design_year, df_solar, progress_callback)

    if isinstance(df, str):
        return df, None, None, None

    df = pd.concat([df, myload.loadProfile], axis=1)
    df["Load Power"] = df["Load Power"] / (eta_load / 100)

    df = compute_power_slow(df, mypv, loc)
    progress_callback(52)
    
    df, ENS_ratio = ENS_calc_slow(df, pcu, mybat)
    progress_callback(64)
    
    bat_df, expected_time = batteryAging(df, pcu, mybat)
    progress_callback(93)

    print(bat_df.describe())

    return df, ENS_ratio, bat_df, expected_time


