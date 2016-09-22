import random


class DungeonRollGame:

    class Déjoueur:
        """Structure d'organisation des dés du joueur, de qu'il est possible de faire avec un dé"""
        def __init__(self, nom, action_type):
            self.nom = nom
            self.action_type = action_type

    def __init__(self):
        """Initialise une partie de DungeonRoll"""

        # Declaration des items trouvables dans les dés et des loot pour les random
        self.compagnons = [
            self.Déjoueur("Guerrier", "Guerrier"),
            self.Déjoueur("Voleur", "Voleur"),
            self.Déjoueur("Mage", "Mage"),
            self.Déjoueur("Clerc", "Clerc"),
            self.Déjoueur("Champion", "Champion"),
            self.Déjoueur("Parchemin", "Parchemin")
        ]
        self.tresor = [
            self.Déjoueur('Portail de ville', "Portail de ville"),             # Fin de la partie avec décompte des points
            self.Déjoueur('Appat de Dragon', "Appat de Dragon"),               # transforme les dés monstres en dé dragon
            self.Déjoueur("Anneau d'invisibilité", "Anneau d'invisibilité"),   # retire les dés de l'antre du dragon (ne le vainc pas)
            self.Déjoueur('Potion', "Potion"),                                 # permet de récupérer 1 seul dé joueur
            self.Déjoueur('Parchemin', "Parchemin"),                           # = dé parchemin
            self.Déjoueur('Epée Vorpale', "Guerrier"),                         # = dé guerrier
            self.Déjoueur('Talisman', "Clerc"),                                # = dé clerc
            self.Déjoueur('Sceptre de Pouvoir', "Mage"),                       # = dé mage
            self.Déjoueur('Outil de Voleur', "Voleur"),                        # = dé voleur
            self.Déjoueur('Ecaille du dragon', "Ecaille du dragon")            # chaque écaille vaut 1 pt XP, chaque paire vaut +2 XP
        ]
        self.mjdice = [
            'Gobelin',
            'Blob',
            'Squelette',
            'Coffre',       # utiliser un compagnon pour en ouvrir un, un voleur pour les ouvrir tous - donne un trésor
            'Dragon',
            'Potion'        # Utiliser un compagnon pour récupérer, Usage immédiat, réssuscite tous les compagnons du cimetière
        ]

        # Initialisation des différents conteneurs de dés ou objets
        self.inventaire = []
        self.cimetiere = []
        self.antre_dragon = []
        self.monstres = []
        self.loot = []
        self.player_hand = []
        self.des_dragons = []

        # Declaration du niveau du hero et du donjon au debut du jeu
        self.niveau_donjon = 6
        self.niveau_hero = 1
        self.XP = 0  # mais il s'agit pas de windows

        # Déclaration des états de la partie
        self.continuer_partie = False
        self.exploration = "Echec"

    def start(self):
        """Lance une partie de DungeonRoll"""
        # Lancement des dés du joueur
        self.afficher(
            "Bienvenue dans le Donjon. Vous etes niveau " + str(self.niveau_hero) + ". Voyons qui vous accompagne :")
        for i in range(1, 7):
            self.lance_dé_joueur()

        # Tour de jeu
        self.continuer_partie = True
        self.exploration = "Succes"
        while self.continuer_partie:
            self.entrer_dans_donjon()
            if self.gerer_phase_baston() == "Succes":
                self.piller_butin()
                self.reflechir_avenir()
        self.clore_la_partie()

    def clore_la_partie(self):
        # Fin de la partie => calcul score
        self.afficher("C'est la FIN")
        if self.exploration == "Succes":
            # calcul du score
            self.afficher("Calcul du score")

            # chaque tresor vaut un point
            score = len(self.inventaire)
            # le Town portal en vaut 2
            for tresor in self.inventaire:
                if tresor == "Portail de ville":
                    score += 1
                        
            # écailles de dragon : chaque pair vaut 2 pts de plus
            # 1 ecaille = 0 pt en plus
            # 2 ecaills = 2 pt en plus
            # 3 écaills = 2 pt en plus
            # 4 écailles = impossible, t'as triché :p 4 pt en plus
            ecailles = 0
            for tresor in self.inventaire:
                if tresor == "Ecaille du dragon":
                    ecailles += 1
            score += (ecailles // 2) * 2    

            # 1 pt XP = 1 pt score
            score += self.XP

            # le niveau du donjon 
            score += self.niveau

            # GREAT, c'est super SCORE !
            self.afficher("Le score est de : " + str(score))

        else:
            self.afficher("C'est la FIN, t'as perdu, 0 point !")

        # peut être un peu violent ? ça marche en console en tt cas
        exit()

    def entrer_dans_donjon(self):
        self.afficher("Vous arrivez au niveau " + str(self.niveau_donjon) + ". Des monstres apparaissent !")

        # Lancement de des du MJ
        self.monstres = []
        self.loot = []
        for i in range(self.niveau_donjon):
            self.lancer_dé_MJ()
        self.verifier_dragon()

    def gerer_phase_baston(self):
        self.exploration = "Succes"
        while self.monstres or self.antre_dragon:
            # afficher les mains
            self.afficher_main_joueur()
            self.afficher_main_MJ()

            # Filtrer les actions possibles :
            # Dragon : avoir 3 compagnons différents
            # utiliser Compagnon : avoir des compagnons dispo
            # etc..
            
            # Choisir une action 
            possibilites = ["utiliser un TRésor", "utiliser un COmpagnon", "FUir", "affronter le DRagon"]
            self.afficher(str(possibilites))
            choix = self.recuperer("Que souhaitez-vous faire ?")
            self.afficher("vous avez choisi : " + choix)

            # Résolution de l'action
            if choix in ("FU", "Fuir", "FUir", "fuir", "F", "f"):
                self.continuer_partie = False
                self.exploration = "Echec"
                break
            elif choix in ("TR", "TRésor", "Trésor", "trésor", "TResor", "Tresor", "tresor", "T", "t"):
                self.utiliser_tresor()
            elif choix in ("COmpagnon", "Compagnon", "compagnon", "C", "c"):
                self.utiliser_compagnon()
            elif choix in ("DR", "DRagon", "Dr", "dr", "Dragon", "dragon", "D", "d"):
                self.affronter_dragon()

        return self.exploration  # "Echec" ou "Succes"

    def affronter_dragon(self):
        """il faut 3 bonhommes différents"""
        choix1 = self.choisir_par_index(self.compagnons)
        choix2 = choix1
        choix3 = choix1
        while choix2 == choix1:
            choix2 = self.choisir_par_index(self.compagnons, "choisissez un compagnon différent") 
        while choix3 == choix2 or choix3 == choix1 :
            choix3 = self.choisir_par_index(self.compagnons, "choisissez un compagnon différent") 

        # on a 3 compagnons différents
        self.compagnons.remove(choix1) 
        self.compagnons.remove(choix2) 
        self.compagnons.remove(choix3)

        # Tuer le dragon
        self.antre_dragon = []
        self.afficher("Couic, dragon bousillé")

        # récupère 1 trésor
        tresor = random.choice(self.tresor)
        self.inventaire.append(tresor)
        self.afficher("Vous avez trouvé : " + str(tresor))

        # gagner 1 pt XP
        self.XP += 1


    def utiliser_tresor(self):
        # choix trésor
        tresor = self.choisir_par_index(self.inventaire)

        # on le retire tout de suite de l'inventaire
        self.inventaire.remove(tresor)

        # résolution de l'action du trésor
        if tresor == 'Portail de ville':     # Fin de la partie avec décompte des points
            self.exploration = "Succes"
            self.clore_la_partie()

        elif tresor == 'Appat de Dragon':    # transforme les dés monstres en dé dragon:
            for i in enumerate(self.monstres):
                self.des_dragon.append("Dragon")
            self.monstres = []
            self.verifier_dragon()

        elif tresor == 'Anneau dinvisibilite': # retire les dés de l'antre du dragon (ne le vainc pas)
            self.des_dragon = []

        elif tresor == 'Potion':               # permet de récupérer 1 seul dé joueur
            self.afficher("Vous pouvez ressusciter un compagnon")
            # choix du compagnon par l'index
            compagnon = self.choisir_par_index(list(self.compagnons.keys()))
            # index = []
            # for i, key in enumerate(self.compagnons.keys()):
            #     self.afficher(str(i) + " : " + key)
            #     index.append(key)
            # compagnon = index[int(self.recuperer("Lequel ?"))]

            # resurection
            self.player_hand.append(compagnon)
            self.cimetiere.pop()

        elif tresor == 'Parchemin':            # = dé parchemin
            self.utiliser_parchemin()

        elif tresor == 'Epee Vorpale':         # = dé guerrier
            self.bastonner("Guerrier")

        elif tresor == 'Talisman':             # = dé clerc
            self.bastonner("Clerc")

        elif tresor == 'Sceptre de Pouvoir':   # = dé mage
            self.bastonner("Mage")

        elif tresor == 'Outil de Voleur':      # = dé voleur
            self.bastonner("Voleur")

        elif tresor == 'Ecaille du dragon':    # chaque écaille vaut 1 pt XP, chaque paire vaut +2 XP
            self.afficher("les Ecailles du dragon comptent dans le décompte des points à la fin de la partie")
            self.inventaire.append("Ecaille du dragon")
            #Retour phase baston car les ecailles ne servent pas au combat
            #elf.gere_phase_baston()

    def piller_butin(self):
        while True:
            # Reste-t-il du loot ?
            if not self.loot:
                break

            # choix action = coffre ou potion (dé) ou  abandonner le loot
            self.afficher_main_joueur()
            choix = self.recuperer("Ouvrez un COffre, buvez une POtion ou ABandonner le loot")

            if choix in ('POtion', "Potion", "potion", "PO", "Po", "po", "P", "p"):
                if "Potion" not in self.loot:
                    self.afficher("Petit boulet, y'a pas de potion !")
                    continue  # go to the next iteration (while) => reproposer les actions

                # rappel de la règle
                self.afficher("Utilisez un compagnon pour boire une potion qui ressuscitera tous les autres compagnons du cimetière")

                compagnon = self.choisir_par_index(self.player_hand)

                # ressusciter tous les compagnons
                for mercenaire in set(self.cimetiere):
                    self.cimetiere.remove(mercenaire)
                    self.player_hand.append(mercenaire)

                # retirer le compagnon utilisé et le placer au cimetière
                self.player_hand.remove(compagnon)
                self.cimetiere.append(compagnon)

            elif choix in ("COffre", "Coffre", "coffre", "CO", "Co", "co", "C", "c"):
                if "Coffre" not in self.loot:
                    self.afficher("Y'a pas de Coffre, boulet va !")
                    continue  # go to the next iteration (while) => reproposer les actions

                # rappel de la règle
                self.afficher("Utilisez n'importe lequel de vos compagnons pour ouvrir un coffre,")
                self.afficher("un voleur pour les ouvrirs tous")

                compagnon = self.choisir_par_index(self.player_hand)

                # action = ouvrir un ou plusieurs coffres
                if compagnon == "Voleur":
                    # décompte du nombre de coffres
                    nb_coffres = self.loot.count("Coffre")

                    for i in range(nb_coffres):
                        self.ouvrir_coffre()

                else:
                    if "Coffre" in self.loot:
                        self.ouvrir_coffre()

                # retirer le compagnon utilisé et le placer au cimetière
                self.player_hand.remove(compagnon)
                self.cimetiere.append(compagnon)

            elif choix in ("ABandonner", "Abandonner", "abandonner", "AB", "Ab", "ab", "A", "a"):
                break

    def ouvrir_coffre(self):
        self.loot.remove("Coffre")

        # tirer trésor
        tresor = random.choice(self.tresor)
        self.inventaire.append(tresor)
        self.afficher("Vous avez trouvé : " + str(tresor))

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
        compagnon = self.choisir_par_index(self.player_hand)

        # retirer le compagnon utilisé et le place au cimetière
        self.player_hand.remove(compagnon)
        self.cimetiere.append(compagnon)

        if compagnon == "Parchemin":
            self.utiliser_parchemin()
        else:
            self.bastonner(compagnon)

    def choisir_par_index(self, liste, msg="Lequel ?"):
        # choix du compagnon par l'index
        while True:
            for i in enumerate(liste):
                self.afficher(str(i) + " : " + str(liste[i]))
            choix = int(self.recuperer(msg))
            if 0 <= choix < len(liste) :
                choix = liste[choix]
                self.afficher('Vous avez choisi : ' + choix)
                return choix
            else:
                self.afficher("Mauvaise saisie, recommencez !")

    def lancer_dé_MJ(self):
        """Lance un dé du MJ, et l'ajoute dans la bonne main du MJ, retourne le dé tiré"""
        lancer_de = random.choice(self.mjdice)
        # on range le dé dans le bon conteneur selon le type tiré
        if lancer_de == "Dragon":
            self.antre_dragon.append(lancer_de)
        elif lancer_de in ("Coffre", "Potion"):
            self.loot.append(lancer_de)
        else:
            self.monstres.append(lancer_de)
        return lancer_de

    def lance_dé_joueur(self):
        """Lance un Déjoueur et l'ajoute dans la main du joueur, retourne le dé tiré"""
        lancer_dé = random.choice(self.compagnons)
        self.player_hand.append(lancer_dé)
        return lancer_dé

    def utiliser_parchemin(self):
        # Gestion du cas parchemin : on relance un dé quelqu'il soit sauf Dragon
        self.afficher("Vous pouvez relancer un dé")

        # afficher avec un index successivement les mains du joueur, du mj (loot, monstres)
        for i in enumerate(self.player_hand + self.loot + self.monstres):
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
            ajouté = self.lance_dé_joueur()
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

        self.verifier_dragon()

    def bastonner(self, compagnon):
        # choix de la cible
        cible = self.choisir_par_index(self.monstres, "ON BUTE QUI ?")

        # creation de cadavres
        if cible in self.compagnons[compagnon]:
            # cible favorite : on supprime tous les monstres similaires
            while cible in self.monstres:
                self.monstres.remove(cible)
        else:
            # on n'en supprime qu'un
            self.monstres.remove(cible)

    def verifier_dragon(self):
        if len(self.des_dragon) >= 3:
            self.afficher("AND HIS NAME IS BIG DRAGON")
            self.des_dragon = []
            self.antre_dragon.append("Dragon") 

    def afficher_main_joueur(self):
        self.afficher("main joueur : " + str(self.player_hand))
        self.afficher("cimetiere : " + str(self.cimetiere))
        self.afficher("inventaire : " + str(self.inventaire))

    def afficher_main_MJ(self):
        self.afficher(str(self.antre_dragon) + str(self.des_dragon) + str(self.loot) + str(self.monstres))

    def afficher(self, msg):
        print(msg)

    def recuperer(self, msg):
        return input(msg + " : ")


if __name__ == "__main__":
    partie = DungeonRollGame()
    partie.start()
