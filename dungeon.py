import random
import math

#Declaration des items trouvables dans les de et des loot pour les random
playerdice = ['Guerrier', 'Voleur', 'Mage', 'Clerc', 'Champion', 'Parchemin']
mjdice = ['Gobelin', 'Blob', 'Squelette', 'Coffre', 'Dragon', 'Potion']
tresor = ['Portail de ville', 'Appat de Dragon', 'Anneau dinvisibilite', 'Potion', 'Parchemin', 'Epee Vorpale', 'Talisman', 'Sceptre de Pouvoir', 'Outil de Voleur']

#Declaration du niveau du hero et du donjon au debut du jeu
niveaudonjon = 4
niveauhero = 1

#Lancement des des du joueur
print("Bienvenue dans le Donjon. Vous etes niveau", niveauhero , ". Voyons qui vous accompagne")
d1 = random.choice(playerdice)
d2 = random.choice(playerdice)
d3 = random.choice(playerdice)
d4 = random.choice(playerdice)
d5 = random.choice(playerdice)
d6 = random.choice(playerdice)
d7 = random.choice(playerdice)

playerhand = [d1, d2, d3, d4, d5, d6, d7]
print(playerhand)


print("Vous arrivez au niveau", niveaudonjon, ". Des monstres apparaissent !")
#Lancement de des du MJ
mjhand = []
for i in range(niveaudonjon):
	mjhand.append(random.choice(mjdice))

print(mjhand)	
print("Que souhaitez-vous faire ?")


