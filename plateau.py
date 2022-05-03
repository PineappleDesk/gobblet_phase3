"""Module Joueur

Functions:
    * Plateau - Classe représentant un Plateau.
"""

import operator as op
from functools import partial, reduce
from types import NoneType
from typing import Union
from gobblet import Gobblet, GobbletError, default, forall, inSet, interleave, map_2d

class Plateau:
    """
    Plateau
    """

    def __init__(self, plateau):
        """Constructeur de Plateau

        Vous ne devez PAS modifier cette méthode

        Args:
            plateau (list): Plateau à construire tel que représenté dans l'énoncé
        """
        self.plateau = self.valider_plateau(plateau)

    def valider_plateau(self, plateau: list([list(list)])):
    
        """Validateur de Plateau
        -> list[list[Union[NoneType, Gobblet]]]:

        Args:
            plateau (list): Plateau tel que représenté dans l'énoncé

        Returns:
            list: Plateau composé de liste de Gobblets ou None pour l'absence de Gobblet

        Raises:
            *GobbletError: Le plateau doit être une liste
            *GobbletError: Le plateau ne possède pas le bon nombre de ligne
            *GobbletError: Le plateau ne possède pas le bon nombre de colonne dans les lignes
            *GobbletError: Les Gobblets doivent être des listes de paires ou une liste vide
        """
        if type(plateau) != list:
            raise GobbletError("Le plateau doit être une liste")
        if len(plateau) != 4:
            raise GobbletError("Le plateau ne possède pas le bon nombre de ligne")
        if not forall(lambda xs: len(xs) == 4, plateau):
            raise GobbletError("Le plateau ne possède pas le bon nombre de colonne dans les lignes")
        if not forall(lambda xs: forall(lambda x: (type(x) == list) and (len(x) in [0, 2]), xs), plateau):
            raise GobbletError("Les Gobblets doivent être des listes de paires ou une liste vide")

        def map_2d(x):
            if x == []:
                return None
            else:
                return Gobblet(x[1], x[0])

        return list(map(lambda xs: list(map(map_2d, xs)), plateau))
        
    def __str__(self):
        """Formater un plateau

        Returns:
            str: Représentation du plateau avec ses Gobblet
        """
        
        vcount = reversed(range(4))

        def fmt_actLines(lin, gobs: list[Gobblet]):
            def fmt_gob(g: Gobblet):
                gstr = g.formater_un_gobblet() if type(g) == Gobblet else ' '
                return f" {gstr} "
            return f"{lin}{interleave(list(map(fmt_gob, gobs)), '|')}\n"

        #lignes où l'action du jeu se déroule
        actLines = list(map(fmt_actLines, vcount, self.plateau))

        #représentation du plateau sans les chiffres horizontaux
        plat = interleave(actLines, " ───┼───┼───┼───\n")

        return reduce(op.add, plat) + "  0   1   2   3 "

    def retirer_gobblet(self, no_colonne, no_ligne):
        """Retirer un Gobblet du plateau

        Args:
            no_colonne (int): Numéro de la colonne
            no_ligne (int): Numéro de la ligne

        Returns:
            Gobblet: Gobblet retiré du plateau

        Raises:
            GobbletError: Ligne et colonne doivent être des entiers
            GobbletError: Le numéro de la ligne doit être 0, 1, 2 ou 3
            GobbletError: Le numéro de la colonne doit être 0, 1, 2 ou 3
            GobbletError: Le plateau ne possède pas de Gobblet pour la case demandée
        """
        if type(no_colonne) != int or type(no_ligne) != int:
            raise GobbletError('Ligne et colonne doivent être des entiers')

        if no_ligne != 0 and no_ligne != 1 and no_ligne != 2 and no_ligne != 3:
            raise GobbletError('Le numéro de la ligne doit être 0, 1, 2 ou 3')

        if no_colonne != 0 and no_colonne != 1 and no_colonne != 2 and no_colonne != 3:
            raise GobbletError('Le numéro de la colonne doit être 0, 1, 2 ou 3')
        if self.plateau[no_ligne][no_colonne] is None:
            raise GobbletError('Le plateau ne possède pas de Gobblet pour la case demandée')

        

    def placer_gobblet(self, no_colonne: int, no_ligne: int, gobblet: Gobblet) -> None:
        """Placer un Gobblet dans le plateau

        Args:
            no_colonne (int): Numéro de la colonne (0, 1, 2 ou 3)
            no_ligne (int): Numéro de la ligne (0, 1, 2 ou 3)
            gobblet (Gobblet): Gobblet à placer dans le plateau

        Raises:
            *GobbletError: Ligne et colonne doivent être des entiers
            *GobbletError: Le numéro de la ligne doit être 0, 1, 2 ou 3
            *GobbletError: Le numéro de la colonne doit être 0, 1, 2 ou 3
            GobbletError: Le Gobblet ne peut pas être placé sur la case demandée
        """
        if not (type(no_colonne) == int and type(no_ligne) == int):
            raise GobbletError("Ligne et colonne doivent être des entiers")

        if not no_ligne in range(4):
            raise GobbletError("Le numéro de la ligne doit être 0, 1, 2 ou 3")

        if not no_colonne in range(4):
            raise GobbletError("Le numéro de la colonne doit être 0, 1, 2 ou 3")

        if not default(self.plateau[no_colonne][no_ligne], ret=Gobblet(0, 1)) < gobblet:
            raise GobbletError('Le Gobblet ne peut pas être placé sur la case demandée')

        self.plateau[no_colonne][no_ligne] = gobblet
    

    def état_plateau(self):
        """Obtenir l'état du plateau

        Returns:
            list: Liste contenant l'état du plateau tel que représenté dans l'énoncé
        """
        def fn(x: Gobblet):
            return [x.no_joueur, x.grosseur] if not x is None else []

        return map_2d(fn, self.plateau)

    def formater_plateau(self):
        return str(self)