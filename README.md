# dungeonroll_sopel
A Boardgame adaptation of DungeonRoll in Sopel IRC

## Description du jeu

To be written :)

## Todo

  * Mécaniques du jeu en mode console
    * OK - initialisation du jeu
    * OK -implémentation du tour de jeu
      *  OK - entrée dans le donjon
        * OK - tirage des monstres
      * OK - phase baston
        * OK - actions des compagnons 
      * OK - phase butin
        * OK -récupérer le loot
        * Ok - utilisation des objets trésors
      * OK - phase regroupement
    * Dragon
      * Déclenchement
      * combat
    * Fin de la partie - décompte des points
    
  
  * Adaptation à irc
    * packaging module sopel
    * entrées et sorties de textes
    * présentation du texte, des aides de jeu 


  * BONUS
    * limiter les choix aux actions possibles
    
  * Validation(s)
    


## Bugs

  * FIXED - potion-trésor : on doit pouvoir choisir la face du dé compagnon qu'on récupère
  * Choix du monstre à tuer : se fait par un string, pas de vérification de s'il y a un élément portant ce nom => mettre en place un système par index
  * saisie d'index hors gamme/hout-of-range => exception non gérée
  * Possibilité d'utiliser les outils de voleur hors baston, pour ouvrir DES coffres par ex ?
  * ne pas pouvoir utiliser les écailles de dragon

