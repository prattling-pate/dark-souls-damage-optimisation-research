from damage_optimisation_script_iterative_function import optimise_iteratively
from damage_optimisation_script_approximation_function import optimise_damage_approximately
from utility.logger import Logger
import random as rnd
import time

def _generate_random_test_case():
    # need to generate random grades, requirements, default skill levels, base damages, number of levels to use  for each
    test_case = {}
    grades_set = ["S", "A", "B", "C", "D", "E", "F"]
    test_case["grades"] = [rnd.choice(grades_set) for i in range(4)]
    test_case["requirements"] = [rnd.randint(1, 50) for i in range(4)]
    test_case["skills"] = [rnd.randint(1,50) for i in range(4)]
    test_case["base_physical"] = rnd.randint(0, 500)
    test_case["base_magical"] = rnd.randint(0, 500)
    test_case["levels"] = rnd.randint(0, 100)
    return test_case

def generate_random_test_cases(n : int):
    test_cases = []
    for i in range(n):
        test_case = _generate_random_test_case()
        test_cases.append(test_case)
    return test_cases

def run_test_case(test_case):
    start_it = time.time()
    iterative_solution = optimise_iteratively(test_case["grades"], test_case["requirements"], test_case["skills"], test_case["base_physical"], test_case["base_magical"], test_case["levels"])
    runtime_it = time.time() - start_it
    start_app = time.time()
    approximate_solution = optimise_damage_approximately(test_case["grades"], test_case["requirements"], test_case["skills"], test_case["base_physical"], test_case["base_magical"], test_case["levels"])
    runtime_app = time.time() - start_app
    results = {"runtime_it" : runtime_it, "soln_it" : iterative_solution, "runtime_app" : runtime_app, "soln_app": approximate_solution}
    return results, test_case

def run_test_cases(test_cases):
    results = []
    for case in test_cases:
        results.append(run_test_case(case))
    return results

def main():
    test_cases = generate_random_test_cases(1)
    results = run_test_cases(test_cases)
    logger = Logger("results.txt")
    for result in results:
        logger.log(str(result[0]) + "\n")
        logger.log(str(result[1]) + "\n")
    logger.write_log()


main()    
