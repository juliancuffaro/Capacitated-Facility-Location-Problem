# Capacitated-Facility-Location-Problem
The CFLP is an optimization problem involving distribution center design. Given a set of proposed production plants, distribution centers (facilities), customer zones, and commodities, the goal is to minimize total cost by selecting which distribution centers to open, what customer zones they should serve, and the amount of each commodity to transport from production plant to distribution center, then to customer zone. Below is a diagram summarizing the transportation layout.

<img width="409" height="377" alt="CFLP_Layout2" src="https://github.com/user-attachments/assets/fd5e9110-9b28-46fb-a396-f61096bd1e83" />

## Requirements and Setup

### Requirements

- Python 3.12 or newer (developed and tested on Python 3.14)
- The packages listed in `requirements.txt`:
  - [Pyomo](https://www.pyomo.org/): builds the optimization model
  - [HiGHS](https://highs.dev/) (via `highspy`): solves the mixed-integer program
  - [pandas](https://pandas.pydata.org/): reads CSVs and wrangles data

### Installation

### Requirements
- Python 3.12 or newer (tested on Python 3.14)
- Dependencies are declared in `pyproject.toml` and installed automatically:
  Pyomo, HiGHS (`highspy`), pandas

### Installation
1. Clone the repository and enter it:
```
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
```
2. Create and activate a virtual environment:
```
   py -m venv .venv                 # Windows (or: python -m venv .venv)
   .venv\Scripts\activate           # Windows
   source .venv/bin/activate        # macOS / Linux
```
   On Windows, if activation is blocked, run
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.
3. Install the project in editable mode:
```
   pip install -e .
```
4. Verify the install:
```
   python -c "import pyomo.environ as pyo, pandas, common.datatypes; print(pyo.SolverFactory('appsi_highs').available())"
```
   This should print `True`.

### Project layout
```
common/              shared data classes and distance functions
CFLP_Single/         single solve
CFLP_Sensitivity/    parametric analysis on commodity rates
CSVs/                input data
Output/              results
```
   This should print `True`.

### Input data

All inputs are CSV files in the `CSVs/` folder:

| File | Contents |
|---|---|
| `distribution_centers.csv` | min/max throughput, fixed cost, variable cost, latitude, longitude for each distribution center |
| `customer_zones.csv` | demand for each commodity, latitude, longitude |
| `production_plants.csv` | supply of each commodity, latitude, longitude |
| `commodity_rates.csv` | transport cost per unit per km for each commodity |

Row order matters: row *i* in each file is entity *i* in the model, and commodity columns must appear in the same order in all three files. To use your own data, replace these files with the same column layout.

### Running

- Single solve: `python main.py`
- Parametric analysis on commodity rates: `python Parametric_Analysis.py`

Output is written to the `Output/` folder:
- `main.py`  writes to `Output/main_out.txt`
- `Parametric_Analysis.py` writes to `Output/parametric_out.txt`

### Configuration

Distance settings are constants near the top of the code:

- `CIRCUITY`: multiplier applied to straight-line distance to approximate road distance
- `EARTH_RADIUS`: 6371 km (haversine distance)


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
| $K_{cpdz}$ | Parameter (Calculated) | Cost of producing c, then shipping from p to d, d to z per unit per km |

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

- Commodity amounts are assumed to be integers (for rounding simplicity)
- Demand is deterministic
- Each customer zone is served by only one distribution center
- We do not model any transportation capacity limits
- Per unit transportation cost are generalized to "commodity rates"
- Distances are calculated using haversine distance, and do not account for actual roads/routing

# Acknowledgements
- Model formulated in AIMMS Optimization Modeling [AIMMS](https://documentation.aimms.com/_downloads/AIMMS_modeling.pdf)
