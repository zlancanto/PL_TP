from pathlib import Path
from pulp import PULP_CBC_CMD, LpMinimize, LpProblem, LpStatus, LpVariable, lpSum

# Données du problème
C = 10  # Capacité d'un camion en m³

# Prix de location des entrepôts (en euros)
p = [1000, 2700, 1000, 5000, 3000]

# Capacité des entrepôts (en m³)
c = [100, 450, 150, 600, 250]

# Demande des zones (en m³)
d = [400, 200, 300]

# Coûts de livraison (en euros par camion)
l = [
    [52, 60, 10],
    [80, 50, 32],
    [47, 18, 32],
    [49, 31, 14],
    [10, 20, 31]
]

# Nombre d'entrepôts et de zones
n = len(p)  # Nombre d'entrepôts
p_zones = len(d)  # Nombre de zones

# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #
def set_model():
    # ------------------------------------------------------------------------ #
    # Problème de minimisation
    # ------------------------------------------------------------------------ #
    prob = LpProblem(name='minimisation_probleme', sense=LpMinimize)

    # ------------------------------------------------------------------------ #
    # Variables de décision
    # ------------------------------------------------------------------------ #
    # Variables binaires pour indiquer si un entrepôt est loué ou non
    E = [LpVariable(f'E_{i}', cat='Binary') for i in range(n)]

    # Variables réelles pour le nombre de camions utilisés pour chaque livraison
    c_ij = [[LpVariable(f'c_{i}_{j}', lowBound=0, cat='Continuous') for j in range(p_zones)] for i in range(n)]

    # ------------------------------------------------------------------------ #
    # Fonction objectif
    # ------------------------------------------------------------------------ #
    # Minimiser la somme des coûts de location et des coûts de transport
    prob += lpSum(p[i] * E[i] for i in range(n)) + lpSum(l[i][j] * c_ij[i][j] for i in range(n) for j in range(p_zones)), "Coût total"

    # ------------------------------------------------------------------------ #
    # Contraintes
    # ------------------------------------------------------------------------ #
    # Contrainte de capacité des entrepôts
    for i in range(n):
        prob += lpSum(c_ij[i][j] for j in range(p_zones)) <= (c[i] / C) * E[i], f"Capacité_entrepôt_{i}"

    # Contrainte de demande des zones
    for j in range(p_zones):
        prob += lpSum(c_ij[i][j] for i in range(n)) >= (d[j] / C), f"Demande_zone_{j}"

    # Retourner le problème et les variables de décision
    return prob, E, c_ij


# ============================================================================ #
#                               SOLVE WITH DATA                                #
# ============================================================================ #
def solve():
    # ------------------------------------------------------------------------ #
    # Résoudre le problème
    # ------------------------------------------------------------------------ #
    prob, E, c_ij = set_model()
    prob.solve(PULP_CBC_CMD(msg=False, logPath=Path('./question4.log')))

    # ------------------------------------------------------------------------ #
    # Afficher les résultats
    # ------------------------------------------------------------------------ #
    print_log_output(prob, E, c_ij)


# ============================================================================ #
#                                   UTILITIES                                  #
# ============================================================================ #
def print_log_output(prob, E, c_ij):
    print()
    print('-' * 40)
    print('Statistiques')
    print('-' * 40)
    print()
    print(f'Nombre de variables: {prob.numVariables()}')
    print(f'Nombre de contraintes: {prob.numConstraints()}')
    print()
    print('Temps de résolution:')
    print(f'- (réel) {prob.solutionTime}')
    print(f'- (CPU) {prob.solutionCpuTime}')
    print()

    print(f'Statut de la solution: {LpStatus[prob.status]}')
    print(f'Valeur de la fonction objectif: {prob.objective.value()}')

    print()
    print('-' * 40)
    print("Valeurs des variables")
    print('-' * 40)
    print()
    for i in range(n):
        print(f'Entrepôt {i+1} loué (E_{i+1}): {E[i].varValue}')
        for j in range(p_zones):
            print(f'Camions de E{i+1} vers Z{j+1} (c_{i+1}_{j+1}): {c_ij[i][j].varValue}')


if __name__ == '__main__':
    solve()
