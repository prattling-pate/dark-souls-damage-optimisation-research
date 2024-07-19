"""
This module allows the implementation of the two phase simplex method and can be used to solve
a given linear program provided it is in the correct form.
"""

from typing import Sequence
import numpy as np

class TwoPhaseSimplex:
    """
    Class which is used to solve a given linear program which is in standard given by a
    matrix a, vector b and vector c.
    The problem is set to maximising the objective function by default.
    """

    def __init__(
        self, a: Sequence[Sequence[float]], b: Sequence[float], c: Sequence[float]
    ) -> None:
        """
        Initializes the TwoPhaseSimplex solver object in terms of it's distinguishing components
        The problem to be solved is of the form: min c*x, s.t. Ax=b.
        Assumes that the problem must be translated to auxillary form.
        """
        valid, message = self._check_validity_of_arguments(a, b, c)
        if not valid:
            raise InvalidProblemException(
                "Invalid linear programming problem described: " + message
            )
        self._a: np.ndarray = np.array(a)
        self._b: np.ndarray = np.array(b)
        self._c: np.ndarray = np.array(c)
        self._tableau: np.ndarray = np.zeros((len(a) + 1, len(a) + len(a[0]) + 1))
        self._solution: np.ndarray = np.zeros(len(c))

    def _check_validity_of_arguments(
        self, a: Sequence[Sequence[float]], b: Sequence[float], c: Sequence[float]
    ) -> tuple[bool, str]:
        """
        Returns a bool referring to whether the input makes any sense as a linear program, if false
        it contains a meaningful error message pertaining as to why the input
        doesn't make any sense.
        """
        m: int = len(a)
        if m <= 0:
            return False, "A should have a postive number of rows"
        n: int = len(a[0])
        if n <= 0:
            return False, "A should have a positive number of columns"
        if len(b) != m:
            return False, "Vector b does not have the same length as matrix A has rows"
        if len(c) != n:
            return (
                False,
                "Vector c does not have the same length as matrix A has columns",
            )
        return True, ""

    def _construct_tableau(self) -> None:
        """
        Constructs the two phase simplex tableau
        """
        m: int
        n: int
        m, n = self._a.shape
        e: np.ndarray = np.ones(m)
        # top left entry is -e*b, e = (1,...,1)
        self._tableau[0, 0] = -np.dot(e, self._b)
        # tab[0, 1:n+1] (exclusive) entries are -e*A
        self._tableau[0, 1 : n + 1] = -np.matmul(e, self._a)
        # tab[1:m+1,0] = b.
        self._tableau[1 : m + 1, 0] = self._b
        # tab[1:m+1, 1:n+1] = A
        self._tableau[1 : m + 1, 1 : n + 1] = self._a
        # tab[n+1:, 1:] = Identity Matrix
        self._tableau[1 : m + 1, n + 1 : n + m + 1] = np.identity(m)

    def _find_pivot(self) -> tuple[int, int]:
        """
        Find the pivot (r,s) on the tableau using Bland's rule.
        """
        m: int = self._tableau.shape[0]
        s = 1
        while self._tableau[0, s] >= 0:
            s += 1
        min_ratio = np.inf
        r = 0
        for i in range(1, m):
            if self._tableau[i][s] > 0:
                temp = self._tableau[i, 0] / self._tableau[i, s]
                if min_ratio > temp:
                    min_ratio = temp
                    r = i
        return (r, s)

    def _pivot(self, r: int, s: int) -> None:
        """
        Induces pivoting operations on the (r,s) entry of the tableau,
        this causes the rth row to be divide by tableau[r,s] and then all entries
        on the sth column to become 0 other than where the row is r.
        """
        m: int = self._tableau.shape[0]
        self._tableau[r] /= self._tableau[r, s]
        for i in range(m):
            if i != r:
                self._tableau[i] -= self._tableau[r] * self._tableau[i, s]

    def _solve_auxillary_problem(self) -> np.ndarray:
        """
        Solves the auxillary problem using the phase 1 simplex method
        """
        m: int
        n: int
        m, n = self._a.shape
        # basis is always the auxillary variables
        basis: np.ndarray = np.arange(n + 1, n + m + 1)
        while self._tableau[0, 1:].min() < 0:
            r, s = self._find_pivot()
            if r != 0:
                self._pivot(r, s)
            basis[r - 1] = s  # beware of this line for the time being
        return basis

    def _check_tableau_for_constraint_violation(self, basis: np.ndarray) -> bool:
        """
        Ensures that if auxillary variables are in basis then they are equal to 0
        """
        m: int
        n: int
        m, n = self._a.shape
        for var in basis:
            if n + 1 <= var <= m + n:
                return False
        return True

    def _drive_auxillary_variables_from_basis(self, basis: np.ndarray) -> np.ndarray:
        """
        Removes auxillary variables from the basis of the simplex tableau, sets up for phase 2
        """
        m: int
        n: int
        m, n = self._a.shape
        for r, var in enumerate(basis):
            # if auxillary variable is in basis
            if n + 1 <= var <= m + n:
                # pivot on any non-zero entry on that basis variables row
                for s, var2 in enumerate(self._tableau[r + 1, 1:]):
                    if var2 != 0:
                        self._pivot(r + 1, s + 1)
                        # to drive the auxillary variable from basis
                        basis[r] = s + 1
                        break
        return basis

    def _get_solution(self, basis: np.ndarray):
        """
        Gets the current solution stored in the tableau, all variables not included in basis are 0
        by construction
        
        Note that the solutions array returned has 0 indexed variable numbers
        (i.e. 0th index is the 1st variable).
        """
        n: int = self._a.shape[1]
        solutions: np.ndarray = np.zeros(n)
        for i, var in enumerate(basis,1):
            # basis contains the numbered variable which is in the index
            solutions[var - 1] = self._tableau[i, 0]
        return solutions

    def _change_tableau_to_phase_two(self, basis: np.ndarray) -> None:
        """
        changes the objective function and removes columns of the auxillary variables,
        preparing the tableau for phase 2.
        """
        phase_one_solution: np.ndarray = self._get_solution(basis)
        self._tableau[0, 0] = -np.dot(self._c, phase_one_solution)
        n: int = self._a.shape[1]
        # take a copy of the tableau and remove the auxillary variables
        temp: np.ndarray = self._tableau[0:, 0 : n + 1].copy()
        # make the new tableau this copy
        self._tableau = temp
        # add in new constraints (of original problem)
        self._tableau[0, 1:] = self._c

    def complete_phase_one(self) -> np.ndarray:
        """
        Completes the first phase of the simplex method
        """
        self._construct_tableau()
        basis: np.ndarray = self._solve_auxillary_problem()
        return basis

    def _complete_phase_two(self, basis: np.ndarray) -> np.ndarray:
        """
        Solves the phase 2 simplex by applying the phase 1 simplex onto the
        new tableau.
        """
        while self._tableau[0, 1:].min() < 0:
            r, s = self._find_pivot()
            self._pivot(r, s)
            basis[r - 1] = s  # beware of this line for the time being
        return basis

    def _store_solution(self, basis: np.ndarray) -> None:
        """
        Writes the solution according to the current basis and tableau into the solution property
        """
        self._solution = self._get_solution(basis)

    def solve_program(self) -> bool:
        """
        Induces the solving of the phase 2 simplex problem prescribed by the object
        Returns True if the problem is bounded
        Returns False if the problem is unbounded
        """
        basis: np.ndarray = self.complete_phase_one()
        basis = self._drive_auxillary_variables_from_basis(basis)
        valid: bool = self._check_tableau_for_constraint_violation(basis)
        # if any optimal auxillary variable is non-zero then throw an error
        # this will only return if and only if it is not possible to drive
        # the variable from the basis (although there always should be a way)
        if not valid:
            return False
        self._change_tableau_to_phase_two(basis)
        basis = self._complete_phase_two(basis)
        self._store_solution(basis)
        return True

    def get_tableau(self) -> np.ndarray:
        """Returns the tableau current state"""
        return self._tableau

    def get_solution(self) -> list:
        """
        Returns dict containing the solution to the given system
        """
        solution_dict = []
        for i, soln in enumerate(self._solution):
            if i > 3:
                break
            # have to translate to 1 index variable names
            solution_dict.append(soln)
        return solution_dict

