"""
Q1
Fonction objectif :
    L'objectif est de minimiser la somme des coûts totaux,
    qui incluent à la fois les coûts de location des entrepôts et les coûts
    de transport pour livrer la marchandise aux différentes zones géographiques.
    - Coût de location : Le coût de location dépend des entrepôts que l'entreprise
        décide de louer. Chaque entrepôt Ei  a un coût de location mensuel Pi
    - Coût de transport : Le coût de transport dépend du nombre de camions
        nécessaires pour livrer la marchandise de chaque entrepôt à chaque zone.
        Chaque camion a un coût de livraison Lij pour transporter la marchandise
        de l'entrepôt Ei à la zone Zj
    La fonction objectif peut donc s'écrire comme la somme des coûts de location
    et des coûts de transport.

Contraintes :
    1. Contrainte de capacité des entrepôts : La quantité totale de marchandise stockée
     dans chaque entrepôt ne doit pas dépasser sa capacité. La capacité de chaque entrepôt
     Ei est donnée par Ci*C
    2. Contrainte de demande : La demande de chaque zone Zj doit être satisfaite. La demande
     de chaque zone est donnée par Dj*C où Dj est un entier représentant le nombre de camions
     nécessaires pour satisfaire la demande de la zone Zj
    3. Contrainte de livraison : Chaque livraison doit être effectuée par un camion
     complètement rempli. Cela signifie que le nombre de camions utilisés pour livrer
     la marchandise de l'entrepôt Ei à la zone Zj doit être un entier
    4. Contrainte de choix des entrepôts : L'entreprise doit décider quels entrepôts louer.
     Cela peut être modélisé par une variable binaire qui indique si un entrepôt est loué ou non.


Q2
Variables de décision :
- Ei : Variable binaire qui indique si l'entrepôt Ei est loué ou non
- Ci : Nombre entier représentant la capacité de l'entrepôt Ei en termes de nombre de camions
- Dj : Nombre de camions nécessaires pour satisfaire la demande de la zone Zj
- Cij : Variable entière qui représente le nombre de camions utilisés pour livrer la zone Zj à partir de l'entrepôt Ei
- Pi : Coût de location mensuel de l'entrepôt Ei
- Lij : Coût de livraison d'un camion de l'entrepôt Ei à la zone Zj
 la marchandise de l'entrepôt Ei à la zone Zj

Fonction objectif :
(min) z = somme(Pi*Ei) + somme(somme(Lij*Cij)) avec (i = 1,...,5) et (j = 1,...,3)

Contraintes :
somme(Cij*C) <= Ci*C*Ei <==> somme(Cij) <= Ci*Ei avec i = 1,...,5
Dj*C <= somme(Cij*C) <==> Dj <= somme(Cij) avec j = 1,...,3
Cij, Ci et Dj sont des entiers naturels avec (i = 1,...,5) et (j = 1,...,3)
Ei est un binaire avec i = 1,...,5

Q3
Coût obtenu : 10345€ (voir question3.py pour le code)

Q4
(voir question4.py pour le code)
Interprétation : Le résultat obtenu est le même que celui de la question 3
Explication : La capacité des camions est 10. Et les capacités des entrepôts et demandes sont toutes multiple
    de 10. Donc même avec les variables continues, les Ci, Dj et Cij respectent la contrainte d'intégrité. D'où
    le résultats identiques
"""
