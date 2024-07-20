def _get_soft_caps_gradient(skill_points: int, soft_caps_locations: list):
    """
    Function which returns the gradient of the damage rating function based off
    where the soft caps are located.

    This encodes the partial differentation explained in the LaTeX doc.
    """
    for i in range(len(soft_caps_locations) - 1):
        # if skill_points is between a boundary of the soft caps
        if soft_caps_locations[i] <= skill_points < soft_caps_locations[i+1]:
            # calculate the gradient of the damage rating function here
            # use a base 2 "logarthmic-like" piece-wise linear function
            return 0.5**(i+1)
    # if not in bounds then skill_points == 99, hence do not want to increase
    # so return 0 to not encourage this increase
    return 0


def _convert_letter_grades_to_floats(grades: list):
    grades_to_floats_dict = {"S": 1.7, "A": 1.195, "B": 0.87,
                             "C": 0.62, "D": 0.37, "E": 0.125}
    for i in range(len(grades)):
        grades[i] = grades_to_floats_dict[grades[i]]
    return grades


def _get_maximum_skill_change(weapon: dict, floats: bool):
    damage_ratings = weapon["grades"].copy()
    if not floats:
        damage_ratings = _convert_letter_grades_to_floats(damage_ratings)
    max_i = 0
    for i in range(len(damage_ratings)):
        if i < 2:
            damage_ratings[i] *= _get_soft_caps_gradient(
                    damage_ratings[i],
                    [1, 10, 20, 40, 99]) * weapon["physical_damage"]
        else:
            damage_ratings[i] *= _get_soft_caps_gradient(
                    damage_ratings[i],
                    [1, 10, 30, 50, 99]) * weapon["magic_damage"]
        if damage_ratings[i] > damage_ratings[max_i]:
            max_i = i
    return max_i


def maximise_damage(weapon: dict, default_skills: list,
                    levels: int, floats: bool = True) -> list:
    """
    Function which takes in a damage maximisation problem and returns the
    optimal skill setup for maximising the damage.

    Parameters
    ==========
        weapon - information about the weapon
            {grades: [(S|A|B|C|D|None) for i in range(n)],
                requirements: [[{1,...,99} for i in range(n)],
                    physical_damage, magic_damage}
        default_skills - skills that are defaulted by the character
             [{1,...,99} for i in range(n)]
        levels - number of skills to level up by
        grades - whether the grades given in weapon are letter grades
             or exact float scalars.
    Returns
    =======
        Optimal skill distribution to maximise damage dealt by the given weapon
        using the number of levels given.
    """
    # constraint 2 part 1 enforced here
    x: list = default_skills.copy()
    # firstly check if you can meet minimum requirements for the weapon
    for i, skill in enumerate(x):
        requirement_i = weapon["requirements"][i]
        # constraint 2 part 2 enforced here
        if requirement_i > skill:
            x[i] = requirement_i
            levels -= x[i]
    # in future can implement a "phase 2" system for this algorithm
    # which would allow for a best guess/encouragement for leveling
    # up appropriately for weapon requirements
    if levels < 0:
        raise Exception("Build is not feasible!")
    while levels > 0:
        skill = _get_maximum_skill_change(weapon, floats)
        x[skill] += 1
        levels -= 1
    return x
