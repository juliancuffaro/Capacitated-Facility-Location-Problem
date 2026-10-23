from common.datatypes import *
from fit_model import fit_model
from itertools import product
import math
import pandas as pd
import pyomo.environ as pyo


#Parse data from CSVs into datatypes
Dist_Center.csv_to_centers("CSVs/distribution_centers.csv")
Cust_Zone.csv_to_zones("CSVs/customer_zones.csv")
Plant.csv_to_plants("CSVs/production_plants.csv")

n_centers = len(Dist_Center.centers)
n_zones = len(Cust_Zone.zones)
n_plants = len(Plant.plants)

df = pd.read_csv("CSVs/commodity_rates.csv")
n_commodities = df.shape[1]

commodity_rates = []
for i in range(n_commodities):
    commodity_rates.append(df.iloc[0, i])
#commodity_rates now stores transport cost per unit per km travelled for each commodity

cost_pd = {(c,p,d): CIRCUITY * commodity_rates[c] * hav_dist(Plant.plants[p].loc, Dist_Center.centers[d].loc)
           for c,p,d in product(range(n_commodities), range(n_plants), range(n_centers))} # per unit cost of shipping c for the first leg

cost_dz = {(c,d,z): CIRCUITY * commodity_rates[c] * hav_dist(Dist_Center.centers[d].loc, Cust_Zone.zones[z].loc)
           for c,d,z in product(range(n_commodities), range(n_centers), range(n_zones))} #per unit cost of shipping c for the second leg

m = fit_model(n_commodities, n_plants, n_centers, n_zones, cost_pd, cost_dz)
solver = pyo.SolverFactory('highs')
result = solver.solve(m)

#Brief summary of results
print(result.solver.termination_condition)
print(round(result.problem.lower_bound, 2))

#Extensive summary is written to Output/main_out.txt
fobj = open("Output/main_out.txt", "w")
for d in range(n_centers):
    if pyo.value(m.v[d]) > 0:
        fobj.write("Distribution center " +  str(d) + " is opened. \n")

for (c,p,d,z) in product(m.C, m.P, m.D, m.Z):
    if (round(pyo.value(m.y[d,z])) == 1):
        shipped = round(pyo.value(m.x[c,p,d])) #We expect commodity amounts to be integers
        if shipped > 0:
            fobj.write("Distribution center " + str(d) +  " ships " + str(shipped) + " of commodity " + str(c) + 
            " from plant " + str(p) + " to customer zone " + str(z) + ".\n")

final_result = round(pyo.value(m.objective), 3)
fobj.write("Optimal Objective value: " + str(final_result))
fobj.close()

