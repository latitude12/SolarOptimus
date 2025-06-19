from datetime import datetime
import LOLP
import pandas as pd
import csv

### --- FUNCTION DEFINITIONS OF INPUT CHECKS ---

def check_valid_type(value):
    """
    Verifies if the type is valid for simulations:
    Returns True if valid, False if invalid
    """
    if isinstance(value, int):
        return True
    elif isinstance(value, float):
        return True
    else:
        return False

def check_position(longitude, latitude):
    """
    Verifies if the longitude and latitude components are valid:
    Returns True if valid, False if invalid
    """
    if check_valid_type(longitude) == False or check_valid_type(latitude) == False:       
        return False
    if latitude<-90 or latitude>90:
        return False
    if longitude<-180 or longitude>180:
        return False
    
    return True

def check_efficiency(eff):
    """
    Verifies if the efficiency is valid:
    Returns True if valid, False if invalid
    """
    if eff<0 or eff>100:
        return False
    return True

def check_load(load):
    """
    Verifies if the load consumption is valid:
    Returns True if valid, False if invalid
    """
    if load<0:
        return False 
    return True

def check_times(start_str, end_str):
    """
    Verifies if the times of usage of the load is valid:
    Returns True if valid, False if invalid
    """
    fmt = "%H:%M"  # 24-hour format
    start = datetime.strptime(start_str.strip(), fmt)
    end = datetime.strptime(end_str.strip(), fmt)

    print(start)
    print(end)

    if start >= end:
        return False
    return True
    

def check_years(design_year):
    if check_valid_type(design_year) == False:    
        return False
    if design_year < 0:
        return False
    else: return True

def check_tables(df_tabs):
    all_valid = True

    for season_idx, df in enumerate(df_tabs):
        for row_idx, row in df.iterrows():
            try:
                # Validate power
                power = int(row['Power [W]'])
                if power <= 0: 
                    print('invalid power')
                    return False

                # Validate from/to time
                from_str = row['From [xx:xx XM]'].strip()
                to_str = row['To [xx:xx XM]'].strip()

                from_time = datetime.strptime(from_str, "%I:%M %p")
                to_time = datetime.strptime(to_str, "%I:%M %p")

                if from_time >= to_time:
                    print('invalid time diff')
                    return False

            except Exception as e:
                all_valid = False
                print('bad extraction')
                return False

    if all_valid: return True

def checksupzero(value):
    if value > 0: return True
    else: return False

def checkpercent(value):
    if value > 100 or value<0: return False
    else: return True

def checkOne(value):
    if value < 1: return False
    else: return True

def checkalpha(alpha):
    if alpha>0: return False
    else: return True

### --- FUNCTION DEFINITIONS OF OTHERS ---


def find_health(bat_df, design_year):

    # Starting time (first timestamp in the DataFrame)
    start_time = bat_df.index[0]

    # Target time = start + N years
    target_time = start_time + pd.DateOffset(years=design_year)

    # Find the nearest index *at or before* the target time
    idx = bat_df.index.get_indexer([target_time], method="nearest")[0]

    # Retrieve SOH
    return bat_df.iloc[idx]["Battery SOH"]

def load_csv(window, filepath):
    """
    Load a CSV file with unknown delimiter into a pandas DataFrame,
    expecting specific columns: Year, Month, Day, Hour, Minut, DHI, DNI, Temperature, Wind.
    Returns an empty string if the file cannot be opened.
    """
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter

        df = pd.read_csv(filepath, delimiter=delimiter)
        print(df)

        expected_cols = ['Month', 'Day', 'Hour', 'DNI', 'DHI', 'Temperature', 'Wind']
        missing = [col for col in expected_cols if col not in df.columns]
        
        if 'Year' not in df.columns:
            df['Year'] = 2024  # or extract from file if known
        if 'Minute' not in df.columns:
            df['Minute'] = 0

        if missing:
            return window._return_error("Invalid Solar File")
        
        return df

    except Exception as e:
        # You can also log `e` if needed
        print("No solar data input by the user")
        return None


### --- DIRECT OPERATIONS FUNCTIONS ---

