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
    for i in range(4):
        # physical skills
        if i < 2:
            if skill_vector_copy[i] <= 10:
                skill_vector_copy[i]*=0.05
            elif skill_vector_copy[i] <= 20:
                skill_vector_copy[i] *= 0.025
            elif skill_vector_copy[i] <= 40:
                skill_vector_copy[i] *= 0.00625
            else:
                skill_vector_copy[i] *= 0.125/59
        # magical skills
        else:
            if skill_vector_copy[i] <= 10:
                skill_vector_copy[i]*=0.005
            elif skill_vector_copy[i] <= 30:
                skill_vector_copy[i] *= 0.0125
            elif skill_vector_copy[i] <= 50:
                skill_vector_copy[i] *= 0.00625
            else:
                skill_vector_copy[i] *= 0.125/49
    return skill_vector_copy + [0 for i in range(8)]

def optimise_iteratively(grades, requirements, skills, base_physical, base_magical, level):
    scalings_floats = _get_scales_list(grades)

    cost_vector : list[float] = [-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0]

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

    return problem_solver.get_solution()
