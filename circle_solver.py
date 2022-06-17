from gekko import GEKKO


pi = 3.1416
radius_of_circle = 5

# variables
m = GEKKO()
s, p = m.Array(m.Var,2,lb=1)
s.value = 1


# constraints
m.Equation( 1.4142 * s <= 2 * radius_of_circle )
 
# objective function
m.Minimize( pi * radius_of_circle * radius_of_circle - s * s )


m.solve(disp=False)
print(s.value)