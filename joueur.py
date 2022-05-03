"""Module Joueur

Functions:
    * Joueur - Classe représentant un joueur de Gobblet.
"""
import plateau
from api import jouer_coup
from gobblet import Gobblet, GobbletError, interleave
import random


class Joueur:
    """
    Joueur de Gobblet.
    """

    def __init__(self, nom, no_joueur, gobelets):
        """Constructeur de joueur.

        Ne PAS modifier cette méthode.

        Args:
            nom (str): le nom du joueur.
            no_joueur (int): le numéro du joueur (1 ou 2).
            gobelets (list): une liste des trois gobelets disponibles pour ce joueur, 
                             par exemple [[1, 1], [], [1, 2]], où la paire [1, 2] 
                             représente le numéro du joueur (1) et la grosseur du gobelet (2).
        """
        self.nom, self.no_joueur, self.piles = self.valider_joueur(
            nom, no_joueur, gobelets)

    def valider_joueur(self, nom, no_joueur, gobelets):
        """Validateur de Joueur.

        Args:
            nom (str): le nom du joueur.
            no_joueur (int): le numéro du joueur (1 ou 2).
            gobelets (list): une liste des trois gobelets disponibles pour ce joueur, 
                             par exemple [[1, 1], [], [1, 2]], où la paire [1, 2] 
                             représente le numéro du joueur (1) et la grosseur du gobelet (2).

        Returns:
            tuple[str, int, list]: Un tuple contenant
                                    - le nom du joueur;
                                    - son numéro;
                                    - une liste d'objets Gobblet (None pour une pile vide).

        Raises:
            *GobbletError: Le nom du joueur doit être une chaine de caractères non vide.
            *GobbletError: Le numéro du joueur doit être 1 ou 2.
            *GobbletError: Les piles de gobelets doivent être spécifiés sous la forme d'une liste.
            *GobbletError: Le joueur doit possèder 3 piles.
            *GobbletError: Une pile doit être une liste de deux entiers ou une liste vide.
        """
        if not (isinstance(nom) is str and nom != ""):
            raise GobbletError(
                "Le nom du joueur doit être une chaine de caractères non vide.")

        if not (isinstance(no_joueur) is int and 1 <= no_joueur <= 2):
            raise GobbletError("Le numéro du joueur doit être 1 ou 2.")

        if not (isinstance(gobelets) is list):
            raise GobbletError(
                f"Les piles de gobelets doivent être spécifiés sous la forme d'une liste. {gobelets}")

        if not(len(gobelets) == 3):
            raise GobbletError("Le joueur doit possèder 3 piles.")

        for pile in gobelets:
            if not (len(pile) == 2 or len(pile) == 0):
                raise GobbletError(
                    "Une pile doit être une liste de deux entiers ou une liste vide.")
            if len(pile) == 2:
                if isinstance(pile[0]) is not int and isinstance(pile[1]) is not int:
                    raise GobbletError(
                        "Une pile doit être une liste de deux entiers ou une liste vide.")
        gobjects = list(map(lambda g: Gobblet(
            g[1], no_joueur) if g != None else None, gobelets))

        return (nom, no_joueur, gobjects)

    def __str__(self):
        """Formater un joueur.

        Returns:
            str: Représentation du joueur et de ses piles de gobelets.
        """

        gobs = interleave(list(map(str, self.piles)), "   ")

        return self.nom + ":  " + gobs

        nom_du_joueur = self.nom
        chaine = ''
        chaine += nom_du_joueur + ':'
        for i in self.piles:
            taille_du_joueur = formater_un_gobblet(i)
            chaine += taille_du_joueur
        return chaine

    def retirer_gobblet(self, no_pile):
        """Retirer un gobelet de la pile.

        Args:
            no_pile (int): le numéro de la pile [0, 1, 2].

        Returns:
            Gobblet: le gobelet retiré de la pile.

        Raises:
            GobbletError: Le numéro de la pile doit être un entier.
            GobbletError: Le numéro de la pile doit être 0, 1 ou 2.
            GobbletError: Le joueur ne possède pas de gobelet pour la pile demandée.
        """
        if isinstance(no_pile) != int:
            raise GobbletError("Le numéro de la pile doit être un entier.")

        if no_pile != 0 and no_pile != 1 and no_pile != 2:
            raise GobbletError("Le numéro de la pile doit être 0, 1 ou 2.")

        if self.piles[no_pile] is None:
            raise GobbletError(
                "Le joueur ne possède pas de gobelet pour la pile demandée.")

        return self.piles[no_pile]

    def placer_gobblet(self, no_pile, gobelets):
        """Placer un gobelet dans la pile.

        Notez que les règles du jeu ne permettent pas de placer un gobelet dans une pile,
        sauf au début de la partie pour l'initialiser.

        L'emplacement de la pile doit donc être libre (valeur `None`).

        Args:
            no_pile (int): le numéro de la pile [0, 1, 2].
            gobelets (Gobblet): le gobelet à placer dans la pile.

        Raises:
            GobbletError: Le numéro de la pile doit être un entier.
            GobbletError: Le numéro de la pile doit être 0, 1 ou 2.
            GobbletError: Le gobelet doit appartenir au joueur.
            GobbletError: Vous ne pouvez pas placer un gobelet à cet emplacement.
        """
        if isinstance(no_pile) != int:
            raise GobbletError("Le numéro de la pile doit être un entier.")

        if no_pile != 1 and no_pile != 2 and no_pile != 0:
            raise GobbletError("Le numéro de la pile doit être 0, 1 ou 2.")

        if gobelets[no_pile] != None:
            raise GobbletError("Le gobelet doit appartenir au joueur.")

        if gobelets[no_pile[0]] != self.no_joueur:
            raise GobbletError(
                "Vous ne pouvez pas placer un gobelet à cet emplacement.")

    def récupérer_le_coup(self, plateau):
        """Récupérer le coup

        Demande au joueur le coup à jouer.
        Cette méthode ne doit PAS modifier le plateau.
        Cette méthode ne doit PAS modifier les piles de Gobblets.

        Returns:
            tuple: Un tuple composé d'une origine et de la destination.
                L'origine est soit un entier représentant le numéro de la pile du joueur
                ou une liste de 2 entier [x, y] représentant le gobelet sur le plateau.
                La destination est une liste de 2 entiers [x, y] représentant le gobelet
                sur le plateau.

        Raises:
            GobbletError: L'origine doit être un entier ou une liste de 2 entiers.
            GobbletError: L'origine n'est pas une pile valide.
            GobbletError: L'origine n'est pas une case valide du plateau.
            GobbletError: L'origine ne possède pas de gobelet.
            GobbletError: Le gobelet d'origine n'appartient pas au joueur.
            GobbletError: La destination doit être une liste de 2 entiers.
            GobbletError: La destination n'est pas une case valide du plateau.

        Examples:
            Quel gobelet voulez-vous déplacer:
            Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): 0
            Où voulez-vous placer votre gobelet (x,y): 0,1

            Quel Gobbgobeletlet voulez-vous déplacer:
            Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): 2,3
            Où voulez-vous placer votre gobelet (x,y): 0,1
        """
        origine = input(
            "Donnez le numéro de la pile (p) ou la position sur le plateau (x,y) : ")

        if isinstance(origine) != int and (isinstance(origine) != list and len(origine) != 2):
            raise GobbletError(
                "L'origine doit être un entier ou une liste de 2 entiers.")

        if origine not in self.gobelets:
            raise GobbletError("L'origine n'est pas une pile valide.")

        if origine not in plateau:
            raise GobbletError(
                "L'origine n'est pas une case valide du plateau.")

        if not self.gobelets[origine]:
            raise GobbletError("L'origine ne possède pas de gobelet.")

        if self.gobelets[self.no_pile[0]] != self.no_joueur:
            raise GobbletError(
                "Le gobelet d'origine n'appartient pas au joueur.")

        destination = input(
            "Où voulez-vous placer votre Gobblet ? Donnez des coordonnées (x,y) : ")

        if isinstance(destination) != list and len(destination) != 2:
            raise GobbletError(
                "La destination doit être une liste de 2 entiers.")

        if destination not in plateau:
            raise GobbletError(
                "La destination n'est pas une case valide du plateau.")

        return (origine, destination)

    def état_joueur(self):
        """Obtenir l'état du joueur

        Returns:
            dict: Dictionnaire contenant l'état du joueur tel que représenté dans l'énoncé
        """

        def pile_fn(x: Gobblet):
            return [x.no_joueur, x.grosseur]

        # return {"nom:" self.nom, "piles": map(lambda xs: map(pile_fn, xs), self.plateau)}

        return {"nom": self.nom, "piles": list(map(lambda x: pile_fn(x), self.piles))}


