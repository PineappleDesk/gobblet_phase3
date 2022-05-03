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

    def jouer(plateau, id_partie, origine, destination, idul, secret):

        api.débuter_partie(self.idul, self.secret)
        while True:
            tour = 1
            if tour == 1 :
                coup1 = joueur1.récupérer_le_coup(plateau)
                if isinstance(coup1[0]) == int :
                    gobblet.placer_gobblet(coup1[1][0], coup1[1][1], coup1[0])
                else :
                    gobblet.retirer_gobblet(coup1[0][0], coup1[0][1])
                    gobblet.placer_gobblet(coup1[1][0], coup1[1][1])
                tour = 2

            if tour == 2 :
                api.jouer_coup(id_partie, origine, destination, idul, secret)
                tour = 1
            
            with open('Sauvegarde {id_partie}', 'w') as outfile:
                json.dump(plateau.état_plateau(), outfile)