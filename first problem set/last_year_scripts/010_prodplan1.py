from gurobipy import *

products = ["Prod1", "Prod2"]
resources = ["M1", "M2"]

profit_contribution = {"Prod1":5.0, "Prod2":4.0}

technology_matrix = {
    "M1": {    "Prod1": 6.0, "Prod2": 4.0 },
    "M2": {    "Prod1": 1.0, "Prod2": 2.0 }
}


# resource availability

qResource = {"M1":24.0, "M2":6.0} 

P2upper = 2.0
smoothingDiff = 1.0

model = Model('prodplan1')

x = model.addVars(products, name="x") # quantity manufactured

# Resource capacity constraints
model.addConstrs((quicksum(technology_matrix[resource][product] * x[product] for product in products)
                           <= qResource[resource] 
                            for resource in resources), name = "Capacity")


model.addConstr(x['Prod2'] <= P2upper, 'P2')

model.addConstr(x['Prod2']-x['Prod1'] <= smoothingDiff, 'D')



# Objective
obj = quicksum(profit_contribution[product] * x[product] for product in products)

model.setObjective(obj, GRB.MAXIMIZE)
      
    
        
model.optimize()


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

for v in model.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
        
        
print('\nOptimal objective value: %g' % model.objVal)

print('\nOptimal shadow prices:\n')
for c in model.getConstrs():
        print("%s %f" % (c.ConstrName, c.Pi))