class Automate(Joueur):

    def __init__(self, nom, no_joueur, gobelets):
        pass

    def rec(plateau):
        n = 1
        looking_empty = True

        for i in plateau:
            if i:
                eat_or_step = random.randint(1, 2)
                if eat_or_step == 1:
                    origine = random.randint(1, 4)
                    destination = i
                    return (origine, destination)

                else:
                    while looking_empty:
                        new_ind = plateau.index(i)+n
                        if plateau[new_ind]:
                            n += 1
                        else:
                            origine = random.randint(1, 4)
                            destination = plateau[new_ind]

            else:
                origine = random.randint(1, 4)
                destination = i
                return (origine, destination)

    def rec_vide(plateau):
        continues = False
        while True:
            origine = random.randint(1, 4)
            destination = [random.randint(1, 5), random.randint(1, 5)]

            try:
                if origine not in self.gobelets:
                    raise GobbletError("L'origine n'est pas une pile valide.")

                if not self.gobelets[origine]:
                    raise GobbletError("L'origine ne possède pas de gobelet.")

                if self.gobelets[self.no_pile[0]] != self.no_joueur:
                    raise GobbletError(
                        "Le gobelet d'origine n'appartient pas au joueur.")

                continues = True

            except:
                pass

            if continues:
                break

    def récupérer_le_coup(self, plateau):

        for i in plateau:

            if i:
                rec(plateau)

            else:
                rec_vide(plateau)
