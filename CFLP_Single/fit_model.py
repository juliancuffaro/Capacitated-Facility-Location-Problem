import pyomo.environ as pyo
from common.datatypes import *

def fit_model(n_commodities, n_plants, n_centers, n_zones, cost_pd, cost_dz):
    """
    Creates a pyomo Concrete model using the given information
    
    Parameters:
        
    n_commodities: (int) number of commodities
    n_plants: (int) number of production plants
    n_centers: (int) number of distribution centers
    n_zones: (int) number of customer zones
    commodity_rates: ([float]) ordered list of commodity rates
    cost_pd: (dict) keys are tuples of the form (c,p,d) for a commodity, c, plant, p, and center, d.
        Value is the per unit cost of transporting c from p to d.
    cost_dz: (dict) keys are tuples of the form (d,z) for a commodity, c, center, d, and a zone, z.
        Value is the per unit cost of transporting c from d to z.
        
    Returns:
    
    m: (pyo.ConcreteModel) Model with the properties of a CFLP, including objective function, constraints, decision variables, and sets of indices.
        
    """
    
    m = pyo.ConcreteModel()

    m.C = pyo.RangeSet(0, n_commodities - 1)
    m.P = pyo.RangeSet(0, n_plants - 1)
    m.D = pyo.RangeSet(0, n_centers - 1)
    m.Z = pyo.RangeSet(0, n_zones - 1)

    #x_{c,p,d,z} = quantity of c shipped from p to d. Don't need to index by z, because each center ships to exactly one zone
    m.x = pyo.Var(m.C, m.P, m.D, domain = pyo.NonNegativeReals)

    #y_{d,z} = binary for whether d ships to z
    m.y = pyo.Var(m.D, m.Z, domain = pyo.Binary)

    #v_{d} = binary for whether d is opened
    m.v = pyo.Var(m.D, domain = pyo.Binary)

    def supply_rule(m, c, p):
        return sum(m.x[c,p,d] for d in m.D) <= Plant.plants[p].supply[c]
    m.supply = pyo.Constraint(m.C, m.P, rule = supply_rule)
    #for each commodity c, plant, p, total amount shipped is at most the supply of c to p

    def demand_rule(m, c, d):
        return (sum(m.x[c,p,d] for p in m.P) == sum(Cust_Zone.zones[z].demand[c] * m.y[d,z] for z in m.Z))
    m.demand = pyo.Constraint(m.C, m.D, rule = demand_rule)
    #for each commodity and distribution center, the amount of c shipped to d across all plants
    #must equal the demand for c across all zones, z, that d supplies to


    def min_throughput_rule(m, d):
        return (Dist_Center.centers[d].min_through * m.v[d] 
                <= sum(m.x[c,p,d] for c in m.C for p in m.P))
    m.min_throughput = pyo.Constraint(m.D, rule = min_throughput_rule)

    def max_throughput_rule(m, d):
        return (sum(m.x[c,p,d] for c in m.C for p in m.P)
        <= (Dist_Center.centers[d].max_through * m.v[d]))
    m.max_throughput = pyo.Constraint(m.D, rule = max_throughput_rule)
    #for each distribution center, the amount shipped must be within the minimum and maximum throughput
    #if that center was opened

    def allocation_rule(m, z):
        return sum(m.y[d,z] for d in m.D) == 1
    m.allocation = pyo.Constraint(m.Z, rule = allocation_rule)
    #Each customer zone receives shipments from exactly one distribution center

    def objective_fct(m):
        transp_cost = sum(cost_pd[c,p,d] * m.x[c,p,d] for c in m.C for p in m.P for d in m.D) + sum(cost_dz[c,d,z] * Cust_Zone.zones[z].demand[c] * m.y[d,z] for c in m.C for d in m.D for z in m.Z)
        center_cost = (sum(Dist_Center.centers[d].fixed_cost * m.v[d] for d in m.D) 
            + sum(Dist_Center.centers[d].var_cost * m.y[d,z] * Cust_Zone.zones[z].demand[c] for d in m.D for c in m.C for z in m.Z))
        return (transp_cost + center_cost)
    m.objective = pyo.Objective(rule = objective_fct, sense = pyo.minimize)

    return m