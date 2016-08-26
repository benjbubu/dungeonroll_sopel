import random
import math

playerdice = ['Guerrier', 'Voleur', 'Mage', 'Clerc', 'Champion', 'Parchemin']
mjdice = ['Gobelin', 'Blob', 'Squelette', 'Coffre', 'Dragon', 'Potion']
tresor = ['Portail de ville', 'Appat de Dragon', 'Anneau dinvisibilite', 'Potion', 'Parchemin', 'Epee Vorpale', 'Talisman', 'Sceptre de Pouvoir', 'Outil de Voleur']

niveaudonjon = 1
niveauhero = 1

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
for i in range(niveaudonjon):
	print(random.choice(mjdice))
