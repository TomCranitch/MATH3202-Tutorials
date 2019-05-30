from gurobipy import *

Ports = ['Manly','Cleveland','Dunwich']
Capacities = [8, 8, 6]
P = range(len(Ports))
B = range(18)

Travel = [
	[29, 27, 21], [39, 18, 30], [40, 20, 31], [33, 19, 27], [35, 29, 36], [21, 23, 20],
	[30, 41, 32], [37, 27, 36], [20, 25, 34], [36, 28, 20], [24, 23, 25], [38, 22, 40], 
	[39, 19, 27], [30, 18, 28], [40, 20, 32], [21, 32, 40], [23, 18, 20], [31, 18, 20]
]

m = Model("Boats")

X = [[m.addVar(vtype=GRB.BINARY) for p in P] for b in B]
MAX = m.addVar()

m.addConstrs(quicksum(X[b][p] for p in P) == 1 for b in B)
m.addConstrs(quicksum(X[b][p] for b in B) <= Capacities[p] for p in P)

m.addConstrs(MAX >= (Travel[b][p] * X[b][p]) for b in B for p in P)

m.setObjective(MAX, GRB.MINIMIZE)
m.optimize()
