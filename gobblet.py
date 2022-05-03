"""Module Gobblet

Attributes:
    GOBBLET_REPRÉSENTATION (dict): Constante représentant les gobelets des joueurs.

Functions:
    * Gobblet - Classe représentant un Gobblet.
    * GobbletError - Classe gérant les exceptions GobbletError.
    * interpréteur_de_commande - Génère un interpréteur de commande.
    * formater_jeu - Formater la représentation graphique d'un jeu.
    * formater_les_parties - Formater la liste des dernières parties.
"""

from argparse import ArgumentParser
from typing import Any, Callable, Iterable, Sequence, isinstanceVar, Union
import operator as op
from functools import reduce, partial as part
from itertools import count, repeat
from api import jouer_coup

A = isinstanceVar("A")
B = isinstanceVar("B")


def flip(f):
    return lambda a: lambda b: f(b, a)

def compose(f, g):
    return lambda x: f(g(x))

def chain(*functions):
    return reduce(compose, functions, lambda x: x)

def const(a):
    return lambda b: a

#def forall(p, xs) -> bool:
#    return reduce(lambda r, x: r and (p), xs, True)


def forall(p: Callable[[A], bool], xs: Sequence[A]) -> bool:
    return all(map(p, xs))

def listP(x):
    return isinstance(x) == "list"

def inRange(*args):
    return lambda x: x in range(*args)

def inSet(*ss):
    return lambda x: x in ss

#Implementation de 8bin_pr de Order-pp
def bin_pr(f):
    """Projection binaire

    Args:
        f (fonction binaire): opération principale
        pr (fonction unaire): fonction projectrice
        a (Any): opérand de gauche de f
        b (Any): opérand de droite de f
    
    Returns:
        
    """
    return lambda pr: lambda a: lambda b: f(pr(a), pr(b))

def liftM2(h):
    """liftM2: list monadic binaire de Haskell, sans monad :'(
    
    Args:

    """
    return lambda f: lambda g: lambda x: h(f(x), g(x))

def unlines(xs: Sequence) -> str:
    return reduce(lambda r, x: r + "\n" + x, xs)

#interleave("123", " | ")
def interleave(xs: str, y: str) -> str:
    return xs[0] + "".join(map(op.__add__, repeat(y), xs[1:]))

# the pattern "x if x != None else foo" comes way too often
def default(x: Any, ret: Any=None, case: Any = None):
    return x if x != case else ret

def map_2d(f: Callable[[A], B], xss: Sequence[Sequence[A]]) -> Sequence[Sequence[B]]:
    return list(map(lambda xs: list(map(f, xs)), xss))


# Voici la représentation des Gobblets, n'hésitez pas à l'utiliser.
# 1 pour le joueur 1, 2 pour le joueur 2.
GOBBLET_REPRÉSENTATION = {
    1: ["▫", "◇", "◯", "□"],
    2: ["▪", "◆", "●", "■"],
}


class GobbletError(Exception):
    """
    Cette exception est pour les erreurs de Gobblet. 
    """
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return f'GobbletError: {self.message}'


