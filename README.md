# Capacitated-Facility-Location-Problem
The CFLP is an optimization problem involving distribution center design. Given a set of proposed production plants, distribution centers (facilities), customer zones, and commodities, the goal is to minimize total cost by selecting which distribution centers to open, what customer zones they should serve, and the amount of each commodity to transport from production plant to distribution center, then to customer zone. Below is a diagram summarizing the transportation layout.

<img width="409" height="377" alt="CFLP_Layout2" src="https://github.com/user-attachments/assets/fd5e9110-9b28-46fb-a396-f61096bd1e83" />

## Model and constraints

We'll now give an explicit mathematical formulation for the problem: variables, constraints, and objective function.

### Variables

| Variable | Type | Description |
|:---------|:-----|:------------|
| c |Index | Commodity |
| p | Index | Production Plant |
| d | Index | Distribution Center |
| z | Index | Customer Zone |
| x<sub>cpdz</sub> | Decision Variable | Amount of commodity c sent from production plant p to distribution center d, then to customer zone z |
| v<sub>d</sub> | Binary Decision Variable | Whether distribution center d is opened |
| y<sub>dz</sub> | Binary Decision Variable | Whether distribution center d ships to customer zone z |
| S<sub>cp</sub> | Parameter | Supply of commodity c available at production plant p |
| D<sub>cz</sub> | Parameter | Demand for commodity c at customer zone z |
| m<sub>d</sub> | Parameter | Minimum throughput of distribution center d |
| M<sub>d</sub> | Parameter | Maximum throughput of distribution center d |
| F<sub>d</sub> | Parameter | Fixed cost of operating distribution center d |
| R<sub>d</sub> | Parameter | Variable cost of distribution center d (per unit throughout charge) |
| K<sub>cpdz</sub> | Parameter (Calculated) | Per unit cost of producing c, then shipping from p to d, d to z |

### Constraints

(1) Supply

$$
\sum_{d,z} x_{cpdz} \leq S_{cp}
$$





### Constraints:

### Objective:

# Acknowledgements
- Model from AIMMS Optimization Modeling [AIMMS](https://documentation.aimms.com/_downloads/AIMMS_modeling.pdf)
