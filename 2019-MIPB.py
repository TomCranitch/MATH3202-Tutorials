from gurobipy import *

Factories = range(10)
Customers = range(20)

Build = [1204, 1757, 1357, 1519, 1785, 1959, 1597, 1683, 1219, 1373]
Assign = [
    [683, 811, 585, 769, 836, 942, 914, 548, 829, 719],
    [580, 869, 722, 972, 635, 957, 992, 787, 564, 528],
    [765, 966, 538, 852, 543, 912, 686, 710, 889, 951],
    [853, 716, 926, 705, 617, 882, 853, 992, 749, 533],
    [853, 815, 679, 803, 833, 618, 889, 560, 752, 806],
    [568, 567, 911, 532, 662, 663, 891, 917, 675, 768],
    [731, 511, 975, 874, 522, 781, 963, 502, 613, 695],
    [632, 967, 687, 570, 802, 652, 766, 982, 658, 548],
    [712, 670, 982, 880, 730, 974, 697, 648, 808, 995],
    [719, 806, 999, 720, 907, 800, 769, 804, 916, 853],
    [712, 597, 998, 527, 715, 647, 897, 833, 839, 689],
    [867, 552, 519, 522, 776, 776, 771, 585, 913, 850],
    [875, 567, 728, 880, 595, 518, 797, 788, 664, 560],
    [536, 760, 733, 503, 531, 904, 598, 891, 983, 908],
    [757, 548, 967, 585, 615, 508, 978, 793, 998, 970],
    [696, 754, 999, 565, 841, 717, 542, 719, 962, 574],
    [778, 715, 866, 713, 651, 809, 591, 513, 864, 953],
    [513, 832, 925, 887, 583, 590, 907, 981, 636, 983],
    [835, 942, 945, 868, 904, 905, 852, 751, 689, 748],
    [714, 985, 724, 721, 655, 964, 901, 726, 701, 977]
]

m = Model("BigCorp Factory Assignment")

X = [m.addVar(vtype=GRB.BINARY) for f in Factories]
Y = [[m.addVar(vtype=GRB.BINARY) for f in Factories] for c in Customers]
Z = [m.addVar(vtype=GRB.BINARY) for f in Factories]

m.addConstrs(Y[c][f] <= X[f] + Z[f] for f in Factories for c in Customers)
m.addConstrs(quicksum(Y[c][f] for f in Factories) == 1 for c in Customers)
m.addConstrs(quicksum(Y[c][f] for c in Customers) <= 6*(1-Z[f]) + 8*Z[f] for f in Factories)
m.addConstrs(Z[f] + X[f] <= 1 for f in Factories)

m.setObjective(quicksum(1.5 * Build[f] * Z[f] for f in Factories) + quicksum(Build[f] * X[f] for f in Factories) + quicksum(Assign[c][f] * Y[c][f] for c in Customers for f in Factories), GRB.MINIMIZE)
m.optimize()


print("\n\n\033[1m Solution Prepared for 2019 MATH3202 Practical Exam Question 1(b). Minimum combined assignment and build cost is $" + str(m.objVal) + "\033[0m.\n\n")

for f in Factories:
    if X[f].x > 0:
        print("Factory", f, "is built at the smaller size. It is assigned the following customers:")
        print(', '.join(map(str, [c for c in Customers if Y[c][f].x > 0])))

    if Z[f].x > 0:
        print("Factory", f, "is built at the larger size. It is assigned the following customers:")
        print(', '.join(map(str, [c for c in Customers if Y[c][f].x > 0])))
