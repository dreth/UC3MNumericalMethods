from gurobipy import *

# n is the number of projects

n = 5

projects = range(1, n+1) # list [1, ..., n] 

# objective coefficients (rewards)

r_coeff = [2, 5, 5, 1, 8] 

# left-hand side (LHS) coefficients (resource consumption)

A_coeff = [79, 53, 53, 45, 45]

# right-hand side (RHS) coefficient

b = 178 # resource budget

r = {j : r_coeff[j-1] for j in projects}

A = {j : A_coeff[j-1] for j in projects}

model = Model('kp1')

# uncomment next line for linear relaxation (continuous variables)
x = model.addVars(projects, name="x") 

# uncomment next line for binary variables
# x = model.addVars(projects, name="x", vtype=GRB.BINARY)

# uncomment next line for general integer variables
# x = model.addVars(projects, name="x", vtype=GRB.INTEGER)

# Capacity constraint
model.addConstr((quicksum(A[j] * x[j] for j in projects)
                           <= b))

# Variable upper bound constraints
model.addConstrs((x[j] <= 1 for j in projects))

# 1st valid inequality
model.addConstr(x[1]+x[2]+x[3] <= 2)

# 2nd valid inequality
model.addConstr(x[2]+x[3]+x[4]+x[5] <= 3)

# Objective
obj = quicksum(r[j] * x[j] for j in projects)

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


