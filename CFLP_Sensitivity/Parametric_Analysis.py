from CFLP_Sensitivity.fit_many import *
from itertools import product
import pandas as pd
import math
import pyomo.environ as pyo
from common.datatypes import *

def run_sweep(m, scales, solver):
    """
    Solves the model, m, with re-scaled commodity rates. At each iteration, the rates are multiplied by an element in scales,
    the model is re-solved and formatted into a pandas DataFrame, then written to the Output/parametric_out.txt file.

    Parameters:
        m: (pyo.ConcreteModel) model representing a CFLP
        scales: ([float]) list of scales we want to apply to our commodity rates and re-solve the problem.
        solver: (pyo.OptSolver) used to optimize the model

    Returns:
        none

    """
    fobj = open('Output/parametric_out.txt', 'w')
    for i, s in enumerate(scales):
        for c in m.C:
            m.rate[c] = base_rates[c] * s
        r = Optimize(m, solver)
        r["Scale"] = s
        row = pd.DataFrame([r])[["Scale", "Status", "Objective", "Open Centers"]] #DataFrame takes a dict as input ... inner double brackets represent a list of columns
        fobj.write(row.to_string(header = (i == 0), index = False) + '\n')
    print('Optimization complete')
    fobj.close()

#Parsing Data and Prepare for Fitting Model
Dist_Center.csv_to_centers("CSVs/distribution_centers.csv")
Cust_Zone.csv_to_zones("CSVs/customer_zones.csv")
Plant.csv_to_plants("CSVs/production_plants.csv")

n_centers = len(Dist_Center.centers)
n_zones = len(Cust_Zone.zones)
n_plants = len(Plant.plants)

df = pd.read_csv("CSVs/commodity_rates.csv")
n_commodities = df.shape[1]

base_rates = []
for i in range(n_commodities):
    base_rates.append(df.iloc[0, i])

dist_pd = {(p,d): CIRCUITY * hav_dist(Plant.plants[p].loc, Dist_Center.centers[d].loc)
           for p,d in product(range(n_plants), range(n_centers))} # distance of the first leg

dist_dz = {(d,z): CIRCUITY * hav_dist(Dist_Center.centers[d].loc, Cust_Zone.zones[z].loc)
           for d,z in product(range(n_centers), range(n_zones))} #distance of the second leg

m = fit_model(n_commodities, n_plants, n_centers, n_zones, base_rates, dist_pd, dist_dz)
solver = pyo.SolverFactory('appsi_highs')
