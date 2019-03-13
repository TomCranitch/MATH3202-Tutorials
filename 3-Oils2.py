from gurobipy import *
from enum import Enum


# Enum for the types of oil
class OilTypes(Enum):
    VEG = 0
    NON_VEG = 1

    def max_type(self):
        if self.value == 0:
            return 200
        else:
            return 250


# Constants
MIN_HARDNESS = 3
MAX_HARDNESS = 6
SALE_PRICE = 150
STORE_MAX = 1000
STORE_COST = 5
INITIAL = 500

# Data
costs = [
    [110, 120, 130, 110, 115],
    [130, 130, 110, 90, 115],
    [110, 140, 130, 100, 95],
    [120, 110, 120, 120, 125],
    [100, 120, 150, 110, 105],
    [90, 100, 140, 80, 135]
]
hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
types = [OilTypes.VEG, OilTypes.VEG, OilTypes.NON_VEG, OilTypes.NON_VEG, OilTypes.NON_VEG]
oils = ['Veg1', 'Veg2', 'Oil1', 'Oil2', 'Oil3']
O = range(len(oils))
M = range(6)

# Setup model and variables
model = Model("Blending Problem")

Q = [[model.addVar() for o in O] for m in M]
B = [[model.addVar() for o in O] for m in M]
S = [[model.addVar() for o in O] for m in M]

# Setup Constraints
model.addConstrs(quicksum(Q[m][o] for o in O if types[o] == oilType) <= oilType.max_type() for oilType in OilTypes for m in M)
model.addConstrs(quicksum((hardness[o] - MIN_HARDNESS) * Q[m][o] for o in O) >= 0 for m in M)
model.addConstrs(quicksum((hardness[o] - MAX_HARDNESS) * Q[m][o] for o in O) <= 0 for m in M)
model.addConstrs(S[m][o] <= STORE_MAX for o in O for m in M)
model.addConstrs(S[0][o] == INITIAL - Q[0][o] + B[0][o] for o in O)
model.addConstrs(S[m][o] == S[m-1][o] - Q[m][o] + B[m][o] for o in O for m in M[1:])

# Optimise and print the solution
model.setObjective(quicksum(SALE_PRICE * Q[m][o] for o in O for m in M)
                   - quicksum(costs[m][o] * B[m][o] for o in O for m in M)
                   - quicksum(STORE_COST * S[m][o] for o in O for m in M), GRB.MAXIMIZE)
model.optimize()

for m in M:
    print('\n Month ', m)
    for o in O:
        print('For ', oils[o], ' bought ', B[m][o].x, ' and used ', Q[m][o].x, ' leaving ', S[m][o].x)
