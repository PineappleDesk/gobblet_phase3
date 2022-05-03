"""Module d'API du jeu Gobblet

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * lister_parties - Récupérer la liste des parties reçus du serveur.
    * débuter_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * récupérer_partie - Retrouver l'état d'une partie spécifique.
    * jouer_coup - Exécute un coup et retourne le nouvel état de jeu.
"""

from typing import Union
import requests


URL = "https://pax.ulaval.ca/gobblet/api/"


def lister_parties(idul: str, secret: str) -> list:
    """Lister les parties

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        list: Liste des parties reçues du serveur,
             après avoir décodé le json de sa réponse.
    """
    rep = requests.get(URL + "parties", auth=(idul, secret))

    if rep.status_code == 401:
        raise PermissionError("Erreur levée lorsque le serveur retourne un code 401.")
    
    if rep.status_code == 406:
        raise RuntimeError("Erreur levée lorsque le serveur retourne un code 406.")

    if not rep.status_code in [200, 401, 401]:
        raise ConnectionError("Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406.")

    return rep.json().get("parties")



def débuter_partie(idul: str, secret: str) -> tuple:
    """Débuter une partie

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    rep = requests.post(URL + "partie", auth=(idul, secret))

    if rep.status_code == 401:
        raise PermissionError("Erreur levée lorsque le serveur retourne un code 401.")
    
    if rep.status_code == 406:
        raise RuntimeError("Erreur levée lorsque le serveur retourne un code 406.")

    if not rep.status_code in [200, 401, 401]:
        raise ConnectionError("Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406.")

    partie = rep.json()

    return (partie.get("id"), partie.get("plateau"), partie.get("joueurs"))


def récupérer_partie(id_partie: str, idul: str, secret: str) -> tuple:
    """Récupérer une partie

    Args:
        id_partie (str): identifiant de la partie à récupérer
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    rep = requests.get(URL + "parties", auth=(idul, secret))

    if rep.status_code == 401:
        raise PermissionError("Erreur levée lorsque le serveur retourne un code 401.")
    
    if rep.status_code == 406:
        raise RuntimeError("Erreur levée lorsque le serveur retourne un code 406.")

    if not rep.status_code in [200, 401, 401]:
        raise ConnectionError("Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406.")

    partie: dict = dict(rep.json().get("parties")).get(id_partie)

    return (id_partie, partie.get("plateau"), partie.get("joueurs"))
    

def jouer_coup(id_partie: str, origine: Union[int, str], destination: list[int], idul: str, secret: str) -> tuple:
    """Jouer un coup

    Args:
        id_partie (str): identifiant de la partie
        origine (int ou list): l'origine est soit un entier représentant
                               le numéro de la pile du joueur ou une liste de 2 entier [x, y]
                               représentant le Gobblet sur le plateau.
        destination (list): la destination estune liste de 2 entier [x, y]
                            représentant le Gobblet sur le plateau
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    rep = requests.put(
        URL+'jouer',
        auth=(idul, secret),
        json={
            "id": id_partie,
            "destination": destination,
            "origine": origine,
        }
    )

    if rep.status_code == 401:
        raise PermissionError("Erreur levée lorsque le serveur retourne un code 401.")
    
    if rep.status_code == 406:
        raise RuntimeError("Erreur levée lorsque le serveur retourne un code 406.")

    if rep.status_code == 406:
        raise RuntimeError("Erreur levée lorsque le serveur retourne un code 406.")

    if not rep.status_code in [200, 401, 401]:
        raise ConnectionError("Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406.")
        
    return rep.json()