def launchOpti(window):
    #Check Latitude and longitude
    tabs = []
    window._updateProgress(0)
   
    try:
        
        longitude = float(window.get_longitude())
        latitude = float(window.get_latitude())
        design_year = int(window.get_years())
        eta_shading = float(window. get_param_shading())
        eta_mismatch = float(window.get_param_mismatch())
        eta_connectors = float(window.get_param_connect())
        eta_nameplate = float(window.get_param_nameplate())
        eta_light = float(window.get_param_light())
        eta_cables = float(window.get_param_cable())
        cleaningfreq = int(window.get_param_PVrate())
        rainthresh = float(window.get_param_PVrain())
        PricePerW = float(window.get_param_Wprice())
        PricePerWh = float(window.get_param_Whprice())
        etaLoad = float(window.get_param_loadEff())
        soc_init = float(window.get_param_SOCinit())
        solar_path = str(window.get_solar_file())

        for i in range(4):
            tabs.append(window.get_tableItem(i))
        #for in range
    
    except ValueError:
        print("Type input Error")  
        return window._return_error("Invalid format") 

    if not check_position(longitude, latitude): return window._return_error("Lat/Long invalid")
    if not check_years(design_year): return window._return_error("Years invalid")
    if not check_tables(tabs): return window._return_error("Invalid Load")
    if not checkpercent(eta_shading): return window._return_error("Invalid PV Loss")#
    if not checkpercent(eta_mismatch): return window._return_error("Invalid PV Loss")#
    if not checkpercent(eta_connectors): return window._return_error("Invalid PV Loss")#
    if not checkpercent(eta_nameplate): return window._return_error("Invalid PV Loss")#
    if not checkpercent(eta_light): return window._return_error("Invalid PV Loss")#
    if not checkpercent(eta_cables): return window._return_error("Invalid PV Loss")#
    if not checkpercent(etaLoad): return window._return_error("Invalid Load efficiency")
    if not checkpercent(soc_init): return window._return_error("Invalid Initial SOC")
    if not checksupzero(PricePerW): return window._return_error("Invalid Price/W") #
    if not checksupzero(PricePerWh): return window._return_error("Invalid Price/Wh") #
    if not checksupzero(cleaningfreq): return window._return_error("Invalid Cleaning")
    if not checksupzero(rainthresh): return window._return_error("Invalid Rain")
    df_solar_data = load_csv(window, solar_path)

    eta_tot = ((1-eta_shading/100) * (1-eta_mismatch/100) * (1-eta_connectors/100) * (1-eta_light/100) * (1-eta_nameplate/100))
    print(f"Eta_tot is {eta_tot}")
    window._updateProgress(5)
    pareto_points = LOLP.optimizer(longitude, latitude, tabs, PricePerW, PricePerWh, eta_tot, 
                                   cleaningfreq, rainthresh, eta_cables, window._updateProgress, 
                                   etaLoad, df_solar=df_solar_data)
    window.df_full = pareto_points
    window.just_launched = True
    window._disable_button()
    window._updatePlot(pareto_points)
    
    return

