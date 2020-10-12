from gurobipy import *

m = 3  # number of resources

n = 8  # number of products

resources = range(m)  # list [1, ..., m]

products = range(n)  # list [1, ..., n]

# primal objective coefficients

r_coeff = [16.0, 31.0, 4.0, 30.0, 68.0, 0.0, 0.0, 0.0]

# left-hand side (LHS) coefficients (matrix A)

A_coeff = [[20.0, 14.0, 13.0,  7.0, 19.0, 1.0, 0.0, 0.0],
           [15.0,  4.0, 12.0, 13.0, 12.0, 0.0, 1.0, 0.0],
           [4.0,  18.0, 2.0,  9.0,  6.0, 0.0, 0.0, 1.0]]

# right-hand side (RHS) coefficients

b_coeff = [96.0, 59.0, 82.0]

r = {j: r_coeff[j] for j in products}

A = {i: {j: A_coeff[i][j] for j in products}
     for i in resources}

b = {i: b_coeff[i] for i in resources}

model = Model('lpex1')

x = model.addVars(products, name="x")  # quantity produced

# Constraints
model.addConstrs((quicksum(A[i][j] * x[j] for j in products)
                  == b[i]
                  for i in resources), name="pi")

# Objective
obj = quicksum(r[j] * x[j] for j in products)

model.setObjective(obj, GRB.MAXIMIZE)

model.optimize()


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

print('Variable Information Including Sensitivity Information:')

# tVars = PrettyTable(['Variable Name', ' Value', 'ReducedCost',
#                     ' SensLow', ' SensUp'])  #column headers

for v in model.getVars():
    print("%s %s %8.2f %s %8.2f %s %8.2f %s %8.2f" %
          (v.Varname, "=", v.X, ", reduced cost = ", abs(v.RC), ", from coeff = ", v.SAObjLow, "to coeff = ", v.SAObjUp))
    print(" ")


print('\nOptimal objective value: %g' % model.objVal)

print('\nOptimal shadow prices:\n')
for c in model.getConstrs():
    print("%s %s %8.2f %s %8.2f %s %8.2f" % (c.ConstrName, ": shadow price = ",
                                             c.Pi, ", from RHS = ", c.SARHSLow, "to RHS = ", c.SARHSUp))
    print(" ")
