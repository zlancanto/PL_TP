# -*- coding=utf-8 -*-


"""Structure of the code used to solve a linear programming problem with PuLP."""


from pathlib import Path  # built-in usefull Path class
from pulp import PULP_CBC_CMD, LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable, lpSum


# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #
def set_model():
    """Maximisation problem."""
    # ------------------------------------------------------------------------ #
    # Linear problem with maximisation
    # ------------------------------------------------------------------------ #
    prob = LpProblem(name='maximisation_problem', sense=LpMinimize)
    # FIXME: it is not always a maximization problem ...

    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #
    x_1 = LpVariable('x_1', lowBound=0)
    x_2 = LpVariable('x_2', lowBound=0)

    # List format: 
    # x = [LpVariable(f'x_{i}', lowBound=0) for i in range(2)]

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
    prob += 2 * x_1 + 5 * x_2, "Objective"

    # List format: 
    # w = [1, 3]
    # prob += lpSum(w[i] * var for i, var in enumerate(x)), "Objective"

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #
    prob += 3 * x_1 + 8 * x_2 >= 24, "Constraint 1"
    #prob += x_2 <= 1, "Constraint 2"

    # List format:
    # c_1 = [1, 1]
    # c_2 = [0, 1]
    # b = [2, 1]
    # prob += lpSum(c_1[i] * var for i, var in enumerate(x)) <= b[1], "Constraint 1"
    # prob += lpSum(c_2[i] * var for i, var in enumerate(x)) <= b[2], "Constraint 2"

    # Return the problem and the list of decision variables
    return prob, x_1, x_2


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
    prob, x_1, x_2 = set_model()
    # After solving, a `.log` file is written.
    prob.solve(PULP_CBC_CMD(msg=False, logPath=Path('./base.log')))

    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print_log_output(prob, x_1, x_2)


# ============================================================================ #
#                                   UTILITIES                                  #
# ============================================================================ #
def print_log_output(prob, x_1, x_2):
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
    print(f'{x_1.name}\t\t{x_1.varValue}')
    print(f'{x_2.name}\t\t{x_2.varValue}')


if __name__ == '__main__':
    solve()
