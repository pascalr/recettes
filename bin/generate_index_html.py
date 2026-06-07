#!/usr/bin/env python3

import json
import os

# 1. Chargement des données du fichier JSON
try:
    with open("./docs/index.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileType:
    print("Erreur lors de la lecture de index.json")
    exit(1)

base_categories = ["Déjeuners", "Entrées", "Soupes", "Plats principaux", "Desserts", "Boissons", "Autres"]

# Dictionnaire pour regrouper les recettes par catégorie
grouped_recipes = {}

# 3. Traitement et tri des recettes
for recipe_id, recipe_info in data.items():
    category = recipe_info.get("category")

    # Détermination de l'image (Logique basée sur votre structure HTML existante)
    # On va chercher l'extension et le nom si présents, sinon image par défaut
    img_name = recipe_info.get("image", "")

    if img_name == "recipe_placeholder.png" or not img_name:
        img_src = "./assets/recipe_placeholder.png"
    elif img_name:
        img_src = f"./images/thumb/{img_name}"

    recipe_data = {
        "id": recipe_id,
        "title": recipe_info.get("title"),
        "img_src": img_src,
    }

    if category in grouped_recipes:
        grouped_recipes[category].append(recipe_data)
    else:
        # Au cas où une nouvelle catégorie apparaîtrait dans le JSON
        grouped_recipes[category] = [recipe_data]

# Tri des recettes par nom (title) dans chaque catégorie
for cat in grouped_recipes:
    grouped_recipes[cat].sort(key=lambda x: x["title"].lower())

# 4. Génération du HTML
html_content = """<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Liste de recettes</title>
    <link rel="stylesheet" href="./assets/bootstrap.min.css" />
    <link rel="stylesheet" href="./assets/recipe.css" />
    <link rel="stylesheet" href="./assets/old_main.css" />
    <style>
      h2 {
        margin: 0.5em 0 0.25em 0;
        border-bottom: 1px solid black;
      }
      .recipe-list li a {
        color: black;
        font-size: 1.1em;
        text-decoration: none;
      }
      .recipe-list li a div {
        display: flex;
        align-items: center;
      }
      .recipe-list li a {
        display: flex;
        align-items: center;
      }
      .recipe-list li a img {
        margin-right: 0.5em;
      }
      .navbar-home {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 50px;
        padding: 0 24px;
        box-sizing: border-box;
        background-color: #111111;
        position: relative;
      }

      .navbar-title {
        color: #ffffff;
        font-family: system-ui, sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        font-size: 1rem; 
      }

      /* Container to handle centering and spacing at the top of your page */
      .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px; /* Spacing between input and button */
        margin: 40px auto; /* Generous spacing above and below the search bar */
        margin-bottom: 20px;
        padding: 0 20px; /* Prevents edge-bleeding on mobile screens */
        max-width: 600px; /* Limits the width so it doesn't stretch too far on desktop */
      }

      /* The actual input field */
      #recipe-search {
        flex: 1; /* Allows the input to grow and fill the container */
        padding: 12px 20px;
        font-size: 16px;
        border: 2px solid #ddd;
        border-radius: 25px; /* Smooth rounded edges */
        outline: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
      }

      /* High visibility focus state when a user clicks into it */
      #recipe-search:focus {
        border-color: #ff6b6b; /* Warm, foodie-friendly accent color */
        box-shadow: 0 4px 10px rgba(255, 107, 107, 0.15);
      }
    </style>
  </head>
  <body>
    <script src="./assets/recipe-search.js" defer></script>
    <nav class="navbar-home">
      <span class="navbar-title">Site de Pascal - Recettes</span>
    </nav>
    <div class="container">
      <div class="search-container">
        <input 
          type="text" 
          id="recipe-search" 
          placeholder="Rechercher des recettes ou par ingrédients (ex: pizza, tomate...)" 
          autocomplete="off"
        >
      </div>
      <ul id="search-list" class="recipe-list"></ul>
      <ul id="categories-list" class="recipe-list">"""

all_categories = base_categories + [cat for cat in grouped_recipes.keys() if cat not in base_categories]

# Ajout dynamique des catégories et des recettes
for category in all_categories:
    recipes_in_cat = grouped_recipes.get(category, [])

    # On n'affiche la catégorie que s'il y a des recettes dedans
    if recipes_in_cat:
        html_content += f"\n        <h2>{category}</h2>"
        for recipe in recipes_in_cat:
            html_content += f"""
        <li id="{recipe['id']}">
          <a href="./r/{recipe['id']}.html">
            <img src="{recipe['img_src']}" width="71" height="48"/>
            <div>{recipe['title']}</div>
          </a>
        </li>"""

# Clôture des balises HTML
html_content += """
       </ul>
    </div>
  </body>
</html>
"""

# 5. Écriture du résultat dans le fichier index.html
with open("./docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Le fichier index.html a été recréé avec succès !")