class LinearPieceWiseTwoPhaseSimplex(TwoPhaseSimplex):
    """
    An extension of the basic two phase simplex method class which allows for iterative
    solving of a problem with a  linear piece-wise objective function
    """
    def __init__(self, a, b, c, scalings_floats, base_physical, base_magical):
        super().__init__(a , b, c)
        self._scalings_floats = scalings_floats
        self._base_physical = base_physical
        self._base_magical = base_magical

    def _get_cost_vector(self, cost_vector) -> np.ndarray:
        # only use slopes of linear functions as we allowed to do that using the 
        # properties derived from solution equivalency
        cost_vector_copy = cost_vector.copy()
        for i in range(4):
            # physical skills
            if i < 2:
                if cost_vector_copy[i] <= 10:
                    cost_vector_copy[i] = -0.05
                elif cost_vector_copy[i] <= 20:
                    cost_vector_copy[i] = - 0.025
                elif cost_vector_copy[i] <= 40:
                    cost_vector_copy[i] = -0.00625
                else:
                    cost_vector_copy[i] = -0.125/59
            # magical skills
            else:
                if cost_vector_copy[i] <= 10:
                    cost_vector_copy[i] = -0.05
                elif cost_vector_copy[i] <= 30:
                    cost_vector_copy[i] = -0.0125
                elif cost_vector_copy[i] <= 50:
                    cost_vector_copy[i] = -0.00625
                else:
                    cost_vector_copy[i] = -0.125/49
        return cost_vector_copy

    def _complete_phase_two(self, basis: np.ndarray) -> np.ndarray:
        """
        Solves the phase 2 simplex by applying the phase 1 simplex onto the
        new tableau.
        """
        while self._tableau[0, 1:].min() < 0:
            r, s = self._find_pivot()
            self._pivot(r, s)
            basis[r - 1] = s
            # after pivoting change to new cost_vector and reformulate the phase two tableau
            cost_vector = self._get_cost_vector(self._get_solution(basis))
            for i, scalar in enumerate(self._scalings_floats):
                if i < 2:
                    cost_vector[i] *= scalar * self._base_physical
                else:
                    cost_vector[i] *= scalar * self._base_magical
            self._c = cost_vector
            self._change_tableau_to_phase_two(basis)
        return basis

    
class InvalidProblemException(Exception):
    """
    Exception which is displayed when the linear program
    described in the constructor for TwoPhaseSimplex does
    not induce a valid linear program for solution.
    """
    def __init__(self, message):
        self.message = message
