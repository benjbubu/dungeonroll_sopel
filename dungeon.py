import random


class DungeonRollGame:

    def __init__(self):
        # Declaration des items trouvables dans les de et des loot pour les random
        # self.playerdice = ['Guerrier', 'Voleur', 'Mage', 'Clerc', 'Champion', 'Parchemin']
        self.compagnons = {
            "Guerrier"  : [ "Gobelin" ],
            "Voleur"    : [],
            "Mage"      : [ "Blob" ],
            "Clerc"     : [ "Squelette" ],
            "Champion"  : [ "Gobelin", "Blob", "Squelette"],
            "Parchemin" : []
        }
        self.mjdice = ['Gobelin', 'Blob', 'Squelette', 'Coffre', 'Dragon', 'Potion']
        self.tresor = [
                'Portail de ville',     # Fin de la partie avec décompte des points
                'Appat de Dragon',      # transforme les dés monstres en dé dragon
                'Anneau dinvisibilite', # retire les dés de l'antre du dragon (ne le vainc pas)
                'Potion',               # permet de récupérer 1 seul dé joueur
                'Parchemin',            # = dé parchemin
                'Epee Vorpale',         # = dé guerrier
                'Talisman',             # = dé clerc
                'Sceptre de Pouvoir',   # = dé mage 
                'Outil de Voleur',      # = dé voleur
                'Ecaille du dragon'     # chaque écaille vaut 1 pt XP, chaque paire vaut +2 XP
                ]
        self.antre_dragon = []

        # Declaration du niveau du hero et du donjon au debut du jeu
        self.niveau_donjon = 9
        self.niveau_hero = 1

        # Lancement des dés du joueur
        self.afficher("Bienvenue dans le Donjon. Vous etes niveau " + str(self.niveau_hero) + ". Voyons qui vous accompagne")
        self.player_hand = []
        for i in range(1, 7):
            self.lancer_dé_joueur()

        # Initialisation de l'inventaire pour récupérer les trésors
        self.inventaire = []

        # Initialisation du cimetière (=dé joueurs utilisés)
        self.cimetiere = []
            
        # Tour de jeu
        self.continuer_partie = True
        while self.continuer_partie:
            self.entrer_dans_donjon()
            if self.gerer_baston() == "Succes":
                self.piller_butin()
                self.reflechir_avenir()
            
        # Fin de la partie => calcul score 
        self.afficher("C'est la FIN")

    def entrer_dans_donjon(self):
        self.afficher("Vous arrivez au niveau " + str(self.niveau_donjon) + ". Des monstres apparaissent !")

        # Lancement de des du MJ
        self.monstres = []
        self.loot = []
        for i in range(self.niveau_donjon):
            self.lancer_dé_MJ()

    def gerer_baston(self):
        exploration = "Succes"
        while self.monstres:
            # afficher les mains
            self.afficher_main_joueur()
            self.afficher_main_MJ()

            # Choisir une action 
            possibilites = ["utiliser un TRésor", "utiliser un COmpagnon", "FUir"]
            self.afficher(str(possibilites))
            choix = self.recuperer("Que souhaitez-vous faire ?")

            self.afficher("vous avez choisi : " + choix) 
            
            # Résolution de l'action
            if choix in ("FU", "Fuir", "FUir", "fuir", "F", "f"):
                self.continuer_partie = False
                exploration = "Echec"
                break
            elif choix in ("TR", "TRésor", "Trésor", "trésor", "TResor", "Tresor", "tresor", "T", "t"):
                self.afficher("Fonction non implémentée")
            elif choix in ("COmpagnon", "Compagnon", "compagnon", "C", "c"):
                self.utiliser_compagnon()

        return exploration  # "Echec" ou "Succes"

    def piller_butin(self):
        pass

    def reflechir_avenir(self):
        # donjon max = niv 10 => fin de la partie
        if self.niveau_donjon >= 10:
            self.continuer_partie = False
            self.afficher("Niveau 10 atteint, c'est la fin de la partie !")
            return

        # choisir entre continuer et partir
        choix = self.recuperer("Vous pouvez COntinuer l'aventure ou vous REtirer...")
        if choix in ("COntinuer", "Continuer", "Continuer", "C", "c"):
            # La partie continue
            self.niveau_donjon += 1
        else:
            self.continuer_partie = False

    def utiliser_compagnon(self):
        # choix du compagnon
        for i in range(len(self.player_hand)):
            self.afficher(str(i) + " : " + str(self.player_hand[i]))
        compagnon = self.player_hand[int(self.recuperer("Lequel ?"))]

        # retirer le compagnon utilisé et le place au cimetière
        self.player_hand.remove(compagnon)
        self.cimetiere.append(compagnon)

        if compagnon == "Parchemin" :
            self.utiliser_parchemin()
        else:
            self.bastonner(compagnon)

    def lancer_dé_MJ(self):
        # Lancer le dé du mj
        lancer_de = random.choice(self.mjdice)
        if lancer_de == "Dragon":
            self.antre_dragon.append(lancer_de)
        elif lancer_de in ("Coffre", "Potion"):
            self.loot.append(lancer_de)
        else:
            self.monstres.append(lancer_de)
        return lancer_de

    def lancer_dé_joueur(self):
        lancer_dé = random.choice(list(self.compagnons.keys()))
        self.player_hand.append(lancer_dé)
        return lancer_dé

    def utiliser_parchemin(self):
        # Gestion du cas parchemin : on relance un dé quelqu'il soit sauf Dragon
        self.afficher("Vous pouvez relancer un dé")

        # afficher avec un index successivement les mains du joueur, du mj (loot, monstres)
        for i in range(len(self.player_hand) + len(self.loot) + len(self.monstres)):
            if i < len(self.player_hand):
                self.afficher(str(i) + " : " + str(self.player_hand[i]))
            elif i < len(self.player_hand) + len(self.loot):
                self.afficher(str(i) + " : " + str(self.loot[i - len(self.player_hand)]))
            else:
                self.afficher(str(i) + " : " + str(self.monstres[i - len(self.player_hand) - len(self.loot)]))

        # choisir le dé à relancer
        choix = self.recuperer("Quel dé voulez-vous relancer ?")
        choix = int(choix)

        # enlever ce dé et selon la catégorie relancer le dé et l'affecter dans la bonne main
        ajouté = ""
        if choix < len(self.player_hand):
            # player_hand
            choix = self.player_hand[choix]
            self.player_hand.remove(choix)
            ajouté = self.lancer_dé_joueur()
        elif choix < len(self.player_hand) + len(self.loot):
            # loot
            choix = self.loot[choix - len(self.player_hand)]
            self.loot.remove(choix)
            ajouté = self.lancer_dé_MJ()
        else:
            # monstres
            choix = self.monstres[choix - len(self.player_hand) - len(self.loot)]
            self.monstres.remove(choix)
            ajouté = self.lancer_dé_MJ()

        # afficher les changements
        self.afficher("Vous avez choisi de relancer : " + choix)
        self.afficher(ajouté + " a été tiré")

    def bastonner(self, compagnon):
        # choix de la cible
        self.afficher(self.monstres)
        cible = self.recuperer("ON BUTE QUI ?")

        # creation de cadavres
        if cible in self.compagnons[compagnon]:
            # cible favorite : on supprime tous les monstres similaires
            while cible in self.monstres:
                self.monstres.remove(cible)
        else:
            # on n'en supprime qu'un
            self.monstres.remove(cible)

    def afficher_main_joueur(self):
        self.afficher("main joueur : " + str(self.player_hand))
        self.afficher("cimetiere : " + str(self.cimetiere))

    def afficher_main_MJ(self):
        self.afficher(str(self.antre_dragon) + str(self.loot) + str(self.monstres))

    def afficher(self, msg):
        print(msg)

    def recuperer(self, msg):
        return input(msg + " : ")


if __name__ == "__main__":
    DungeonRollGame()


