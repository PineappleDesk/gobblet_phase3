# -*- coding: utf-8 -*-
"""Jeu Gobblet

Ce programme permet de joueur au jeu Gobblet.
"""
from api import débuter_partie, lister_parties
from gobblet import (
    formater_jeu,
    formater_les_parties,
    interpréteur_de_commande,
)
from joueur import Joueur
from plateau import Plateau

# Mettre ici votre secret récupérer depuis le site de PAX
SECRET = "86b4350c-5ea6-4b70-b75d-d0ca393301c6"
def interpréteur_de_commande():
    parser = ArgumentParser(description='Gobblet')
    parser.add_argument('-l', '--lister', action = 'store_true', help = 'Lister les parties existantes')
    parser.add_argument('-a', '--automatique', action = 'store_true', help = 'Activer le mode automatique')
    parser.add_argument('IDUL', help = 'IDUL du joueur')
    return parser.parse_args()

if __name__ == "__main__":
    args = interpréteur_de_commande()
    if args.lister:
        parties = lister_parties(args.IDUL, SECRET)
        print(formater_les_parties(parties))
    else:
        id_partie, plateau, joueurs = débuter_partie(args.IDUL, SECRET)
        while True:
            # Implémentez votre boucle de jeu
            pass
