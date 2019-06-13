from gurobipy import *

compartments = ['A', 'B', 'C', 'D']

w = [70, 90, 100, 110, 120, 130, 150, 180, 210, 220, 250, 280, 340, 350, 400]
MinPackages = 3
MaxWeight = 1000

C = range(len(compartments))
P = range(len(w))

m = Model("Payload")

X = [[m.addVar(vtype=GRB.BINARY) for c in C] for p in P]

m.addConstr(quicksum(w[p] * X[p][0] for p in P) == quicksum(w[p] * X[p][3] for p in P))
m.addConstr(quicksum(w[p] * X[p][1] for p in P) == quicksum(w[p] * X[p][2] for p in P))

m.addConstrs(quicksum(w[p]*X[p][c] for p in P) <= MaxWeight for c in C)
m.addConstrs(quicksum(X[p][c] for p in P) >= MinPackages for c in C)
m.addConstrs(quicksum(X[p][c] for c in C) == 1 for p in P)

m.optimize()

for c in C:
    print("Compartment", compartments[c])

    for p in P:
        if X[p][c].x > 0:
            print(w[p], end=', ')

    print("")
