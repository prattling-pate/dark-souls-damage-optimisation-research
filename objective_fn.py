import numpy as np

def get_scales_list(scalings : np.ndarray) -> np.ndarray:
    """Gets the list of float damage scales for the weapon given"""
    scalings_copy = scalings.copy()
    # translate scalings to floats
    scaling_dict = {"S" : 1.7, "A" : 1.195, "B" : 0.87, "C": 0.62, "D" : 0.37, "E" : 0.125, "F" : 0}
    for i, letter_scale in enumerate(scalings):
        scalings_copy[i] = scaling_dict[letter_scale]
    return scalings_copy

def rating_physical(x : int) -> float:
    """piecewise continous linear function depicting the physical rating of a character"""
    if x <= 10:
        return 0.005*x
    elif x <= 20:
        return 0.05 + 0.035*(x-10)
    elif x <= 50:
        return 0.4 + 0.0225*(x-20)
    elif x < 99:
        return 0.85 + 0.0025*(x-40)
    else:
        return 1
    
def rating_magic(x : int) -> float:
    """piecewise continous linear function depicting the magic rating of a character"""
    if x <= 10:
        return 0.005*x
    elif x <= 30:
        return 0.05 + 0.0225*(x-10)
    elif x <= 50:
        return 0.5 + 0.015*(x-30)
    elif x < 99:
        return 0.8 + 0.0041*(x-50)
    else:
        return 1
    
def get_rating(i : int, x : int) -> float:
    """
    Gets the rating of skill i dependant on its skill level x.
    """
    assert i >= 0 and i < 4 # assert that the skill is in the accepted range
    if (i < 2):
        return rating_physical(x)
    return rating_magic(x)
    
def get_ratings_list(points : list) -> list:
    ratings_copy = points.copy()
    for i, point in enumerate(points):
        ratings_copy[i] = get_rating(i, point)
    return ratings_copy

def get_total_damage_rating(points : list, scalings : list, weapon : list, two_handing : bool = False):
    """
    The total attack rating of the dark souls game engine,
    points = x = [STR, DEX, INT, FAITH] (skill points)
    scalings = [STR, DEX, INT, FAITH] (letter scaling of skills)
    weapon = [base_physical, base_magic]
    Note that only points is variate and all other inputs are constants
    """
    # two handing a weapon causes a 1.5x increase in strength skill
    if (two_handing):
        points[0] *= 1.5
    # translate letter scales to float multipliers
    scalings = np.array(get_scales_list(scalings))
    # get damage ratings for all skills dependant on points
    ratings = np.array(get_ratings_list(points))
    # reassign weapon to be a np array for vector operations
    weapon : np.ndarray = np.array(weapon)
    decision_variates : np.ndarray = np.zeros(2)
    # multiplying two np arrays results in an entry wise multiplication
    decision_variates[0] = 1+sum(ratings[0:2]*scalings[0:2])
    decision_variates[1] = 1+sum(ratings[2:4]*scalings[2:4])
    # now dot product of weapon and decision_variates
    total_damage_rating = np.dot(weapon, decision_variates)
    return total_damage_rating
