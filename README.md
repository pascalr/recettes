Voir docs/index.html pour la liste de mes recettes.

Toutes les recettes sont enregistrés dans des fichiers HTML dans le dossier docs/r.

Pour ajouter une nouvelle recette, exécuter bin/copy_new_recipe_prompt.py
Ensuite exécuter update_index_json.py, puis generate_index_html.py (TODO: simplifier le processus, exécuter 1 seule commande)

TODO:
- Rajouter recette de Poké bowl. (Mangues, Edamames, Algues, Avocats, concombre en tranches, carottes rapées)
- Rajouter recette mayonnaise à l'ail
- emphase sur les ingrédients dans les étapes, certains sont manquants
- Voir docs/todo.html pour les recettes avec images à rajouter
- Écrire des instructions pour les recettes incomplètes
- M'assurer que toutes les recettes sont transférées. Relish n'était pas transféré. Voir pourquoi.
- Un script pour rajouter une image. (Copie un système prompt. Ensuite prend l'image copié et la sauvegarde. Ensuite génère un thumbnail pour l'image.)
- Un nice to have: Search -oeuf -lait pour avoir des recettes sans oeuf et sans lait

TODO: Faire que create_recipe le LLM retourne déjà ce qu'il faut pour classer la recette et appeler update_index automatiquement.

TODO:
Courge spaghetti au feta, bacon et champignons

TODO: Recettes si manquantes:

Tofu caramélisé à l'érable
Curry de tofu à l'ancienne

Tofu parmentier
Tofu mariné au balsamique
Mapo tofu
Tofu sichuan
Tofu milanais
Doigts de tofu avec sauce moutarde et miel
Hamburger aux haricots rouges
Biscuits aux pain d'épices

Galettes à la mélasse
Tofu général tao
Biscuits tendres et moelleux aux brisures de chocolat
Muffins déjeuner aux patates douces
Muffins à la cannelle
Pain déjeuner style pizza
Pâté chinois végétarien
Pois chiches cuits

Quatre quart aux bananes
Pets-de-soeur
Haricots rouges cuits
Oignons caramélisés
Pâte de curry jaune
Gâteau rouge velours
Oeuf de lin
Tarte à la lime

Poulet champignons à la chinoise
Carrés coco et cerise
Ketchup maison
Ail des bois mariné
Tofu sauce chinoise à l'ail
Petits gâteaux à la forêt noire
Pouding aux fraises
Biscuits de pâte aux raisins secs

Biscuits au son
Galettes au chocolat
Galettes de Sarrasin
Mille-feuilles
Gâteau aux carottes
Gâteau au gruau et au sucre à la crème
Galettes au gruau
Sauce nems

Salade vinaigrette à l'ail
Riz au quinoa et curcuma
Poe banane
Tofu à la vapeur
Salade d'artichauts feta et dattes
Tacos végés
Crêpe hollandaise
Dal aux lentilles corail
Tapenlou



TODO: Des recettes suggestions? En rouge pour dire que c'est manquant et que tu ne peux pas cliquer dessus. Simplement des entrées dans index.json.
- Pâtes au pesto