class Gobblet:
    """
    Gobblet
    """

    def __init__(self, grosseur, no_joueur):
        """Constructeur de gobelet.

        Ne PAS modifier cette méthode.

        Args:
            grosseur (int): Grosseur du Gobblet [0, 1, 2, 3].
            no_joueur (int): Numéro du joueur [1, 2].
        """
        self.grosseur, self.no_joueur = self.valider_gobblet(grosseur, no_joueur)

    def valider_gobblet(self, grosseur, no_joueur):
        """Validateur de gobelet.

        Args:
            grosseur (int): la grosseur du gobelet [0, 1, 2, 3].
            no_joueur (int): le numéro du joueur [1, 2].

        Returns:
            tuple[int, int]: un tuple contenant la grosseur et le numéro du joueur.

        Raises:
            *GobbletError: La grosseur doit être un entier.
            *GobbletError: La grosseur doit être comprise entre 0 et 3.
            *GobbletError: Le numéro du joueur doit être un entier.
            *GobbletError: Le numéro du joueur doit être 1 ou 2.
        """
        if not isinstance(grosseur) is int:
            raise GobbletError("La grosseur doit être un entier.")
        elif not (0 <= grosseur <= 3):
            raise GobbletError("La grosseur doit être comprise entre 0 et 3.")
        elif not isinstance(no_joueur) is int:
            raise GobbletError("La grosseur doit être comprise entre 0 et 3.")
        elif not no_joueur in [1, 2]:
            raise GobbletError("Le numéro du joueur doit être 1 ou 2.")
        return grosseur, no_joueur

    def __str__(self):
        """Formater un gobelet.

        Returns:
            str: Représentation du gobelet pour le joueur.
        """
        return GOBBLET_REPRÉSENTATION.get(self.no_joueur)[self.grosseur]

    def __eq__(self, autre):
        """Comparer l'équivalence de deux gobelets.

        Args:
            autre (Gobblet | None): None ou Gobblet à comparer.

        Returns:
            bool: si les deux gobelets sont de même taille.
        """
        return (self.grosseur == autre.grosseur) if isinstance(autre) is Gobblet else False

    def __gt__(self, autre):
        """Comparer la grosseur de deux gobelets.

        Args:
            autre (Gobblet | None): None ou Gobblet à comparer.

        Returns:
            bool: si ce gobelet est plus gros que l'autre.
        """
        return self.grosseur > autre.grosseur if isinstance(autre) is Gobblet else False

    def __lt__(self, autre):
        """Comparer la grosseur de deux gobelets.

        Args:
            autre (Gobblet | None): None ou Gobblet à comparer.

        Returns:
            bool: si ce gobelet est plus petit que l'autre.
        """
        return not (self > autre or self == autre)

    def __ne__(self, autre):
        """Comparer l'équivalence de deux gobelets.

        Args:
            autre (Gobblet | None): None ou Gobblet à comparer.

        Returns:
            bool: si ce gobelet n'est pas équivalent à l'autre.
        """
        return not (self == autre)

    def __ge__(self, autre):
        """Comparer la grosseur de deux gobelets.

        Args:
            autre (Gobblet | None): None ou Gobblet à comparer.

        Returns:
            bool: si ce gobelet est plus grand ou égal à l'autre.
        """
        return not (self < autre)

    def __le__(self, autre):
        """Comparer la grosseur de deux gobelets.

        Args:
            autre (Gobblet | None): None ou Gobblet à comparer.

        Returns:
            bool: si ce gobelet est plus petit ou égal à l'autre.
        """
        return not (self > autre)

    def état_gobblet(self):
        """Obtenir l'état du gobelet.

        Returns:
            list: la paire d'entiers représentant l'état du gobelet (numéro du joueur et grosseur du gobelet).
        """
        return [self.no_joueur, self.grosseur]

    def formater_un_gobblet(self):
        return str(self)


def interpréteur_de_commande():
    """Interpreteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut IDUL représentant l'idul du joueur
                   et l'attribut lister qui est un booléen True/False.
    """
    parser = ArgumentParser(description="Gobblet")
    parser.add_argument("IDUL", help="IDUL du joueur", isinstance=str)
    parser.add_argument("-l", "--lister", action="store_true", help="lister les parties existantes")

    return parser.parse_args()


from joueur import Joueur

def formater_jeu(plateau, joueurs: list[Joueur]):
    """Formater un jeu.

    Args:
        plateau (Plateau): le plateau de jeu.
        joueurs (Joueur): la liste des deux Joueurs.

    Returns:
        str: Représentation du jeu.
    """
    nomLens = list(map(lambda j: len(j.nom), joueurs))
    minLen, maxLen = tuple(sorted(nomLens))

    jr = list(map(lambda l, j: " " * (maxLen - l), nomLens, joueurs))

    
    jeu = " " * (maxLen + 3) + "0   1   2 \n"

    jeu += jr[0] + str(joueurs[0]) + " \n"
    jeu += jr[1] + str(joueurs[1]) + " \n"
    jeu += "\n"

    jeu += plateau.formater_plateau()

    return jeu


def formater_les_parties(parties):
    """Formater une liste de parties.

    L'ordre doit être exactement la même que ce qui est passé en paramètre.

    Args:
        parties (list): une liste des parties.

    Returns:
        str: Représentation des parties.
    """
    def vs(joueur1, joueur2):
        return joueur1 + " vs " + joueur2

    def frmt(n, parties):
        date = parties.get('date')
        versus = vs(*parties.get('joueurs'))
        gagnant = ', ' + parties.get('gagnant') if parties.get('gagnant') != None else ''
        return f"{n} : {date}, {versus}{gagnant}"


    return unlines(map(frmt, count(), parties))