def launchVerification(window):

    tabs = []
    #Cannot download or see results anymore
    window._updateProgress(0)
    window._downloadtoggle(False)
    window._hideFinalResult()

    
    try:
        #First page
        longitude = float(window.get_longitude())
        latitude = float(window.get_latitude())
        design_year = int(window.get_years())
        for i in range(4):
            tabs.append(window.get_tableItem(i))
        
        #Second page
        power = float(window.get_power())
        alpha = float(window.get_temp_coef())
        area = float(window.get_area())
        pv_num = int(window.get_PV_num())
        pcu_inv = float(window.get_PCU_inv())
        pcu_charge = float(window.get_PCU_charge())
        bat_capa = float(window.get_capa())
        bat_height = float(window.get_height())
        bat_mass = float(window.get_mass())
        soc_min = float(window.get_SOC_min())
        bat_cycle = int(window.get_cycle())
        bat_lifetime = float(window.get_lifetime())
        bat_para = int(window.get_bat_para())
        bat_series = int(window.get_bat_series())

        #Parameters
        #ETA values
        eta_shading = float(window. get_param_shading())
        eta_mismatch = float(window.get_param_mismatch())
        eta_connectors = float(window.get_param_connect())
        eta_nameplate = float(window.get_param_nameplate())
        eta_light = float(window.get_param_light())
        eta_cables = float(window.get_param_cable())
        #Soiling
        cleaningfreq = int(window.get_param_PVrate())
        rainthresh = float(window.get_param_PVrain())
        #Others
        PricePerW = float(window.get_param_Wprice())
        PricePerWh = float(window.get_param_Whprice())
        etaLoad = float(window.get_param_loadEff())
        soc_init = float(window.get_param_SOCinit())
        pcu_current = float(window.get_max_current())
        solar_path = str(window.get_solar_file())

    except ValueError:
        print("Type input Error")  
        return window._return_error_2("Invalid format")

    #Verification that values are within bounds
    if not check_position(longitude, latitude): return window._return_error_2("Lat/Long invalid")
    if not check_years(design_year): return window._return_error_2("Years invalid")
    if not check_tables(tabs): return window._return_error_2("Invalid Load")
    if not checksupzero(power): return window._return_error_2("Invalid Power")
    if not checksupzero(area): return window._return_error_2("Invalid Area")
    if not checksupzero(bat_capa): return window._return_error_2("Invalid Capacity")
    if not checksupzero(bat_lifetime): return window._return_error_2("Invalid Lifetime")
    if not checkOne(bat_cycle): return window._return_error_2("Invalid Cycle")
    if not checksupzero(bat_height): return window._return_error_2("Invalid Height")
    if not checksupzero(bat_series): return window._return_error_2("Invalid #Battery")
    if not checksupzero(bat_mass): return window._return_error_2("Invalid Mass")
    if not checksupzero(bat_para): return window._return_error_2("Invalid #Battery")
    if not checkOne(pv_num): return window._return_error_2("Invalid #PV-panels")
    if not checkpercent(soc_min): return window._return_error_2("Invalid SOC min")
    if not checkpercent(pcu_charge): return window._return_error_2("Invalid PCU")
    if not checkpercent(pcu_inv): return window._return_error_2("Invalid PCU")
    if not checkalpha(alpha): return window._return_error_2("Invalid alpha")
    if not checkpercent(eta_shading): return window._return_error_2("Invalid PV Loss")
    if not checkpercent(eta_mismatch): return window._return_error_2("Invalid PV Loss")
    if not checkpercent(eta_connectors): return window._return_error_2("Invalid PV Loss")
    if not checkpercent(eta_nameplate): return window._return_error_2("Invalid PV Loss")
    if not checkpercent(eta_light): return window._return_error_2("Invalid PV Loss")
    if not checkpercent(eta_cables): return window._return_error_2("Invalid PV Loss")
    if not checkpercent(etaLoad): return window._return_error_2("Invalid Load efficiency")
    if not checkpercent(soc_init): return window._return_error_2("Invalid Initial SOC")
    if not checksupzero(PricePerW): return window._return_error_2("Invalid Price/W")
    if not checksupzero(PricePerWh): return window._return_error_2("Invalid Price/Wh")
    if not checksupzero(cleaningfreq): return window._return_error_2("Invalid Cleaning")
    if not checksupzero(rainthresh): return window._return_error_2("Invalid Rain")
    if not checksupzero(pcu_current): return window._return_error_2("Invalid PCU Current")
    df_solar_data = load_csv(window, solar_path)

    window._updateProgress_2(10)
    eta_tot = ((1-eta_shading/100) * (1-eta_mismatch/100) * (1-eta_connectors/100) * (1-eta_light/100) * (1-eta_nameplate/100))

    df, _, ens, bat_df, lifetime_exp = LOLP.verifier(longitude, latitude, tabs, power, area, 
                                bat_capa, bat_lifetime, bat_cycle, bat_height, bat_series, 
                                bat_mass, bat_para, pv_num, soc_min, pcu_charge, pcu_inv, 
                                alpha, cleaningfreq, rainthresh, eta_tot, pcu_current, eta_cables, 
                                window._updateProgress_2, etaLoad, df_solar= df_solar_data)
    
    design_health = str(round(find_health(bat_df, design_year)*100,1))
    print(f"The ENS computed is LOLP.py is {ens}")
                
    window.design_year = design_year
    window.df_final.append(df)
    window._showfinalInfo(str(round(ens*100,2)))
    window._showBatteryInfo(lifetime_exp,design_health)
    window._resampleSystem()
    window._updateBatteryplot(bat_df)
    window._downloadtoggle(True)
    window._updateProgress_2(100)

    return

