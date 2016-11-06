"""
DungeonRoll_sopel, le jeu de dés Dungeon Roll adapté pour irc
Auteurs: Kuun-Lann & Louc
2016
"""

# dépendances pour le jeu
import random
from time import sleep  # pour la version irc

# dépendances pour irc (sopel)
import sopel.module
from sopel.module import commands, thread, rule, example


class DungeonRollGame:

    class QuitOrderException(Exception):
        def __init__(self):
            super().__init__(self)

    class DéJoueur:
        """Structure d'organisation des dés du joueur, de qu'il est possible de faire avec un dé"""
        def __init__(self, nom, type_dé, action_type=None, cible_favorite=None):
            self.nom = nom
            self.type_dé = type_dé
            self.action_type = action_type
            self.cible_favorite = cible_favorite

        def __str__(self):
            return self.nom

        def __repr__(self):
            return self.nom

    class MainJoueur:
        pass
        # à développer pour optimiser (avec prise en charge de l'inventaire, du cimetière ..)

    def __init__(self, bot):
        """Initialise une partie de DungeonRoll"""

        # Pour permettre les réponses sur irc
        self.bot = bot

        # Declaration des items trouvables dans les dés et des loot pour les random
        self.compagnons = [
            self.DéJoueur("Guerrier", "Compagnon", "Guerrier", "Gobelin"),
            self.DéJoueur("Voleur", "Compagnon", "Voleur"),
            self.DéJoueur("Mage", "Compagnon", "Mage", "Blob"),
            self.DéJoueur("Clerc", "Compagnon", "Clerc", "Squelette"),
            self.DéJoueur("Champion", "Compagnon", "Champion", ("Squelette", "Blob", "Gobelin")),
            self.DéJoueur("Parchemin", "Compagnon", "Parchemin")     # On peut relancer autant de dé qu'on veut
        ]
        self.tresors = [
            self.DéJoueur('Portail de ville', "Trésor", "Portail de ville"),             # Fin de la partie avec décompte des points
            self.DéJoueur('Appat de Dragon', "Trésor", "Appat de Dragon"),               # transforme les dés monstres en dé dragon
            self.DéJoueur("Anneau d'invisibilité", "Trésor", "Anneau d'invisibilité"),   # retire les dés de l'antre du dragon (ne le vainc pas)
            self.DéJoueur('Potion', "Trésor", "Potion"),                                 # permet de récupérer 1 seul dé joueur
            self.DéJoueur('Parchemin', "Trésor", "Parchemin"),                           # = dé parchemin
            self.DéJoueur('Epée Vorpale', "Trésor", "Guerrier", "Gobelin"),              # = dé guerrier
            self.DéJoueur('Talisman', "Clerc", "Trésor", "Squelette"),                   # = dé clerc
            self.DéJoueur('Sceptre de Pouvoir', "Trésor", "Mage", "Blob"),               # = dé mage
            self.DéJoueur('Outil de Voleur', "Trésor", "Voleur"),                        # = dé voleur
            self.DéJoueur('Ecaille du dragon', "Trésor", "Ecaille du dragon")            # chaque écaille vaut 1 pt XP, chaque paire vaut +2 XP
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
        self.cimetiere = []
        self.antre_dragon = []
        self.monstres = []
        self.loot = []
        self.player_hand = []
        self.des_dragon = []

        # Declaration du niveau du hero et du donjon au debut du jeu
        self.niveau_donjon = 6
        self.niveau_hero = 1
        self.XP = 0  # mais il s'agit pas de windows

        # Déclaration des états de la partie
        self.attente_joueur = False
        self.msg_joueur = ""
        self.stop = False
        self.continuer_partie = False
        self.exploration = "Echec"

    def start(self):
        """Lance une partie de DungeonRoll"""
        # Lancement des dés du joueur
        self.afficher(
            "Bienvenue dans le Donjon. Vous etes niveau " + str(self.niveau_hero) + ". Voyons qui vous accompagne :")
        for i in range(0, 7):
            self.lance_dé_joueur()

        # Tour de jeu
        try:
            self.continuer_partie = True
            while self.continuer_partie:
                self.entrer_dans_donjon()
                if self.gerer_phase_baston() == "Succes":
                    self.piller_butin()
                    self.reflechir_avenir()
            self.clore_la_partie()
        except self.QuitOrderException:
            self.afficher("Le jeu s'arrête brutalement, aucun score n'est enregistré")

    def clore_la_partie(self):
        """Fin de la partie => calcul score"""
        self.afficher("C'est la FIN")

        if self.exploration == "Succes":
            # calcul du score
            self.afficher("Calcul du score")

            # chaque tresor vaut un point
            inventaire = [i for i in self.player_hand if i.type_dé == "Trésor"]
            score = len(inventaire)
            # le Town portal en vaut 2
            for tresor in inventaire:
                if tresor == "Portail de ville":
                    score += 1
                        
            # écailles de dragon : chaque pair vaut 2 pts de plus
            # 1 ecaille = 0 pt en plus
            # 2 ecaills = 2 pt en plus
            # 3 écaills = 2 pt en plus
            # 4 écailles = impossible, t'as triché :p 4 pt en plus
            ecailles = 0
            for tresor in inventaire:
                if tresor == "Ecaille du dragon":
                    ecailles += 1
            score += (ecailles // 2) * 2    

            # 1 pt XP = 1 pt score
            score += self.XP

            # le niveau du donjon 
            score += self.niveau_donjon

            # GREAT, c'est un super SCORE !
            self.afficher("Le score est de : " + str(score))

        else:
            self.afficher("C'est la FIN, t'as perdu, 0 point !")

        # peut être un peu violent ? ça marche en console en tt cas
        #exit()

    def entrer_dans_donjon(self):
        """Arrivée dans un nouveau niveau du donjon"""
        self.afficher("Vous arrivez au niveau " + str(self.niveau_donjon) + ". Des monstres apparaissent !")

        # Lancement de des du MJ
        self.monstres = []
        self.loot = []
        for i in range(self.niveau_donjon):
            self.lancer_dé_MJ()
        self.verifier_dragon()

    def gerer_phase_baston(self):
        """Faut bousiller tous les monstres avant de continuer"""

        # par défaut on réussit car il y a un seul critère d'échec: la fuite
        self.exploration = "Succes"

        # boucle tant qu'il y a des monstres ou un dragon
        while self.monstres or self.antre_dragon:
            # afficher les mains
            self.afficher_main_joueur()
            self.afficher_main_MJ()

            # Filtrer les actions possibles : TBD
            # Dragon : avoir 3 compagnons différents
            # utiliser Compagnon : avoir des compagnons dispo
            # etc..
            
            # Choisir une action 
            possibilites = ["utiliser un TRésor", "utiliser un COmpagnon", "FUir", "affronter le DRagon"]
            self.afficher(str(possibilites))
            choix = self.recuperer("Que souhaitez-vous faire ?")
            self.afficher("vous avez choisi : " + choix)

            # Résolution de l'action
            if choix in ("FU", "Fu", "fu", "Fuir", "FUir", "fuir", "F", "f"):
                self.continuer_partie = False
                self.exploration = "Echec"
                break
            elif choix in ("TR", "Tr", "tr", "TRésor", "Trésor", "trésor", "TResor", "Tresor", "tresor", "T", "t"):
                self.utiliser_tresor()
            elif choix in ("COmpagnon", "Compagnon", "compagnon", "C", "c", "CO", "Co", "co"):
                self.utiliser_compagnon()
            elif choix in ("DR", "DRagon", "Dr", "dr", "Dragon", "dragon", "D", "d"):
                self.affronter_dragon()

        return self.exploration  # "Echec" ou "Succes"

    def affronter_dragon(self):
        """il faut 3 bonhommes différents"""

        # on vérifie qu'on a trois choses différentes en passant par un ensemble (ne contient que des objets uniques)
        main_objets_uniques = set(self.player_hand)
        if len(main_objets_uniques) < 3 :
            self.afficher("Combat contre le dragon impossible, vous n'avez pas 3 compagnons/objets différents")
            return

       # on choisit 3 "objets" différents (grace à l'ensemble)
        for i in range(0,3):
            choix = self.choisir_par_index(main_objets_uniques)
            main_objets_uniques.remove(choix)
            self.player_hand.remove(choix)

        # Tuer le dragon
        self.antre_dragon = []
        self.afficher("Couic, dragon bousillé")

        # récupère 1 trésor
        tresor = random.choice(self.tresors)
        self.player_hand.append(tresor)
        self.afficher("Vous avez trouvé : " + str(tresor))

        # gagner 1 pt XP
        self.XP += 1

    def utiliser_tresor(self):
        inventaire = [i for i in self.player_hand if i.type_dé == "Trésor"]

        # choix trésor
        tresor = self.choisir_par_index(inventaire)

        # on le retire tout de suite de l'inventaire
        self.player_hand.remove(tresor)

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
            self.utiliser_parchemin("trésor")

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
            self.player_hand.append("Ecaille du dragon")

    def piller_butin(self):
        """Les monstres vaincus, on peut piller la salle"""
        while True:
            # Reste-t-il du loot ?
            if not self.loot:
                break

            # choix action = coffre ou potion (dé) ou  abandonner le loot
            self.afficher_main_joueur()
            self.afficher_main_MJ()
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

                # on a bu la potion, la bouteille est vide !
                self.loot.remove("Potion")

            elif choix in ("COffre", "Coffre", "coffre", "CO", "Co", "co", "C", "c"):
                if "Coffre" not in self.loot:
                    self.afficher("Y'a pas de Coffre, boulet va !")
                    continue  # go to the next iteration (while) => reproposer les actions

                # rappel de la règle
                self.afficher("Utilisez n'importe lequel de vos compagnons pour ouvrir un coffre,")
                self.afficher("un voleur pour les ouvrir tous")

                dé_utilisables = [i for i in self.player_hand if i.cible_favorite is not None]

                dé = self.choisir_par_index(dé_utilisables)

                # action = ouvrir un ou plusieurs coffres
                if dé.action_type == "Voleur":
                    # décompte du nombre de coffres
                    nb_coffres = self.loot.count("Coffre")

                    for i in range(nb_coffres):
                        self.ouvrir_coffre()

                else:
                    if "Coffre" in self.loot:
                        self.ouvrir_coffre()

                # retirer le dé utilisé et le placer au cimetière si c'est un compagnon
                self.player_hand.remove(dé)
                if dé.type_dé == "Compagnon":
                    self.cimetiere.append(dé)

            elif choix in ("ABandonner", "Abandonner", "abandonner", "AB", "Ab", "ab", "A", "a"):
                break

    def ouvrir_coffre(self):
        self.loot.remove("Coffre")

        # tirer trésor
        tresor = random.choice(self.tresors)
        self.player_hand.append(tresor)
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

        if compagnon.action_type == "Parchemin":
            self.utiliser_parchemin("dé")
        else:
            self.bastonner(compagnon)

    def choisir_par_index(self, liste, msg="Lequel ?"):
        # choix du compagnon par l'index
        while True:
            for i, value in enumerate(liste):
                self.afficher(str(i) + " : " + str(value))
            try:    
                choix = int(self.recuperer(msg))
                if 0 <= choix < len(liste) :
                    choix = liste[choix]
                    self.afficher('Vous avez choisi : ' + str(choix))
                    return choix
            except:
                pass
            else:
                self.afficher("Mauvaise saisie, recommencez !")

    def lancer_dé_MJ(self):
        """Lance un dé du MJ, et l'ajoute dans la bonne main du MJ, retourne le dé tiré"""
        lancer_de = random.choice(self.mjdice)
        # on range le dé dans le bon conteneur selon le type tiré
        if lancer_de == "Dragon":
            self.des_dragon.append(lancer_de)
        elif lancer_de in ("Coffre", "Potion"):
            self.loot.append(lancer_de)
        else:
            self.monstres.append(lancer_de)
        return lancer_de

    def lance_dé_joueur(self):
        """Lance un DéJoueur et l'ajoute dans la main du joueur, retourne le dé tiré"""
        lancer_dé = random.choice(self.compagnons)
        self.player_hand.append(lancer_dé)
        return lancer_dé

    def utiliser_parchemin(self):
        # Gestion du cas parchemin : on relance un dé quelqu'il soit sauf Dragon
        self.afficher("Vous pouvez relancer un dé")

        compagnons = [i for i in self.player_hand if i.type_dé == "Compagnon"]

        # afficher avec un index successivement les mains du joueur, du mj (loot, monstres)
        for i in range(len(compagnons) + len(self.loot) + len(self.monstres)):
            if i < len(compagnons):
                self.afficher(str(i) + " : " + str(compagnons[i]))
            elif i < len(compagnons) + len(self.loot):
                self.afficher(str(i) + " : " + str(self.loot[i - len(compagnons)]))
            else:
                self.afficher(str(i) + " : " + str(self.monstres[i - len(compagnons) - len(self.loot)]))

        # choisir le dé à relancer
        choix = self.recuperer("Quel dé voulez-vous relancer ?")
        choix = int(choix)

        # enlever ce dé et selon la catégorie relancer le dé et l'affecter dans la bonne main
        ajouté = ""
        if choix < len(compagnons):
            # player_hand
            choix = compagnons[choix]
            self.player_hand.remove(choix)
            ajouté = self.lance_dé_joueur()
        elif choix < len(compagnons) + len(self.loot):
            # loot
            choix = self.loot[choix - len(compagnons)]
            self.loot.remove(choix)
            ajouté = self.lancer_dé_MJ()
        else:
            # monstres
            choix = self.monstres[choix - len(compagnons) - len(self.loot)]
            self.monstres.remove(choix)
            ajouté = self.lancer_dé_MJ()

        # afficher les changements
        self.afficher("Vous avez choisi de relancer : " + str(choix))
        self.afficher(ajouté + " a été tiré")

        self.verifier_dragon()

    def bastonner(self, compagnon):
        # choix de la cible
        cible = self.choisir_par_index(self.monstres, "ON BUTE QUI ?")

        # creation de cadavres
        if cible in compagnon.cible_favorite:
            # cible favorite : on supprime tous les monstres similaires
            while cible in self.monstres:
                self.monstres.remove(cible)
        else:
            # on n'en supprime qu'un
            self.monstres.remove(cible)

    def verifier_dragon(self):
        """Si il y a 3 dé dragon ou plus, un dragon apparait et tous les dés sont défaussés""" 
        if len(self.des_dragon) >= 3:
            self.afficher("AND HIS NAME IS BIG DRAGON")
            self.des_dragon = []
            self.antre_dragon.append("Dragon")

    def afficher_main_joueur(self):
        compagnons = [dé for dé in self.player_hand if dé.type_dé == "Compagnon"]
        trésors = [i for i in self.player_hand if i.type_dé == "Trésor"]
        self.afficher("Compagnons : " + str(compagnons))
        self.afficher("cimetiere : " + str(self.cimetiere))
        self.afficher("inventaire : " + str(trésors))
        return

    def afficher_main_MJ(self):
        self.afficher("Antre du dragon : " + str(self.antre_dragon))
        self.afficher("Nid du dragon : " + str(self.des_dragon))
        self.afficher("Loot : " + str(self.loot))
        self.afficher("Monstres : " + str(self.monstres))

    def afficher(self, msg):
        """méthode pour afficher les textes du jeu au joueur"""
        # playing in console
        # print(msg)

        self.bot.say(msg, "#game")

    def recuperer(self, msg):
        """méthode pour récupérer les input du joueur. Surveille aussi les demandes de fin de partie"""

        # playing in console
        # return input(msg + " : ")

        # indique qu'on attend qque chose
        self.attente_joueur = True
        self.msg_joueur = ""

        # on prévient le joueur qu'on attend sa réponse
        self.afficher(msg)

        # attente de la réponse du joueur
        while True:
            # réponse du joueur
            if self.msg_joueur != "":
                break

            # ordre d'arrêter
            if self.stop:
                raise self.QuitOrderException()

            # petite pause pour pas monopoliser les ressources
            sleep(0.2)

        self.attente_joueur = False
        self.msg_joueur = ""
        return self.msg_joueur


# Variables globales décrivant l'état du jeu
INSTANCE = None
EN_COURS = False
JOUEUR = None      # nickname du joueur


# pour interagir avec le jeu : le lancer, l'arreter, voir son état
@commands("dungeon")
@thread(True)  # non bloquant, permet d'executer simultanément d'autres triggers sopel
def dungeon(bot, trigger):
    """Le jeu de dé Dungeon Roll adapté pour irc. Le but : explorer le donjon et amasser le plus grand score !"""
    global INSTANCE, EN_COURS, JOUEUR

    if not trigger.group(2):
        for msg in [".dungeon start : lance le jeu",
                    ".dungeon stop : interrompt le jeu",
                    ".dungeon etat : pour avoir des détails sur l'instance du jeu (jeu en cours, joueur..",
                    ".dungeon highscore : affiche le meilleur score",
                    ".dungeon stats : afficher les stats des joueurs"]:
            bot.say(msg)
        return

    # tri des commandes
    cmd = trigger.group(2)
    if cmd == "start":
        # on ne commence une partie que si on est sur le canal #game
        if trigger.sender != "#game":
            return bot.say("la partie ne peut se jouer que dans le canal #game")

        # on vérifie si une partie n'est pas déjà en cours
        if EN_COURS:
            return bot.say("Une partie est déjà en cours")

        # il n'y a pas de partie en cours, on peut en commencer une
        JOUEUR = trigger.nick
        EN_COURS = True
        INSTANCE = DungeonRollGame(bot)
        INSTANCE.start()
        EN_COURS = False

    elif cmd == "stop":
        """on arrete brutalement le jeu"""
        # on vérifie que le jeu est bien en cours
        if EN_COURS:
            INSTANCE.stop = True
            EN_COURS = False
            return

    elif cmd == "etat":
        return bot.say("Fonction non implémentée")
    elif cmd == "highscore":
        return bot.say("Fonction non implémentée")
    elif cmd == "stats":
        return bot.say("Fonction non implémentée")
    else:
        for msg in [".dungeon start : lance le jeu",
                    ".dungeon stop : interrompt le jeu",
                    ".dungeon etat : pour avoir des détails sur l'instance du jeu (jeu en cours, joueur..",
                    ".dungeon highscore : affiche le meilleur score",
                    ".dungeon stats : afficher les stats des joueurs"]:
            bot.say(msg)
        return


# pour les interactions requises par le jeu
@rule('(^[^\.])+.*')  # on récupère tout ce qui n'est ni vide, ni commençant par un '.'
def interagir_dungeon(bot, trigger):
    """Pour que le jeu récupère les input des joueurs"""
    global INSTANCE, EN_COURS, JOUEUR

    # on n'écoute que si le jeu est en cours
    if not EN_COURS:
        return

    # on n'écoute que si le canal est #game
    if trigger.sender != "#game":
        return

    # on n'écoute que le joueur de la partie
    if trigger.nick != JOUEUR:
        return

    # on transmet ce qu'à dit le joueur à l'instance du jeu si l'INSTANCE attend qque chose
    if INSTANCE.attente_joueur:
        INSTANCE.msg_joueur = trigger.group(0)


if __name__ == "__main__":
    partie = DungeonRollGame(None)
    partie.start()
