from gurobipy import *
import random

# Data and ranges
nHospitalSites = 30
nSuburbs = 55
MaxSuburbsPerHospital = 6
MaxPopulation = 500000

H = range(nHospitalSites)
S = range(nSuburbs)

random.seed(3)

FixedCost = [random.randint(5000000,10000000) for h in H]
Population = [random.randint(60000,90000) for s in S]

# Travel distance - multiply by population moved to get travel cost
Dist = [[random.randint(0,50) for s in S] for h in H]

# Set up model and set the gap on the answer to 0
m = Model()
m.setParam('MIPGap', 0)

x = [m.addVar(vtype=GRB.BINARY) for h in H]
y = [[m.addVar(vtype=GRB.BINARY) for s in S] for h in H]

m.addConstrs(y[h][s] <= x[h] for h in H for s in S)
m.addConstrs(quicksum(y[h][s] for s in S) <= MaxSuburbsPerHospital for h in H)
m.addConstrs(quicksum(Population[s] * y[h][s] for s in S) <= MaxPopulation for h in H)
m.addConstrs(quicksum(y[h][s] for h in H) == 1 for s in S)

m.setObjective(quicksum(y[h][s]*Population[s]*Dist[h][s] + FixedCost[h]*x[h] for h in H for s in S), GRB.MINIMIZE)
m.optimize()

print("\n\n\033[1m Report Prepared for 2016 MATH3202 Practical Exam. Minimum cost is $" + str(m.objVal) + ".\033[0m")

for h in H:
    if x[h].x > 0:
        print("Hospital", h)
        print(', '.join(map(str, [s for s in S if y[h][s].x > 0])))

for h in H:
    if x[h].x > 0:
        for s in S:
            print()

