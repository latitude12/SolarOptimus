# This battery aging model is based primarily on the lifetime prediction framework
# described in the following paper:
#
# Julia Schiffer, Dirk Uwe Sauer, Henrik Bindner, Tom Cronin, Per Lundsager, Rudi Kaiser,
# "Model prediction for ranking lead-acid batteries according to expected lifetime in renewable energy systems
# and autonomous power-supply systems", Journal of Power Sources, Volume 168, Issue 1, 2007, Pages 66–78.
# DOI: 10.1016/j.jpowsour.2006.11.092
#
# The implementation includes weighted Ah throughput, corrosion modeling, acid stratification,
# sulfation effects, and SOC-dependent degradation, following the approach described in the paper.

import numpy as np

# Corrosion curve data: Voltage [V] vs corrosion speed (empirical, used for interpolation)
# From /* Bindner et al. (2005) / Section 5.2.1.1 / Figure #11 */
LANDER_CURVE_X = np.array([0, 0.5, 1.576, 1.598, 1.664, 1.686, 1.709, 1.739,
                           1.950, 2.029, 2.099, 2.151, 2.184])
LANDER_CURVE_Y = np.array([0.053305, 0.055084, 0.346755, 0.666663, 0.368389,
                           0.347145, 0.048716, 0.016842, 0.017591, 0.177787,
                           0.615137, 2.00125, 5.00777])

### FAST MODEL ###

class BatteryFast:
    def __init__(self,C_nom, SOC_min, Soc_init, V_nom=12):
        self.C_nom = C_nom
        self.SOC_min = SOC_min
        self.Soc_init = Soc_init
        self.V_nom = V_nom

def run_battery_model(T_array, P_array, soc_init, u_init,
                      C_nom, Uo, g, Cc, Cd, Mc, Md, pc, pd,
                      I_gas0, U_gas0, T_gas0, c_u, c_t, delta_t, SOC_min):
    
    n = len(T_array)
    SOC = np.empty(n + 1)
    U = np.empty(n + 1)
    Igas = np.empty(n)

    SOC[0] = soc_init
    U[0] = u_init

    for i in range(n):
        soc_last = SOC[i]
        U_last = U[i]
        I = P_array[i] / (U_last * 6)
        I_div_C = I / C_nom

        # Compute terminal voltage
        if I > 0:
            U_t = (Uo - g * (1 - soc_last)
                   + pc * I_div_C
                   + pc * Mc * I_div_C * (soc_last / (Cc - soc_last)))
        else:
            U_t = (Uo - g * (1 - soc_last)
                   + pd * I_div_C
                   + pd * Md * I_div_C * ((1 - soc_last) / (Cd - (1 - soc_last))))

        # Clip voltage
        U_safe = min(2.45, max(1.5, U_t))
        U[i + 1] = U_safe

        # Gassing current
        igas = ((C_nom / 100) * I_gas0 *
                np.exp(c_u * (U_safe - U_gas0) +
                       c_t * ((T_array[i] + 273.15) - T_gas0)))
        Igas[i] = igas

        # SoC update
        SOC_next = soc_last + (I - igas) * delta_t / (3600 * C_nom)
        SOC[i + 1] = min(1.0, max(SOC_min, SOC_next))
    
    E_left = C_nom * U * 6 * SOC

    return SOC, E_left

class BatteryModel_fast:
    def __init__(self, bat):
        
        # Voltage and SOC
        self.soc_init = bat.Soc_init
        self.U = bat.V_nom
        self.SOC = []; self.SOC.append(bat.Soc_init)
        self.SOC_min = bat.SOC_min
        self.V_nom = bat.V_nom

        #Gassing constants
        self.Igas = []
        self.U_gas0 = 2.23
        self.I_gas0 = 0.02
        self.T_gas0 = 298
        self.c_u = 11
        self.c_t = 0.06

        #Voltage estimation
        self.p_nom = 1.28  # [cm³/g]
        self.Uo = 0.86 + self.p_nom  # OCV baseline
        self.m = 30 * bat.C_nom  # The mass of electrolyte is approx 30g/Ah
        self.C_nom = bat.C_nom  # nominal capacity [Ah]
        self.a_rho = 0.4956
        self.b_rho = 0.2456
        self.c_rho = 77.53
        self.d_rho = -0.01278
        self.e_rho = 0.01289
        self.f_rho = 0.0373
        self.Cc = 1.001
        self.Md = 0.0464
        self.pc = 0.242 #To add variation
        self.pd = 0.242 #To add variation
        self.Mc =  0.888
        self.Cd = 1.001

        self.term = (self.d_rho + self.e_rho * self.p_nom) * self.m - self.f_rho * self.C_nom
        self.under_sqrt = self.b_rho + self.c_rho * self.p_nom / self.m * self.term
        self.p_empty = self.a_rho + np.sqrt(self.under_sqrt) if self.under_sqrt > 0 else self.a_rho
        self.g = self.p_nom - self.p_empty

        #time
        self.delta_t = 30 * 60  # 30 minutes in seconds

    def RunModel_fast(self, T,P):
        return run_battery_model(T, P, self.soc_init, self.U,
                          self.C_nom, self.Uo, self.g, self.Cc, self.Cd, self.Mc, self.Md, self.pc, self.pd,
                          self.I_gas0, self.U_gas0, self.T_gas0, self.c_u, self.c_t, self.delta_t, self.SOC_min)

