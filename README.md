## dungeonroll_sopel
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
      * phase butin
        * récupérer le loot
            * OK - utilisation d'un compagnon
            * utilisation d'un objet/tresor (OK pour les coffres, pour les potions aussi ?) 
        * OK - utilisation des objets trésors
      * OK - phase regroupement
    * OK Dragon
      * OK Déclenchement
      * OK combat en utilisant 3 objets/compagnons différents
      * OK Vérifier la possibilité d'avoir 3 acteurs différents
    * OK Fin de la partie - décompte des points

  * Combiner plusieurs explorations

  
  * Adaptation à irc
    * OK - packaging module sopel
    * à tester - entrées du joueur
    * à tester - sorties de textes
    * présentation du texte pour que ce soit plus fluide/facile
    * OK - présentation des aides de comamnde du jeu
    * Publier le score sur tous les channels
    * voir l'état du jeu
    * voir les stats
    * enregistrer le high-score
    * OK - permettre d'interrompre le jeu en cours


  * BONUS
    * limiter les choix aux actions possibles
    * OK -ajouter message selection funny dans la méthode choisir_par_index() (ex: ON BUTE QUI ?), utilisation d'un autre paramètre ?
    
  * Validation(s)
    


## Bugs

  * FIXED - potion-trésor : on doit pouvoir choisir la face du dé compagnon qu'on récupère
  * FIXED - Choix du monstre à tuer : se fait par un string, pas de vérification de s'il y a un élément portant ce nom => mettre en place un système par index
  * FIXED - saisie d'index hors gamme/hout-of-range => exception non gérée
  * Possibilité d'utiliser les outils de voleur hors baston, pour ouvrir DES coffres par ex ?
  * FIXED ne pas pouvoir utiliser les écailles de dragon

