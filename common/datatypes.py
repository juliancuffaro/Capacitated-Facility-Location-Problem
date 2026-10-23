import pandas as pd
import math

EARTH_RADIUS = 6371 #km
CIRCUITY = 1.0 #1.3 #assumed circuity factor


#locations must be given in the form (lat, long)
def hav_dist(loc_1, loc_2): #haversine distance

    phi_1 = math.radians(loc_1[0])
    phi_2 = math.radians(loc_2[0])
    lambda_1 = math.radians(loc_1[1])
    lambda_2 = math.radians(loc_2[1])
    
    a = pow(math.sin((phi_2 - phi_1) / 2), 2) + math.cos(phi_1) * \
    math.cos(phi_2) * pow(math.sin((lambda_2 - lambda_1) / 2),2)
    
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    d = EARTH_RADIUS * c
    return d

def dist(loc_1, loc_2): #planar distance
    d = math.sqrt( math.pow((loc_1[0] - loc_2[0]), 2) + math.pow((loc_1[1] - loc_2[1]), 2) )
    return d

class Dist_Center:
    """
    Represents a distribution center

    Class attributes:
    centers: (Dist_Center []) The element at index i is the Dist_Center with ID number i


    Instance attributes:
    min_through: (float) Minimum units of throughput for the distribution center
    max_through: (float) Maximum units of throughput for the distribution center
    fixed_cost: (float) fixed cost of opening this distribution center
    var_cost: (float) per unit throughput charge of the distribution center
    loc: (float, float) latitude and longitude of the center
    ID: (int)  identifies the center 
    """
    centers = []

    def __init__(self, min_through, max_through, fixed_cost, var_cost, loc):

        self.ID = len(Dist_Center.centers)
        if (min_through > max_through):
            raise ValueError(f"Minimum throughput must be at most maximum throughput for distribution center {self.ID}.")

        self.min_through = min_through
        self.max_through = max_through
        self.fixed_cost = fixed_cost
        self.var_cost = var_cost
        self.loc = loc

        Dist_Center.centers.append(self)

    @staticmethod
    def clear_centers():
        (Dist_Center.centers).clear()
    #After optimization complete, clear data

    @staticmethod
    def csv_to_centers(csv):
        """
        Parses csv into distribution centers, automatically appended to the list of distribution centers, Dist_Center.centers
        
        Args:
            csv: (str) path to csv file of form specified in CSV file

        Returns: none
        """
        df = pd.read_csv(csv)
        for row in df.itertuples(): 
            Dist_Center(row.min_through, row.max_through, row.fixed_cost, row.var_cost, (row.lat, row.long))

class Cust_Zone:
    """
    Represents a zone from which customers are placing orders

    Class attributes:
    zones: (Cust_Zone []) The element at index i is the Cust_Zone with ID number i

    Instance attributes:
    demand: (float  []) element at index i represents the demand for commodity i of the Cust_Zone
    loc: (float, float) latitude and longitude of the zone
    ID: (int) identifies the customer zone
    """

    zones = []

    def __init__(self, demand, loc): #note: we'll parse the customer zones csv into demand: a list integers, each representing the demand for a certain commodity. That commodity is represented by its index in the list

        self.ID = len(Cust_Zone.zones)

        for i in range(len(demand)):
            if demand[i] < 0:
                raise ValueError(f"Demand for commodity {i} must be non-negative in Customer Zone {self.ID}.")

        
        self.demand = list(demand)
        self.loc = loc

        Cust_Zone.zones.append(self)

    @staticmethod
    def clear_zones():
        (Cust_Zone.zones).clear()

    @staticmethod
    def csv_to_zones(csv):
        """
        Parses csv into customer zones, automatically appended to the list of customer zones, Cust_Zone.zones
                
        Args:
            csv: (str) path to csv file of form specified in CSV file
        
        Returns: none
        """
        df = pd.read_csv(csv)

        commodity_columns = []
        for c in df.columns:
            if c not in ("lat", "long"):
                commodity_columns.append(c)
                #commodity_columns = ["demand_1", "demand_2", etc.]

        for _, row in df.iterrows():
            demand = []
            for col in commodity_columns:
                demand.append(row[col]) 
                #demand = [120, 45, 0, etc.]
            Cust_Zone(demand, (row["lat"], row["long"]))

class Plant:
    """
    Represents a production plant, which ships commodities to distribution centers

    Class attributes:
   
    plants: (Plant []) The element at index i is the Plant with ID number i

    Instance attributes:
    supply: (float []) element at index i represents the supply of commodity i given by the Plant
    loc: (float, float) latitude and longitude of the Plant
    ID: (int) identifies the Plant 
    """

    plants = []

    def __init__(self, supply, loc):

        self.ID = len(Plant.plants)

        for i in range(len(supply)):
            if supply[i] < 0:
                raise ValueError(f"Supply of product {i} must be non-negative for Production Plant {self.ID}")

        self.supply = list(supply)
        self.loc = loc

        Plant.plants.append(self)

    @staticmethod
    def clear_plants():
        (Plant.plants).clear()

    @staticmethod
    def csv_to_plants(csv):
        """
        Parses csv into production plants, automatically appended to the list of production plants, Plant.plants            
        
        Args:
            csv: (str) path to csv file of form specified in CSV file
    
        Returns: none
        """
        df = pd.read_csv(csv)

        commodity_columns = []
        for c in df.columns:
            if c not in ("lat", "long"):
                commodity_columns.append(c)

        for _, row in df.iterrows():
            supply = []
            for col in commodity_columns:
                supply.append(row[col])
            Plant(supply, (row["lat"], row["long"]))