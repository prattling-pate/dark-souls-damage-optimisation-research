from damage_optimisation_script_iterative_function import optimise_iteratively
from damage_optimisation_script_approximation_function import optimise_damage_approximately
from utility.logger import Logger
import random as rnd
from objective_fn import get_total_damage_rating
import time
import json

def _generate_random_feasible_test_case():
    # need to generate random grades, requirements, default skill levels, base damages, number of levels to use  for each
    test_case = {}
    # want to produce test cases such that the second constraint set is always satisfied
    grades_set = ["S", "A", "B", "C", "D", "E", "F"]
    test_case["grades"] = [rnd.choice(grades_set) for i in range(4)]
    test_case["requirements"] = [rnd.randint(1, 50) for i in range(4)]
    test_case["skills"] = [rnd.randint(1,50) for i in range(4)]
    test_case["base_physical"] = rnd.randint(0, 500)
    test_case["base_magical"] = rnd.randint(0, 500)
    # levels is the only one you need to bound correctly for feasible setups
    # levels upper bound is sum ( [99 for i in range(4)] - skills)
    upper_bound_levels = 0 
    for i in range(4):
        upper_bound_levels += 99 - max(test_case["skills"][i], test_case["requirements"][i])
    lower_bound_levels = 0
    for i in range(4):
        lower_bound_levels += max(test_case["skills"][i], test_case["requirements"][i])
    test_case["levels"] = rnd.randint(lower_bound_levels, upper_bound_levels)
    return test_case

def generate_random_feasible_test_cases(n : int):
    test_cases = []
    for i in range(n):
        test_case = _generate_random_feasible_test_case()
        test_cases.append(test_case)
    return test_cases

def read_problem_from_json():
    problem = {}
    with open('problem.json', 'r') as f:
        problem = json.load(f)
    return problem

def run_test_case(test_case):
    start_it = time.time()
    iterative_solution = optimise_iteratively(test_case["grades"], test_case["requirements"], test_case["skills"], test_case["base_physical"], test_case["base_magical"], test_case["levels"])
    obj_fn_it_soln = get_total_damage_rating(iterative_solution, test_case["grades"],[test_case["base_physical"], test_case["base_magical"]])   
    runtime_it = time.time() - start_it
    start_app = time.time()
    approximate_solution = optimise_damage_approximately(test_case["grades"], test_case["requirements"], test_case["skills"], test_case["base_physical"], test_case["base_magical"], test_case["levels"])
    obj_fn_app_soln = get_total_damage_rating(approximate_solution, test_case["grades"],[test_case["base_physical"], test_case["base_magical"]]) 
    runtime_app = time.time() - start_app
    results = {"runtime_it" : runtime_it, "soln_it" : iterative_solution, "obj_fun_it_soln" : obj_fn_it_soln, "runtime_app" : runtime_app, "soln_app": approximate_solution, "obj_fn_app_soln" : obj_fn_app_soln}
    return results, test_case

def run_test_cases(test_cases):
    results = []
    for case in test_cases:
        results.append(run_test_case(case))
    return results

def main():
    preset_problem = read_problem_from_json()
    results_preset = run_test_cases([preset_problem])
   # test_cases = generate_random_feasible_test_cases(1)
   # results = run_test_cases(test_cases)
    logger = Logger("results.txt")
   # for result in results:
   #     logger.log(str(result[0]) + "\n")
   #     logger.log(str(result[1]) + "\n")
    logger.log(str(results_preset))
    logger.write_log()


main()    
