Voir docs/index.html pour la liste de mes recettes.

Toutes les recettes sont enregistrés dans des fichiers HTML dans le dossier docs.

Pour ajouter une nouvelle recette, créer un assistant IA et lui donner le context écrit dans SystemPrompt.txt.

Copier/Coller le contenu dans un nouveau fichier .html dans docs.

Copier/Coller et entrer les bonnes informations dans index.html.

TODO:
- Degré C en premier avec degré F en parenthèse
- fraction et non 0.5 t
- outils de recherche (idéalement généré automatiquement avec index.html avec les recettes à jour, exact_match nom recette et aussi si contient ingrédient serait cool)
- emphase sur les ingrédients dans les étapes, certains sont manquants
- générer index.html automatiqement (commencer les noms de fichier avec la catégorie? _soupe_soupe_blah_blah_blah?)
- Voir docs/todo.html pour les recettes avec images à rajouter
- Écrire des instructions pour les recettes incomplètes
- M'assurer que toutes les recettes sont transférées. Relish n'était pas transféré. Voir pourquoi.
- Un nice to have: Search -oeuf -lait pour avoir des recettes sans oeuf et sans lait








WIP js prompt:
Write html line to include javascript file after page loaded. Write javascript file that handles event on input tag id = "recipe-search". It should fetch data from "./index.json" URL. Whenever at least 2 key pressed, it should filter recipes. Recipes are in a ul tag with class = "recipe-list". The keys from index.json matches the ids of the li tags. Whenever searching, hide all the h2 tags. It should prioritize matching index.json "title" property. After that it should check index.json "ingredients" array for a match. It should sort by likelihood. It should not matter accents and lettercases.