# Implementation of min cost flow model
#
# created by Jose Niño Mora

from gurobipy import *

 # Model data

nodes, supply = multidict({
         1:  1,
         2:  0,
         3:  0,
         4: 0,
         5: 0,
         6: -1})
 
arcs, cost, locap, upcap = multidict({
    (1, 2): [3, 0, 1000],
    (1, 3): [4, 0, 1000],
    (1, 4): [1, 0,  80],
    (2, 3): [5, 0, 1000],
    (2, 5): [6, 0, 1000],
    (3, 4): [1, 0, 120],
    (3, 5): [2, 0, 1000],
    (4, 6): [2, 0, 120],
    (5, 6): [4, 0, 1000]})
 
 # Create optimization model
 
m = Model('minCostFlow')
 
 # Create variables
 
flow = m.addVars(arcs, obj=cost, name="flow")
 
# Flow balance constraints
m.addConstrs(
         (flow.sum(i, '*') - flow.sum('*', i) == supply[i] for i in nodes), "supply")
 
# Lower arc capacity constraints
m.addConstrs(
         (flow[i, j] >= locap[i, j] for i, j in arcs if locap[i, j] != 0), "lowCap")
 
# Upper arc capacity constraints
m.addConstrs(
         (flow[i, j] <= upcap[i, j] for i, j in arcs), "upCap")
 
# model.setObjective(obj, GRB.MINIMIZE)

m.ModelSense=GRB.MINIMIZE

 # Compute optimal solution
m.optimize()
 
 # Print solution
 
print('\nVariable Information Including Sensitivity Information:\n')

for v in m.getVars():
    print("%s %s %8.2f %s %8.2f %s %8.2f %s %8.2f" % 
              (v.Varname, "=", v.X, ", reduced cost = ", abs(v.RC), ", from coeff = ", v.SAObjLow, "to coeff = ", v.SAObjUp))
    print(" ")
        
        
print('\nOptimal objective value: %g' % m.objVal)

print('\nOptimal shadow prices:\n')
for c in m.getConstrs():
        print("%s %s %8.2f %s %8.2f %s %8.2f" % (c.ConstrName, ": shadow price = ", c.Pi, ", from RHS = ", c.SARHSLow, "to RHS = ", c.SARHSUp))
        print(" ")