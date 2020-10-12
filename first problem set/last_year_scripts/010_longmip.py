from gurobipy import *

n = 21 # there are n binary variables and 1 continuous variable

zeroton = range(n+1)   # list [0, ..., n]
oneton = range(1, n+1) # list [1, ..., n]

model = Model('longmip')

x0 = model.addVar(name="x0") 

# uncomment next line for linear relaxation (continuous variables)
# x = model.addVars(oneton, name="x") 

# uncomment next line for binary variables
#x = model.addVars(oneton, name="x", vtype=GRB.BINARY)

# uncomment next line for general integer variables
x = model.addVars(oneton, name="x", vtype=GRB.INTEGER)

# Capacity constraints
model.addConstr((x0 + 2*quicksum(x[j] for j in oneton)
                           <= n))
# Variable upper bound constraints
model.addConstrs((x[j] <= 1 for j in oneton))

# Objective
obj = -x0 + 2*quicksum(x[j] for j in oneton)

model.setObjective(obj, GRB.MAXIMIZE)

# disable Presolve
model.setParam(GRB.Param.Presolve, 0)
# disable Heuristics
model.setParam(GRB.Param.Heuristics, 0)
# disable Cuts
model.setParam(GRB.Param.Cuts, 0)
        
model.optimize()


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

print('Variable Information:')
                 
for v in model.getVars():
    print("%s %s %8.2f" % 
              (v.Varname, "=", v.X))
    
    print(" ")
        
print('\nOptimal objective value: %g' % model.objVal)