### SLOW BUT PRECISE MODEL ###

#Used for slow but precise simulation
class Battery:
    def __init__(self,C_nom, SOC_min, Mass, Bat_height, Lifetime, Ziec, Soc_init, n_para, n_serie, V_nom = 12):
        self.C_nom = C_nom  # Nominal capacity of one battery capacity [Ah]
        self.n_para = n_para # Number of battery strings in parallel
        self.n_series = n_serie # Number of battery strings in series
        self.SOC_min = SOC_min  # Minimum allowed state of charge (0-1)
        self.Mass = Mass  # Battery mass [kg]
        self.Bat_height = Bat_height*1e-2  # Battery height [m]
        self.Lifetime = Lifetime  # Lifetime in years
        self.Ziec = Ziec  # IEC reference cycle lifetime
        self.V_nom = V_nom # Nominal voltage [V] of one battery
        self.Soc_init = Soc_init  # Initial SOC (0-1)

class BatteryModel:
    def __init__(self, bat):
        
        self.n_para = bat.n_para
        self.n_series = bat.n_series
        #SOC min tracking
        self.soc_min = 1.
        self.idx_min = None
        self.tracking = False
        self.soc_max = bat.Soc_init #Something to see here mhm
        self.last_was_discharge = False
        
        # Voltage and SOC
        self.U = [bat.V_nom]
        self.SOC = []; self.SOC.append(bat.Soc_init)
        self.SOC_min = bat.SOC_min
        self.V_nom = bat.V_nom
        self.I_t = []
        self.I_track = False

        #Gassing constants
        self.Igas = []
        self.U_gas0 = 2.23
        self.I_gas0 = 0.02
        self.T_gas0 = 298
        self.c_u = 11
        self.c_t = 0.06

        #Voltage estimation
        self.p_nom = 1.28  #[cm³/g]
        self.Uo = 0.86 + self.p_nom  # CV baseline
        self.m = bat.Mass * 0.25 * 1000  #mass of electrolyte adapted to [g] ~25% of battery weighy
        self.C_nom = bat.C_nom  #nominal capacity [Ah]
        self.Cc = 1.001
        self.Md = 0.0464
        self.pc = [0.242] 
        self.pd = [0.242] 
        self.Mc =  0.888

        # Estimate p_empty (min electrolyte conc.) from empirical equation
        self.a_rho = 0.4956
        self.b_rho = 0.2456
        self.c_rho = 77.53
        self.d_rho = -0.01278
        self.e_rho = 0.01289
        self.f_rho = 0.0373
        self.term = (self.d_rho + self.e_rho * self.p_nom) * self.m - self.f_rho * self.C_nom
        self.under_sqrt = self.b_rho + self.c_rho * self.p_nom / self.m * self.term
        self.p_empty = self.a_rho + np.sqrt(self.under_sqrt) if self.under_sqrt > 0 else self.a_rho
        self.g = self.p_nom - self.p_empty

        #Corrosion Impact
        self.T_corr0 = 298
        self.lifetime = bat.Lifetime * 356 * 24 * 3600 
        self.ksT = np.log(2)/15
        self.C_corr_lim = 0.2 
        self.U_corr0 = 1.75
        self.Cd = [1.]  #Battery starts at 100% of its nominal capacity
        self.W_corr_lim = self.lifetime * self.corrosion_speed(self.V_nom 
                                                               * np.exp(self.ksT*((25 + 273.15) - self.T_corr0)))
        self.U_corr = [self.U_corr0]
        self.W_corr = [0]
        self.C_corr = [0]
        self.p_corr = []
        self.p_corr_lim = 0.2 * self.pc[0]

        #Degradation impact
        self.c_plus = 1/30
        self.c_minus = 0.1
        self.Diff_coef = 20e-9

        #fmin_gass and fmin_diff
        self.f_strat = [0] # Stratification increase factor
        self.f_min_gas = []
        self.f_min_diff = []
        self.f_min = []
        self.f_plus = []
        self.f_acid = []
        self.U_ref = 2.5
        self.z_height = bat.Bat_height
        self.I_ref = self.C_nom/10
        self.Cdeg_lim = 0.8
        self.Ziec = bat.Ziec
        self.Zw = [0] # Weighted cycle throughput
        self.Cdeg = [0] # Capacity loss due to degradation

        #SOC capacity impact
        self.n = [0]
        self.f_soc = []
        self.soc_max = 1
        self.Csoc_0 = 6.614e-5#converting to seconds
        self.Csoc_min = 3.307e-3#converting to seconds
        self.f_I = 0 # Current-dependent scaling

        #time
        self.delta_t = 30 * 60  # 30 minutes in seconds

    def corrosion_speed(self, voltage):
        # Interpolates corrosion speed [1/s] from experimental voltage-speed curve
        sp = np.interp(voltage, LANDER_CURVE_X, LANDER_CURVE_Y, left=0.0, right=5.0)/3600
        return sp
        
    def find_SOC_min(self, soc, delta_t, i):
        """
        Tracks the minimum SOC since the last full charge.
    
        Returns:
            soc_min: Minimum SOC since last full charge
            delta_t_since_min: Time since that minimum occurred
        """
        if soc >= 1:
            # Reset at full charge
            self.soc_min = 1.0
            self.idx_min = None
            self.tracking = True
            return self.soc_min, 0
    
        if self.tracking:
            if self.idx_min is None:
                # First time SOC drops below 1
                self.idx_min = i
                self.soc_min = soc
            elif soc < self.soc_min:
                self.soc_min = soc
                self.idx_min = i
    
        delta_t_since_min = (i - self.idx_min) * delta_t if self.idx_min is not None else 0
        return self.soc_min, delta_t_since_min
        
    def RunModel(self, T,P):

        # Convert power [W] to current [A]
        I = P / (self.n_para * self.U[-1] * 6 * self.n_series) # Assumes 6 cells in series
        self.I_t.append(I)
    
        #### CELL VOLTAGE ###
        if I > 0:  # charging mode
            U_t = (self.Uo - self.g * (1 - self.SOC[-1]) + self.pc[-1] * I / self.C_nom 
            + self.pc[-1] * self.Mc * (I / self.C_nom) * (self.SOC[-1] / (self.Cc - self.SOC[-1])))
        else:  # discharging mode
            U_t = (self.Uo - self.g * (1 - self.SOC[-1]) + self.pd[-1] * I / self.C_nom 
            + self.pd[-1] * self.Md * (I / self.C_nom) * ((1 - self.SOC[-1]) / (self.Cd[-1] - (1 - self.SOC[-1]))))

        # Limit voltage to a safe physical cell range
        U_safe = np.clip(U_t, 1.5, 2.45)
        self.U.append(U_safe)

        ### CORROSION IMPACT ###
        # Estimate corrosion voltage depending on charge/discharge regime
        if I >0:    # charge mode
            U_corr_t = (self.U_corr0 - (10./13.) * self.g * (1- self.SOC[-1]) 
            + 0.5 * self.pc[-1] * self.Mc * I/self.C_nom * self.SOC[-1]/(self.Cc - self.SOC[-1]) + 0.5 * self.pc[-1] * I/self.C_nom)
        else:   # discharging mode
            U_corr_t = (self.U_corr0 - (10./13.) * self.g * (1- self.SOC[-1]) 
            + 0.5 * self.pd[-1] * self.Md * I/self.C_nom * (1 - self.SOC[-1])/(self.Cd[-1] - (1 - self.SOC[-1])) + 0.5 * self.pd[-1] * I/self.C_nom)

        self.U_corr.append(U_corr_t)
        
        # Calculate corrosion rate based on temperature and voltage
        k_s = max(self.corrosion_speed(self.U_corr[-1]) * np.exp(self.ksT * ((T + 273.15) - self.T_corr0)), 1e-10)
        
        # corrosion layer and resistivity update
        if self.U_corr[-1]<1.74:
            x = (self.W_corr[-1] / k_s)**(1/0.6) + self.delta_t
            W_corr_t = k_s * x ** 0.6
        elif self.U_corr[-1]>=1.74:
            W_corr_t = self.W_corr[-1] + k_s*self.delta_t

        else: W_corr_t = self.W_corr[-1]

        self.W_corr.append(W_corr_t)

        # Update capacity loss due to corrosion
        self.C_corr += [self.C_corr_lim * self.W_corr[-1]/ self.W_corr_lim]
        self.p_corr += [self.p_corr_lim * self.W_corr[-1]/ self.W_corr_lim]
        self.pc += [self.pc[0] + self.p_corr[-1]]
        self.pd += [self.pd[0] + self.p_corr[-1]]

        ### GASSING IMPACT ###

        # Compute gassing current
        self.Igas += ([(self.C_nom / 100) * self.I_gas0 * np.exp(self.c_u * (U_safe - self.U_gas0) 
                                                               + self.c_t * ((T + 273.15) - self.T_gas0))])
        ### SOC CAPACITY IMPACT ###
        if len(self.SOC) >= 2:
            soc_prev = self.SOC[-2]
            soc_now = self.SOC[-1]
        
            if soc_now > soc_prev:
                # Charging → track peak
                self.soc_max = max(self.soc_max, soc_now)
                self.last_was_discharge = False  # reset flag
                self.n.append(self.n[-1]) # no degradation increment
        
            elif soc_now < soc_prev and not self.last_was_discharge:
                # First discharge step → evaluate bad charge
                if self.soc_max >= 0.9999:
                    self.n.append(0) # fully charged: no degradation
                elif self.soc_max >= 0.5:
                    # Apply a non-linear penalty for not fully charging
                    raw_weight = (0.0025 - (0.95 - self.soc_max)**2) / 0.0025
                    weight = max(raw_weight, 0)
                    self.n.append(self.n[-1] + weight)
                else:
                    self.n.append(self.n[-1])  # too low → ignore
                self.soc_max = soc_now  # reset for next cycle
                self.last_was_discharge = True
        
            else:
                # Still discharging → skip
                self.n.append(self.n[-1])
                
        SOC_last, delta_soc = self.find_SOC_min(self.SOC[-1], self.delta_t, len(self.U)-1)

        if len(self.SOC) >= 2:
            soc_prev_ = self.SOC[-2]
            soc_now_ = self.SOC[-1]
            
            if soc_now_ >= 0.99 and soc_now_ >= soc_prev_:
                self.I_track = True
                
            if soc_now_< soc_prev_:
                if soc_now_ < 0.98:  # None and delta_soc != 0:
                    if self.I_track == True:
                        self.I_curr = self.I_t[-1]
                        self.f_I = pow(self.C_nom/(10*abs(self.I_curr)), 1/2) * pow(np.exp(self.n[-1]/3.6), 1/3)
                        self.I_track = False

        else: 
            self.I_curr = 1
                    
        # SOC-related degradation scaling factor
        self.f_soc += [0] if delta_soc is None else [1 + self.Csoc_0 + self.Csoc_min*(1-SOC_last)*delta_soc*self.f_I/3600]

        ### STRATIFICATION IMPACT ###
        # Mixing due to gassing
        self.f_min_gas += ([self.c_minus * np.sqrt(100/self.C_nom) * self.Igas[-1]/(self.I_gas0*3600)])
        # Mixing due to natural diffusion
        self.f_min_diff += [8 * self.Diff_coef / self.z_height ** 2 * self.f_strat[-1] * pow(2, (T - 20)/10)]
        # Total mixing
        self.f_min += [self.f_min_gas[-1] + self.f_min_diff[-1]]

        # Stratification growth during discharge
        self.f_plus += [0] if I > 0 else [self.c_plus / 3600 * (1-SOC_last)*np.exp(-3*self.f_strat[-1])* abs(I)/self.I_ref]

         # Update stratification state
        self.f_strat += [self.f_strat[-1] + (self.f_plus[-1] - self.f_min[-1])*self.delta_t]
        if self.f_strat[-1]<0: self.f_strat[-1] = 0
            
        self.f_acid += [1] if I == 0 else [1 + self.f_strat[-1] * np.sqrt(self.I_ref/abs(I))]

        ### COMPUTING C_DEG ###

        # Update weighted cycle throughput only during discharge
        self.Zw += ([self.Zw[-1] + self.delta_t / (3600*self.C_nom) * (
            self.f_acid[-1]*self.f_soc[-1]*abs(I))] if I <0 else [self.Zw[-1]])
        
        # Compute remaining capacity from weighted throughput
        self.Cdeg += [self.Cdeg_lim * np.exp(-5 * ( 1 - (self.Zw[-1]/(1.6*self.Ziec))))]
        #print(Cdeg[t])
                                             
        ### UPDATING CAPACITY ###
        self.Cd +=  [self.Cd[0] - self.C_corr[-1] - self.Cdeg[-1]]
        if self.Cd[-1]<0: self.Cd[-1] = 1e-3

        # Update SoC
        self.SOC += [self.SOC[-1] + (I - self.Igas[-1]) * self.delta_t / (3600 * self.C_nom)]
        # Clamp SOC within valid range
        self.SOC[-1] = np.clip(self.SOC[-1], self.SOC_min, 1)

    def getInfo(self):
        E_left = (self.Cd[-1]*self.U[-1]*6*self.SOC[-1]*self.C_nom) * self.n_para * self.n_series
        return E_left, self.SOC[-1], self.Zw[-1], self.Cd[-1], 6*self.U[-1]
    