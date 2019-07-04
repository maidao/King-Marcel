# King-Marcel

DVORE


Objectifs :
prédiction de la fréquentation journalière
prédiction du CA
=> sur le midi / après midi / soir

Outils finaux :
fiche d’achats produits (frais)
fiche de préparation (congelés)

Permettrait :
de réduire le gaspillage
de ne pas manquer de produits
de palier au turn over important des employés

La carte des burgers changeant d’une année sur l’autre, la prédiction produits actuelle reprend les recettes des 4 dernières semaines et pondère le résultat avec l’algo.
L’aspect boissons est moins important puisque non périssable.
L’indice de confiance actuel est de 87%.

Plusieurs fichiers fournis :

JOUR
Data de janvier 2017 à juillet 2019, contient le CA, la fréquentation etc
> la saisonnalité est visible (semaine/we, journalière)
Si possible, prendre en compte sur place VS à emporter (en revanche ne pas dissocier livraison propre et livraison type uber). Voir si cette distinction permettrait d’améliorer le taux de prédiction sur l’un ou l’autre.
lemonade = conso uniquement boissons (sans plats)
Les “conso perso” sont à supprimer

PRODUITS
Données à prendre dans un second temps, moins prioritaire.
> voir si l’on trouve une saisonnalité produits/météo

METEO
Possibilité d’avoir des data + fines si besoin (ex: créneaux horaires)
La météo de la veille semble avoir de l’impact sur la conso.
> Travail à faire sur les tranches : leur pertinence, le seuil où il y a une influence.

VACANCES
Calendrier des différentes zones

PROMOTIONS
Contient les dates où il y a eu +10 burgers offerts (seuil modifiable).
Donc pas pris en compte dans le CA mais présents dans les produits + fréquentation.




A terme, est-ce que le modèle de prédiction est universel ? Ou nécessite un paramétrage spécifique à chaque restaurant ? > notre point de vue là dessus.

Possibilité de croiser avec de la data externe (ex: fréquentation des gares)

Garder en tête la notion de coût de l’entraînement (temps de calcul, entraînement journalier ? mensuel ?)

Point intermédiaire : mardi 9 juillet
