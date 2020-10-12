# Implementation of the transportation model
#
# created by Jose Niño Mora

from gurobipy import *

 # Model data

origins, supply = multidict({
         'LA': 1000,
         'Detroit': 1500,
         'New Orleans': 1200 })
 
destinations, demand = multidict({
         'Denver': 2299,
         'Miami': 1400 })
 
arcs, cost = multidict({
    ('LA', 'Denver'):           80,
    ('LA', 'Miami'):           215,
    ('Detroit', 'Denver'):     100,
    ('Detroit', 'Miami'):      108,
    ('New Orleans', 'Denver'): 102,
    ('New Orleans', 'Miami'):   68 })
 
 # Create optimization model
 
m = Model('transp')
 
 # Create variables
 
flow = m.addVars(arcs, obj=cost, name="flow")
 
# flow = m.addVars(arcs, name="flow")
 
 # Origin supply constraints
m.addConstrs(
         (flow.sum(i, '*') <= supply[i] for i in origins), "supply")
 
 # Destination demand constraints
m.addConstrs(
         (flow.sum('*', j) >= demand[j] for j in destinations), "demand")
 


# m.setObjective(obj, GRB.MINIMIZE)

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
             
             
 



