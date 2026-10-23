# Capacitated-Facility-Location-Problem
The CFLP is an optimization problem involving distribution center design. Given a set of proposed production plants, distribution centers (facilities), customer zones, and commodities, the goal is to minimize total cost by selecting which distribution centers to open, what customer zones they should serve, and the amount of each commodity to transport from production plant to distribution center, then to customer zone. Below is a diagram summarizing the transportation layout.

<img width="409" height="377" alt="CFLP_Layout2" src="https://github.com/user-attachments/assets/fd5e9110-9b28-46fb-a396-f61096bd1e83" />

## Requirements and Setup

**Requirements**


## Repository Format

There are two components to this project: optimization of the model using the given data, and a parametric analysis on commodity rates, which optimizes the model for the given commodity rates, and for re-scaled commodity rates with scale decided by the user. In either case, inputs are taken from four CSV files, each detailing a different portion of the data required (commodities, production plants, distribution centers, and customer zones). The commodity rates CSV is parsed into a one-dimensional array for simplicity, and the remaining three are parsed into corresponding data-types that are defined within the program. The Python library Pandas is used for all data parsing and wrangling. Optimization is done by Pyomo using the 'highs' solver for the single optimization, and 'appsi_highs' is used for the sensitivity analysis, as it allows for mutability of commodity rates.
NOT FINISHEDWWWWWWWWWWWWWWWWWWWWWW

## Model and constraints

We'll now give an explicit mathematical formulation for the problem: variables, constraints, and objective function.

### Variables

| Variable | Type | Description |
|:---------|:-----|:------------|
| $c$ |Index | Commodity |
| $p$ | Index | Production Plant |
| $d$ | Index | Distribution Center |
| $z$ | Index | Customer Zone |
| $x_{cpdz}$ | Decision Variable | Amount of commodity c sent from production plant p to distribution center d, then to customer zone z |
| $v_{d}$ | Binary Decision Variable | Whether distribution center d is opened |
| $y_{dz}$ | Binary Decision Variable | Whether distribution center d ships to customer zone z |
| $S_{cp}$ | Parameter | Supply of commodity c available at production plant p |
| $D_{cz}$ | Parameter | Demand for commodity c at customer zone z |
| $m_{d}$ | Parameter | Minimum throughput of distribution center d |
| $M_{d}$ | Parameter | Maximum throughput of distribution center d |
| $F_{d}$ | Parameter | Fixed cost of operating distribution center d |
| $R_{d}$ | Parameter | Variable cost of distribution center d (per unit throughout charge) |
| $K_{cpdz}$ | Parameter (Calculated) | Per unit cost of producing c, then shipping from p to d, d to z |

### Constraints

#### (1) Supply

$$
\sum_{d,z} x_{cpdz} \leq S_{cp} \qquad \forall c, p
$$

For any given commodity and production plant, the amount shipped cannot exceed the plant's available supply.

#### (2) Demand

$$
\sum_{p} x_{cpdz} \geq D_{cz} y_{dz} \qquad \forall c, d, z
$$

For a given commodity, distribution center, and customer zone, if the center ships to the zone, the total amount delivered must meet the zone's demand.

#### (3) Throughput

$$
m_{d} v_{d} \leq \sum_{c,p,z} x_{cpdz} \leq M_{d} v_{d} \qquad \forall d
$$

Every distribution center must operate within its minimum and maximum throughput (and can only handle flow if it is open).

#### (4) Allocation

$$
\sum_{d} y_{dz} = 1 \qquad \forall z
$$

Every customer zone is served by exactly one distribution center.

### Objective

Minimize total cost:

$$
\sum_{c,p,d,z} K_{cpdz} x_{cpdz} + \sum_{d} \left( F_{d} v_{d} + R_{d} \sum_{c,z} D_{cz} y_{dz} \right)
$$

This covers production and shipping costs, plus each open distribution center's fixed cost and variable cost (per-unit throughput charge). We minimize with respect to our decision variables, $v_d$, $x_{cpdz}$, and $y_{dz}$.

### Assumptions and Limitations

- Demand is deterministic
- Each customer zone is served by only one distribution center
- We do not model any transportation capacity limits
- Per unit transportation cost are generalized to "commodity rates"
- Distances are calculated using haversine distance, and do not account for actual roads/routing

# Acknowledgements
- Model from AIMMS Optimization Modeling [AIMMS](https://documentation.aimms.com/_downloads/AIMMS_modeling.pdf)
