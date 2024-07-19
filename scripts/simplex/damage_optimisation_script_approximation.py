import numpy as np
import scipy as sc
from two_phase_simplex import TwoPhaseSimplex

def _get_scales_list(scalings : list[str]) -> list[float]:
    """Gets the list of float damage scales for the weapon given"""
    scalings_copy = []
    # translate scalings to floats
    scaling_dict = {"S" : 1.7, "A" : 1.195, "B" : 0.87, "C": 0.62, "D" : 0.37, "E" : 0.125, "F" : 0}
    for letter_scale in scalings:
        scalings_copy.append(scaling_dict[letter_scale])
    return scalings_copy

# input weapon details
grades : list[str]= [input(f"Input grade for skill {1+i}: ").upper() for i in range(4)]
requirements : list[int] = [int(input(f"Input requirement for skill {i+1}: ")) for i in range(4)]

# input default class skills
skills : list[int] = [int(input(f"Input default skill level {1 + i}: ")) for i in range(4)]

#input base phy + magic damage 
base_physical : int = int(input(f"Input base physical damage of weapon: "))
base_magical : int = int(input(f"Input base magical damage of weapon: "))

# levels to optimize with
level : int = int(input(f"Input number of skill points to input: "))

# cost vector for objective function
scalings_floats = _get_scales_list(grades)
cost_vector = [-0.612, -0.612, -0.642, -0.642, 0, 0, 0, 0, 0, 0, 0, 0]

# multiply correctly according to mathematical formulation
for i, scalar in enumerate(scalings_floats):
    if i < 2:
        cost_vector[i] *= scalar * base_physical
    else:
        cost_vector[i] *= scalar * base_magical

# now the cost_vector is fully constructed

# matrix representing constraints
# vector encoding RHS of constraints
constraint_matrix = []
constraint_vector : list[int] = []

# construct constraints
# constraint 1:
for i in range(4):
    row_i = np.zeros(4*3)
    row_i[i] = 1
    row_i[i+4] = 1
    constraint_matrix.append(row_i)
    constraint_vector.append(99)

#constraint 2:
for i in range(4):
    row_i = np.zeros(4*3)
    row_i[i] = 1
    row_i[i+4*2] = -1
    constraint_matrix.append(row_i)
    constraint_vector.append(max(requirements[i], skills[i]))

# constraint 3:
row_i = np.zeros(4*3)
row_i[0:4] = 1
constraint_matrix.append(row_i)
constraint_vector.append(level + sum(skills))

soln = sc.optimize.linprog(cost_vector, A_eq = constraint_matrix, b_eq = constraint_vector)
print(soln)

problem_solver = TwoPhaseSimplex(constraint_matrix, constraint_vector, cost_vector)
problem_solver.solve_program()
print(problem_solver.get_solution())
