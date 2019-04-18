from gurobipy import *

Arcs = [
    (0,2,100),
    (0,1,60),
    (0,1,60),
    (1,2,100),
    (2,3,80), (2,3,80),
    (3,5,20),
    (3,4,40), (3,4,40), (3,4,40), (3,4,40),
    (4,5,50), (4,5,50), (4,5,50),
    (5,0,75), (5,0,75)
]

Names = ["Line 1", "Line 2", "Line 3", "Line 4",
         "Unload 1", "Unload 2",
         "StockPile Bypass",
         "Stacker 1", "Stacker 2", "Stacker 3", "Stacker4",
         "Reclaimer 1", "Reclaimer 2", "Reclaimer 3",
         "Load 1", "Load2"]

Maintenance = [
    1, 1, 1, 1,
    1, 1,
    1,
    1, 1, 1, 1,
    1, 1, 1,
    1, 1
]

MAN_DAYS_PER_WEEK = 2

N = range(len(Names))
A = range(len(Arcs))
T = range(10)

m = Model("Coal Line Maintenance")

Y = [[m.addVar(vtype=GRB.BINARY) for a in A] for t in T]
X = [[m.addVar() for a in A] for t in T]

m.addConstrs(quicksum(X[t][a] for a in A if Arcs[a][0] == n) == quicksum(X[t][a] for a in A if Arcs[a][1] == n) for n in N for t in T)
m.addConstrs(quicksum(Y[t][a] * Maintenance[a] for a in A) <= MAN_DAYS_PER_WEEK for t in T)
m.addConstrs(quicksum(Y[t][a] for t in T) == 1 for a in A)
m.addConstrs(X[t][a] <= Arcs[a][2] * (1-Y[t][a]) for a in A for t in T)

m.setObjective(quicksum(X[t][-1] + X[t][-2] for t in T), GRB.MAXIMIZE)
m.optimize()

for t in T:
    print("\nMaximum flow for week", t, X[t][-1].x + X[t][-2].x)


    for a in A:
        if Y[t][a].x > 0.99:
            print("Maintenance performed on", Names[a])
        else:
            print(Names[a], "transported", X[t][a].x)