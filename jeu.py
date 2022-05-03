import joueur
import api
import gobblet

class Jeu:
    def __init__(self, idul, secret, id_partie=None, automatique=False):
        self.plateau = plateau
        if automatique :
            self.joueur1 = Automate(Joueur)
        else :
            self.joueur1 = Joueur()
        self.joueur2 = Joueur()
        self.secret = ""
        self.id_partie = ""

        try:
            api.lister_parties(idul, secret)

        except PermissionError():
            raise GobbletError("L'IDUL {idul} n'est pas reconnu par le serveur.")

        if id_partie :
            try :
                api.récupérer_partie(id_partie, idul, secret)
            except RuntimeError():
                raise GobbletError("L'identifiant {id_partie} ne correspond pas à une partie du joueur {idul}.")




    def __str__(self, plateau, joueurs):
        gobblet.formater_jeu(plateau, joueurs)

    def jouer():

        while True:
            tour = 1
            if tour == 1 :
                tour = 2
            if tour == 2 :
                tour = 1