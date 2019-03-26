from gurobipy import *
from enum import Enum

class OptionTypes(Enum):
    Cars = 0
    Computers = 1
    Appliance = 2
    Insurance = 3
    Bonds = 4

    def max_option_type(self):
        if self.value == 0:
            return 30000
        if self.value == 1:
            return 30000
        if self.value == 2:
            return 20000

        return GRB.INFINITY

    def min_option_type(self):
        if self.value == 3:
            return 20000
        if self.value == 4:
            return 25000

        return 0


returns = [10.3, 10.1, 11.8, 11.4, 12.7, 12.2, 9.5, 9.9, 3.6, 4.2]
productOptions = [OptionTypes.Cars, OptionTypes.Cars, OptionTypes.Computers, OptionTypes.Computers,
                  OptionTypes.Appliance, OptionTypes.Appliance, OptionTypes.Insurance, OptionTypes.Insurance,
                  OptionTypes.Bonds, OptionTypes.Bonds]
P = range(10)

m = Model("Portfolio Optimisation")

products = [m.addVar() for p in P]

maxConstrs = m.addConstrs(quicksum(products[p] for p in P if option == productOptions[p]) <= option.max_option_type() for option in OptionTypes)
minConstrs = m.addConstrs(quicksum(products[p] for p in P if option == productOptions[p]) >= option.min_option_type() for option in OptionTypes)

# One off constraints
m.addConstr(products[8] >= 0.4 * products[9])
m.addConstr(products[0] + products[6] <= 50000)
m.addConstr(products[2] + products[7] <= 40000)

m.addConstr(quicksum(products[p] for p in P) <= 100000)

m.setObjective(quicksum(products[p] * (0.01 * returns[p]) for p in P), GRB.MAXIMIZE)
m.optimize()

for p in P:
    print(p+1, products[p].x)

print("\n -----------\n")
for c in maxConstrs:
    if c.max_option_type() < GRB.INFINITY:
        print(c.name, maxConstrs[c].RHS, maxConstrs[c].Slack, maxConstrs[c].Pi)

print("\n")

for c in minConstrs:
    if c.min_option_type() > 0:
        print(c.name, minConstrs[c].RHS, minConstrs[c].Slack, minConstrs[c].Pi)

