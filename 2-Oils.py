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

# Data
costs = [110, 120, 130, 110, 115]
hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
types = [OilTypes.VEG, OilTypes.VEG, OilTypes.NON_VEG, OilTypes.NON_VEG, OilTypes.NON_VEG]
oils = ['Veg1', 'Veg2', 'Oil1', 'Oil2', 'Oil3']

# Setup model and variables
m = Model("Blending Problem")

O = range(len(oils))

Q = {o: m.addVar() for o in O}

# Setup Constraints
m.addConstrs(quicksum(Q[o] for o in O if types[o] == oilType) <= oilType.max_type() for oilType in OilTypes)
m.addConstr(quicksum(Q[o]*hardness[o] for o in O) >= MIN_HARDNESS*quicksum(Q[o] for o in O))
m.addConstr(quicksum(Q[o]*hardness[o] for o in O) <= MAX_HARDNESS*quicksum(Q[o] for o in O))

# Optimise and print the solution
m.setObjective(quicksum((150 - costs[o])*Q[o] for o in O), GRB.MAXIMIZE)
m.optimize()

for o in O:
    print(oils[o], " ", Q[o].x)

