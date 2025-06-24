import numpy as np
import pandas as pd
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.termination import get_termination
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize

# Your domain-specific imports
from ENS_model import Panels, PCU, BatteryFast, compute_power_fast, ENS_calc_fast, inverter_price

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
        out["F"] = np.array([
            evaluate_one(x, self.df, self.location, self.step_pv, self.step_bat,
                        self.eta_tot, self.clean_freq, self.rain_thresh,
                        self.price_W_pv, self.price_Wh_bat, self.price_max)
            for x in X
        ])

def evaluate_one(x, df, location, step_pv, step_bat, eta_tot, clean_freq, rain_thresh, price_W_pv, price_Wh_bat, price_max):
    """
    Evaluates a single solution for ENS and normalized cost.
    Parameters are injected via functools.partial.
    """
    P_pv, C_bat = x

    # Round to step sizes
    P_pv = max(step_pv, int(P_pv // step_pv) * step_pv)
    C_bat = max(step_bat, int(C_bat // step_bat) * step_bat)

    # Instantiate system components
    panel = Panels(power=P_pv, eta_tot=eta_tot, clean_freq=clean_freq, rainthresh=rain_thresh)
    pcu = PCU()
    battery = BatteryFast(C_nom=C_bat / 12, SOC_min=0.2, Soc_init=0.5)

    # Simulate system behavior
    df_fast = compute_power_fast(df, panel, location)
    ENS_ratio = ENS_calc_fast(df_fast, pcu, battery)

    # Compute normalized cost
    inverter_cost = inverter_price(df["Load Power"].max() * 1.2)
    total_cost = P_pv * price_W_pv + C_bat * price_Wh_bat + inverter_cost
    normalized_cost = total_cost / price_max

    return [ENS_ratio, normalized_cost]

# Define and run the optimizer
def run_nsga2_pareto(df, location, price_max, pv_bounds, bat_bounds, 
                     eta_tot, cleaning_freq, rain_thresh,  price_W_pv, price_Wh_bat, step_pv=25, step_bat=100, 
                     pop_size=80, n_gen=10, progress_callback=None):
    
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
        verbose=False,
        callback=my_progress_callback
    )

    pareto_df = pd.DataFrame(res.X, columns=["P_pv", "C_bat"])
    pareto_df["ENS"] = res.F[:, 0]
    pareto_df["Cost"] = res.F[:, 1]

    return pareto_df