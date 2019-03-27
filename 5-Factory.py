from gurobipy import *

# Set up your data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit))

n = [4, 2, 3, 1, 1]
M = range(len(n))

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
]

T = range(6)

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
]

# market[P][T]
market = [
    [ 500, 600, 300, 200,   0, 500],
    [1000, 500, 600, 300, 100, 500],
    [ 300, 200,   0, 400, 500, 100],
    [ 300,   0,   0, 500, 100, 300],
    [ 800, 400, 500, 200,1000,1100],
    [ 200, 300, 400,   0, 300, 500],
    [ 100, 150, 100, 100,   0,  60]
]

MAX_STORE = 100
STORE_COST = 0.5
FINAL_STORE = 50
MONTH_HOURS = 16*24

mod = Model("Factory Planning")

X = [[mod.addVar(vtype=GRB.INTEGER) for t in T] for p in P]
Y = [[mod.addVar(vtype=GRB.INTEGER, ub=market[p][t]) for t in T] for p in P]
S = [[mod.addVar(vtype=GRB.INTEGER, ub=MAX_STORE) for t in T] for p in P]

Z = [[mod.addVar(vtype=GRB.INTEGER) for m in M] for t in T]

mod.addConstrs((quicksum(usage[p][m] * X[p][t] for p in P) <= MONTH_HOURS*(n[m] - Z[t][m]) for m in M for t in T))
mod.addConstrs(S[p][t] == S[p][t-1] + X[p][t] - Y[p][t] for p in P for t in T if t > 1)
mod.addConstrs(S[p][t] <= MAX_STORE for p in P for t in T)
mod.addConstrs(S[p][-1] >= FINAL_STORE for p in P)
mod.addConstrs(S[p][0] == X[p][0] - Y[p][0] for p in P)

mod.addConstrs(quicksum(Z[t][m] for t in T) == sum(maint[t][m] for t in T) for m in M)

mod.setObjective(quicksum(profit[p]*Y[p][t] for p in P for t in T) - quicksum(STORE_COST*S[p][t] for p in P for t in T), GRB.MAXIMIZE)
mod.optimize()

print("\n\n Report Prepared for Factory Planing\n Optimal Cost", mod.objVal, "\n\n")

for p in P:
    print([X[p][t].x for t in T])

print("\n\n Sell \n")
for p in P:
    print([Y[p][t].x for t in T])

print("\n\n Storage \n")
for p in P:
    print([S[p][t].x for t in T])

print("\n\n Maintainence \n")
for m in M:
    print([Z[t][m].x for t in T])
