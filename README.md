This repo is mainly concerned with the research of an optimisation problem of maximising damage of a weapon in dark souls (and maybe extrapolating this to other souls-like games).

## (Possible) Solutions
1. Approximation (explored, yielded some linear combination simplex method properties being found)
2. Iteratively running the simplex method every time the objective function changes due to x crossing discrete intervals on the piecewise objective function (does not work experimentally)
3. Deriving a mathematically justified algorithm for solving the problem with an exact solution.

# Observations
## Simplex Method
1. I have noticed that objective functions that differ by a real coefficient will not be any different from each other methodically. (i.e. two phase simplex method yields the same optimal solution) <br>
    - A proof for this will be attached in a proofs.pdf file that will be added soonish.<br>
2. I have also programatically conjectured (for n=1,...,100) that the solution given by a simplex method optimisation is identical to two functions that differ by a real positive multiple. <br>
    - I will attempt to prove this as well. <br>
3. Together these two will give that any functions that are linear combinations of another linear function will produce the same simplex result (given all other variables in the problem are controlled, i.e. constraints are equal).
## Exact solution (incremental algorithm)
1. Has the same idea as behind simplex method.
2. Manually increment each skill by 1 and following the path of greatest change using partial derivatives of the damage function.
3. Only look at partial derivatives local to current non-optimal solution (due to linear piecewise function).

# Take away
The simplex method cannot solve the damage optimisation problem, however it can approximate a solution by approximating a linear piece wise function to a linear function over it's whole domain.
