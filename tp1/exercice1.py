# -*- coding=utf-8 -*-


"""Structure of the code used to solve a linear programming problem with PuLP."""


from pathlib import Path  # built-in usefull Path class
from pulp import PULP_CBC_CMD, LpMaximize, LpProblem, LpStatus, LpVariable, lpSum


# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #
def set_model():
    """Maximisation problem."""
    # ------------------------------------------------------------------------ #
    # Linear problem with maximisation
    # ------------------------------------------------------------------------ #
    prob = LpProblem(name='maximisation_problem', sense=LpMaximize)
    # FIXME: it is not always a maximization problem ...

    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #
    A = LpVariable('A', lowBound=0)
    B = LpVariable('B', lowBound=0)

    # List format: 
    # x = [LpVariable(f'x_{i}', lowBound=0) for i in range(2)]

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
    prob += 40 * A + 35 * B, "Objective"

    # List format: 
    # w = [1, 3]
    # prob += lpSum(w[i] * var for i, var in enumerate(x)), "Objective"

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #
    prob += 2 * A + 4 * B <= 50, "Constraint 1"
    prob += 3 * A + 2 * B <= 30, "Constraint 2"

    # List format:
    # c_1 = [1, 1]
    # c_2 = [0, 1]
    # b = [2, 1]
    # prob += lpSum(c_1[i] * var for i, var in enumerate(x)) <= b[1], "Constraint 1"
    # prob += lpSum(c_2[i] * var for i, var in enumerate(x)) <= b[2], "Constraint 2"

    # Return the problem and the list of decision variables
    return prob, A, B


# ============================================================================ #
#                               SOLVE WITH DATA                                #
# ============================================================================ #
def solve():
    """Solve the maximisation problem."""
    # ------------------------------------------------------------------------ #
    # Set data
    # ------------------------------------------------------------------------ #
    # Here: no data.

    # ------------------------------------------------------------------------ #
    # Solve the problem using the model
    # ------------------------------------------------------------------------ #
    prob, A, B = set_model()
    # After solving, a `.log` file is written.
    prob.solve(PULP_CBC_CMD(msg=False, logPath=Path('./base.log')))

    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print_log_output(prob, A, B)


# ============================================================================ #
#                                   UTILITIES                                  #
# ============================================================================ #
def print_log_output(prob, A, B):
    """Print the log output and problem solutions."""
    print()
    print('-' * 40)
    print('Stats')
    print('-' * 40)
    print()
    print(f'Number variables: {prob.numVariables()}')
    print(f'Number constraints: {prob.numConstraints()}')
    print()
    print('Time:')
    print(f'- (real) {prob.solutionTime}')
    print(f'- (CPU) {prob.solutionCpuTime}')
    print()

    print(f'Solve status: {LpStatus[prob.status]}')
    print(f'Objective value: {prob.objective.value()}')

    print()
    print('-' * 40)
    print("Variables' values")
    print('-' * 40)
    print()
    print(f'{A.name}\t\t{A.varValue}')
    print(f'{B.name}\t\t{B.varValue}')


if __name__ == '__main__':
    solve()
