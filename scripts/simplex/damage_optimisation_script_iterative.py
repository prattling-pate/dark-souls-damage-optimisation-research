from two_phase_simplex import LinearPieceWiseTwoPhaseSimplex
import numpy as np

def _get_scales_list(scalings : list[str]) -> list[float]:
    """Gets the list of float damage scales for the weapon given"""
    scalings_copy = []
    # translate scalings to floats
    scaling_dict = {"S" : 1.7, "A" : 1.195, "B" : 0.87, "C": 0.62, "D" : 0.37, "E" : 0.125, "F" : 0}
    for letter_scale in scalings:
        scalings_copy.append(scaling_dict[letter_scale])
    return scalings_copy

def _get_cost_vector(skill_vector : list[float]) -> list[float]:
    skill_vector_copy = skill_vector.copy()
    print(skill_vector_copy)
    for i in range(4):
        # physical skills
        if i < 2:
            if skill_vector_copy[i] <= 10:
                skill_vector_copy[i]*=0.005
            elif skill_vector_copy[i] <= 20:
                skill_vector_copy[i] *= 0.035
            elif skill_vector_copy[i] <= 40:
                skill_vector_copy[i] *= 0.0225
            else:
                skill_vector_copy[i] *= 0.0025
        # magical skills
        else:
            if skill_vector_copy[i] <= 10:
                skill_vector_copy[i]*=0.005
            elif skill_vector_copy[i] <= 30:
                skill_vector_copy[i] *= 0.0225
            elif skill_vector_copy[i] <= 50:
                skill_vector_copy[i] *= 0.015
            else:
                skill_vector_copy[i] *= 0.0041
    return skill_vector_copy + [0 for i in range(8)]

# input weapon details
grades : list[str]= [input(f"Input grade for skill {1+i}: ").upper() for i in range(4)]
requirements : list[int] = [int(input(f"Input requirement for skill {i+1}: ")) for i in range(4)]

# input default class skills
skills : list[float] = [int(input(f"Input default skill level {1 + i}: ")) for i in range(4)]

#input base phy + magic damage 
base_physical : int = int(input(f"Input base physical damage of weapon: "))
base_magical : int = int(input(f"Input base magical damage of weapon: "))

# levels to optimize with
level : int = int(input(f"Input number of skill points to input: "))

# cost vector for objective function
scalings_floats = _get_scales_list(grades)
cost_vector : list[float] = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

# find the correct piece-wise section of damage rating functions
cost_vector = _get_cost_vector(skills)

# multiply correctly according to mathematical formulation
for i, scalar in enumerate(scalings_floats):
    if i < 2:
        cost_vector[i] *= scalar * base_physical
    elif i < 4:
        cost_vector[i] *= scalar * base_magical
    else:
        break
# now the cost_vector is fully constructed

# matrix representing constraints
# vector encoding RHS of constraints
constraint_matrix = []
constraint_vector : list[int] = []

# construct constraints
# constraint set 1:
for i in range(4):
    row_i = np.zeros(4*3)
    row_i[i] = 1
    row_i[i+4] = 1
    constraint_matrix.append(row_i)
    constraint_vector.append(99)

#constraint set 2:
for i in range(4):
    row_i = np.zeros(4*3)
    row_i[i] = 1
    row_i[i+4*2] = -1
    constraint_matrix.append(row_i)
    constraint_vector.append(max(requirements[i], int(skills[i])))

# constraint 3:
row_i = np.zeros(4*3)
row_i[0:4] = 1
constraint_matrix.append(row_i)
constraint_vector.append(level + int(sum(skills)))

problem_solver = LinearPieceWiseTwoPhaseSimplex(constraint_matrix, constraint_vector, cost_vector, scalings_floats, base_physical, base_magical)

problem_solver.solve_program()

print(problem_solver.get_solution())

