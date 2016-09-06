# from unittest import TestCase


#class TestDungeonRollGame(TestCase):
#    pass


import dungeon

# DESCRIPTION DES TESTS

def test_utiliser_tresor():
    # création de l'objet
    partie = dungeon.DungeonRollGame()

    # initialisation de la partie avec des dés et objets qui vont bien
    partie.inventaire = [
        'Portail de ville',  # Fin de la partie avec décompte des points
        'Appat de Dragon',  # transforme les dés monstres en dé dragon
        'Anneau dinvisibilite',  # retire les dés de l'antre du dragon (ne le vainc pas)
        'Potion',  # permet de récupérer 1 seul dé joueur
        'Parchemin',  # = dé parchemin
        'Epee Vorpale',  # = dé guerrier
        'Talisman',  # = dé clerc
        'Sceptre de Pouvoir',  # = dé mage
        'Outil de Voleur',  # = dé voleur
        'Ecaille du dragon'  # chaque écaille vaut 1 pt XP, chaque paire vaut +2 XP
    ]
    partie.cimetiere = ["Guerrier", "Mage"]
    partie.player_hand = ["Voleur", "Clerc"]
    partie.monstres = [
        'Gobelin',
        'Blob',
        'Squelette',
        'Gobelin',
        'Blob',
        'Squelette'
        ]
    partie.antre_dragon = ["Dragon", "Dragon"]

    # afficher l'état actuel
    partie.afficher_main_joueur()
    partie.afficher_main_MJ()

    # fonction à tester
    partie.utiliser_tresor()

    # voir l'état apres la fonction
    partie.afficher_main_joueur()
    partie.afficher_main_MJ()


# TESTS A DEROULER

test_utiliser_tresor()


