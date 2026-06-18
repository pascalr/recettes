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

Faire une page cuisson des aliments? Un petit paragraph très court pour chaque.
- Oeufs
- Mais
- Pois chiches
- Lentilles
- Haricots rouges, Haricots noirs
- Oignons caramélisés
Ex:  Oeufs à la coque
Plongez-le délicatement dans une casserole d'eau bouillante (utiliser une cuillère pour déposer les oeufs). Laissez cuire 11 minutes pour un oeuf dur. Plongez-le immédiatement dans un bol d'eau glacée pour arrêter la cuisson et l'écaler facilement. (On a toujours cuit à partir de l'eau froide et calculer 10 minutes, mais apparament c'est plus facile à écailler avec le choc thermique)

TODO: Recettes si manquantes:

Muffins déjeuner aux patates douces

Galettes au gruau??? Je ne me rappelle pas de cette recette...

Tacos végés
Crêpe hollandaise
Dal aux lentilles corail
Tapenlou



TODO: Des recettes suggestions? En rouge pour dire que c'est manquant et que tu ne peux pas cliquer dessus. Simplement des entrées dans index.json.
- Pâtes au pesto