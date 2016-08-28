import random
import math

class DungeonRollGame:




	def __init__(self):
		#Declaration des items trouvables dans les de et des loot pour les random
		self.playerdice = ['Guerrier', 'Voleur', 'Mage', 'Clerc', 'Champion', 'Parchemin']
		self.mjdice = ['Gobelin', 'Blob', 'Squelette', 'Coffre', 'Dragon', 'Potion']
		self.tresor = ['Portail de ville', 'Appat de Dragon', 'Anneau dinvisibilite', 'Potion', 'Parchemin', 'Epee Vorpale', 'Talisman', 'Sceptre de Pouvoir', 'Outil de Voleur']

		self.antre_dragon = []

		#Declaration du niveau du hero et du donjon au debut du jeu
		self.niveau_donjon = 4
		self.niveau_hero = 1

		#Lancement des des dU JOUeUR
		self.afficher("Bienvenue dans le Donjon. Vous etes niveau" + str(self.niveau_hero) + ". Voyons qui vous accompagne")
		d1 = random.choice(self.playerdice)
		d2 = random.choice(self.playerdice)
		d3 = random.choice(self.playerdice)
		d4 = random.choice(self.playerdice)
		d5 = random.choice(self.playerdice)
		d6 = random.choice(self.playerdice)
		d7 = random.choice(self.playerdice)

		self.player_hand = [d1, d2, d3, d4, d5, d6, d7]
		self.afficher(self.player_hand)


		# Tour de jeu
		self.continuer_partie = True
		while(self.continuer_partie):
			self.entrerDansDonjon()
			self.bastonner()
			self.pillerButin()
			self.reflechirAvenir()
			
		# Fin de la partie => calcul score 
		self.afficher("C'est la FIN")

	def entrerDansDonjon(self):
		self.afficher("Vous arrivez au niveau" + str(self.niveau_donjon) + ". Des monstres apparaissent !")

		#Lancement de des du MJ
		self.monstres = []
		self.loot = []
		for i in range(self.niveau_donjon):
			lancer_de = random.choice(self.mjdice)
			if lancer_de == "Dragon":
				self.antre_dragon.append(lancer_de)
			elif lancer_de in ("Coffre", "Potion"):
				self.loot.append(lancer_de)
			else: 
				self.monstres.append(lancer_de)

		self.afficher(str(self.antre_dragon) + str(self.loot) + str(self.monstres))	

	def bastonner(self):
		
		while self.monstres:
			# Choisir une action 
			possibilites = ["utiliser un TRésor", "utiliser un COmpagnon", "FUir"]
			self.afficher(str(possibilites))
			choix = self.recuperer("Que souhaitez-vous faire ?")

			self.afficher("vous avez choisi : " + choix) 
			
			# Résolution de l'action
			if choix in ("FU", "Fuir", "FUir", "fuir", "F", "f"):
				self.continuer_partie = False
				break
			elif choix in ("TR", "TRésor", "Trésor", "trésor", "TResor", "Tresor", "tresor", "T", "t"):
				self.afficher("Fonction non implémentée")
			elif choix in ("COmpagnon", "Compagnon", "compagnon", "C", "c"):
				self.utiliserCompagnon()


	def pillerButin(self):
		if not self.monstres
			self.afficher("Phase de loot a developper")
		else :
			pass

	def reflechirAvenir(self):
		# pour l'instant on continue toujours
		self.niveau_donjon += 1

	def utiliserCompagnon(self):
		# choix du compagnon
		for i in range(len(self.player_hand)):
			self.afficher(str(i) + " : " + str(self.player_hand[i]))
		compagnon = self.player_hand[int(self.recuperer("Lequel ?"))]
		# TODO : vérifier si le compagnon existe

		# choix de la cible
		self.afficher(self.monstres)
		cible = self.recuperer("ON BUTE QUI ?")
		 
		# creation de cadavres
		if cible == "Gobelin": 
			if compagnon in ("Guerrier", "Champion"):
				# on supprime tous les gobs
				while "Gobelin" in self.monstres:
					self.monstres.remove("Gobelin")					
			else :
				# on n'en supprime qu'un
				self.monstres.remove("Gobelin")

		elif cible == "Squelette":
			if compagnon in ("Clerc", "Champion"):
				# on supprime tous les squelettes
				while "Squelette" in self.monstres:
					self.monstres.remove("Squelette")					
			else :
				# on n'en supprime qu'un
				self.monstres.remove("Squelette")

		elif cible == "Blob":
			if compagnon in ("Mage", "Champignon"):
				# on supprime tous les blobs
				while "Blob" in self.monstres:
					self.monstres.remove("Blob")					
			else :
				# on n'en supprime qu'un
				self.monstres.remove("Blob")

		# retirer le candidat
		self.player_hand.remove(compagnon)


	def afficher(self, msg):
		print(msg)

	def recuperer(self, msg):
		return input(msg + " : ")

if __name__ == "__main__":
	DungeonRollGame()


