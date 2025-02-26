# -*- coding=utf-8 -*-
"""
Noms de binômes :
    SOSSOU Horacio
    MIHAN Zlanca-Nto

Q1 : Effectif année 1 = (Effectif Année 0) * (Matrice d'évolution)
                     [0.95   0    0   ]
    [200 500 3000] * [0.02  0.9   0   ]
                     [0     0.01  0.8 ]

    Niveau N1 = 200*0.95 + 500*0.02 + 3000*0 = 200
    Niveau N2 = 200*0 + 500*0.9 + 3000*0.01 = 480
    Niveau N3 = 200*0 + 500*0 + 3000*0.8 = 2400

Q2 :
    Variables de décision :
    Rij : Nombre de récrutements au niveau j de l'année i
    c : Nombre de licenciements au niveau j de l'année i
    Sij : Nombre de d'employés au niveau j de l'année i

    Contraintes :
    Sij = Evolution naturelle + Rij − Lij
    Sij ≥ Besoins en effectifs pour l’annee i
    Rij, Lij, Sij ≥ 0

    Fonction objectif :
    (min) z = (Coût salarial)*Sij + (Coûts de recrutement)*Rij + (Coûts de licenciement)*Lij

Q4 : Somme(Lij) = 236 + 405 + 104 = 745

Q5a :
    On procède à l'ajout d'une contrainte supplémentaire au prog linéaire de la question 2.
    somme(somme(Lij)) <= L (avec i allant de 1 à 3, et j allant de 1 à 3)

Q5b :


"""

"""Structure of the code used to solve a linear programming problem with """


from pathlib import Path  # built-in usefull Path class
from pulp import PULP_CBC_CMD, LpMinimize, LpProblem, LpStatus, LpVariable, lpSum


# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #
from pulp import PULP_CBC_CMD, LpMinimize, LpProblem, LpStatus, LpVariable, lpSum
from pathlib import Path

def set_model():
    """Minimisation problem for personnel planning."""
    # ------------------------------------------------------------------------ #
    # Linear problem with minimisation
    # ------------------------------------------------------------------------ #
    prob = LpProblem(name='personnel_planning', sense=LpMinimize)

    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #
    # Variables de recrutement
    R = {
        (i, j): LpVariable(name=f'R_{i}_{j}', lowBound=0, cat='Integer')
        for i in range(1, 4) for j in range(2, 4)
    }

    # Variables de licenciement
    L = {
        (i, j): LpVariable(name=f'L_{i}_{j}', lowBound=0, cat='Integer')
        for i in range(1, 4) for j in range(1, 4)
    }

    # Variables d'effectif
    S = {
        (i, j): LpVariable(name=f'S_{i}_{j}', lowBound=0, cat='Integer')
        for i in range(1, 4) for j in range(1, 4)
    }

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
    # Coûts salariaux
    salary_costs = {
        1: 100,  # N1
        2: 70,   # N2
        3: 50    # N3
    }

    # Coûts de recrutement
    recruitment_costs = {
        2: 10,  # N2
        3: 5    # N3
    }

    # Coûts de licenciement
    layoff_costs = {
        1: 50,  # N1
        2: 35,  # N2
        3: 25   # N3
    }

    # Fonction objectif : minimiser le coût total
    prob += lpSum(
        salary_costs[j] * S[i, j] for i in range(1, 4) for j in range(1, 4)
    ) + lpSum(
        recruitment_costs[j] * R[i, j] for i in range(1, 4) for j in range(2, 4)
    ) + lpSum(
        layoff_costs[j] * L[i, j] for i in range(1, 4) for j in range(1, 4)
    ), "Total Cost"

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #
    # Effectifs initiaux
    S[0, 1] = LpVariable(name='S_0_1', lowBound=200, upBound=200, cat='Integer') #N1
    S[0, 2] = LpVariable(name='S_0_2', lowBound=500, upBound=500, cat='Integer') #N2
    S[0, 3] = LpVariable(name='S_0_3', lowBound=3000, upBound=3000, cat='Integer') #N3

    # Matrice d'évolution
    evolution_matrix = {
        (1, 1): 0.95,  # N1 -> N1
        (2, 1): 0.02,  # N1 -> N2
        (3, 1): 0.00,  # N1 -> N3
        (2, 2): 0.90,  # N2 -> N2
        (3, 2): 0.01,  # N2 -> N3
        (3, 3): 0.80   # N3 -> N3
    }

    # Contraintes d'évolution des effectifs
    for i in range(1, 4):
        for j in range(1, 4):
            if j == 1:
                prob += S[i, 1] == evolution_matrix[(1, 1)] * S[i-1, 1] + R[i, 2] - L[i, 1]
            elif j == 2:
                prob += S[i, 2] == evolution_matrix[(2, 1)] * S[i-1, 1] + evolution_matrix[(2, 2)] * S[i-1, 2] + R[i, 2] - L[i, 2]
            elif j == 3:
                prob += S[i, 3] == evolution_matrix[(3, 1)] * S[i-1, 1] + evolution_matrix[(3, 2)] * S[i-1, 2] + evolution_matrix[(3, 3)] * S[i-1, 3] + R[i, 3] - L[i, 3]

    # Contraintes de besoins en effectifs
    needs = {
        (1, 1): 150,  # Année 1, N1
        (1, 2): 700,  # Année 1, N2
        (1, 3): 2000, # Année 1, N3
        (2, 1): 200,  # Année 2, N1
        (2, 2): 500,  # Année 2, N2
        (2, 3): 3000, # Année 2, N3
        (3, 1): 200,  # Année 3, N1
        (3, 2): 500,  # Année 3, N2
        (3, 3): 3000  # Année 3, N3
    }

    for i in range(1, 4):
        for j in range(1, 4):
            prob += S[i, j] >= needs[(i, j)]

    # Return the problem and the decision variables
    return prob, R, L, S

def solve():
    """Solve the personnel planning problem."""
    # ------------------------------------------------------------------------ #
    # Solve the problem using the model
    # ------------------------------------------------------------------------ #
    prob, R, L, S = set_model()
    # After solving, a .log file is written.
    prob.solve(PULP_CBC_CMD(msg=False, logPath=Path('./personnel_planning.log')))

    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print_log_output(prob, R, L, S)

def print_log_output(prob, R, L, S):
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
    print("Recrutements:")
    for key, var in R.items():
        print(f'{var.name}: {var.varValue}')

    print()
    print("Licenciements:")
    for key, var in L.items():
        print(f'{var.name}: {var.varValue}')

    print()
    print("Effectifs:")
    for key, var in S.items():
        print(f'{var.name}: {var.varValue}')

if __name__ == '__main__':
    solve()