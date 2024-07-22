import damage_maximisation, damage_maximisation_elden_ring
import json

problem = {}

with open("problem.json", "r") as file:
    problem = json.load(file)

print("DS1 ", damage_maximisation.maximise_damage(problem["weapon"], problem["skills"], problem["levels"]))
print("ER ", damage_maximisation_elden_ring.maximise_damage(problem["weapon"], problem["skills"], problem["levels"]))
