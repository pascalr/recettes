#!/usr/bin/env python3

import json
import os
import sys

# 1. Chargement des données du fichier JSON
try:
    with open("./docs/index.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:  # Fixed the undefined FileType error to a generic Exception
    print(f"Erreur lors de la lecture de index.json : {e}")
    sys.exit(1)

base_categories = ["Déjeuners", "Entrées", "Soupes", "Plats principaux", "Desserts", "Boissons", "Autres"]

# Dictionnaire pour regrouper les recettes par catégorie
grouped_recipes = {}

# 3. Traitement et tri des recettes
for recipe_id, recipe_info in data.items():
    category = recipe_info.get("category")

    # Détermination de l'image (Logique basée sur votre structure HTML existante)
    img_name = recipe_info.get("image", "")

    if img_name == "recipe_placeholder.png" or not img_name:
        img_src = "./assets/recipe_placeholder.png"
    elif img_name:
        img_src = f"./images/thumb/{img_name}"

    recipe_data = {
        "id": recipe_id,
        "title": recipe_info.get("title"),
        "img_src": img_src,
        "link": recipe_info.get("link"),
        # Fetch the 'recipe' boolean value (defaults to True if not present)
        "is_recipe": recipe_info.get("recipe", True) 
    }

    if category in grouped_recipes:
        grouped_recipes[category].append(recipe_data)
    else:
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
      .recipe-list li {
        font-size: 1.1em;
      }
      .recipe-list li a {
        color: black;
        text-decoration: none;
      }
      .recipe-list li a, .recipe-list li.missing-link {
        display: flex;
        align-items: center;
      }
      .recipe-list li a img, .recipe-list li.missing-link img {
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

      .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin: 40px auto;
        margin-bottom: 20px;
        padding: 0 20px;
        max-width: 600px;
      }

      #recipe-search {
        flex: 1;
        padding: 12px 20px;
        font-size: 16px;
        border: 2px solid #ddd;
        border-radius: 25px;
        outline: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
      }

      #recipe-search:focus {
        border-color: #ff6b6b;
        box-shadow: 0 4px 10px rgba(255, 107, 107, 0.15);
      }
      
      /* Added a helper class to completely hide empty categories dynamically */
      .category-hidden {
        display: none !important;
      }

      .missing-link {
        color: #d83b3b;
      }
    </style>
  </head>
  <body>
    <script src="./assets/recipe-search.js" defer></script>
    <nav class="navbar-home">
      <span class="navbar-title">Site de Pascal - Recettes</span>
    </nav>
    <div class="container">
      <ul class="nav nav-tabs mb-3" id="recipe-tabs">
        <li class="nav-item"><a class="nav-link active" id="tab-recettes" href="#">Recettes</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-inspirations" href="#">Inspirations</a></li>
        <li class="nav-item"><a class="nav-link" href="./aide_memoire.html">Aide-mémoire</a></li>
      </ul>
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

    if recipes_in_cat:
        # Added a class to the H2 title so we can manage its visibility via JS
        html_content += f"\n        <h2 class='category-title'>{category}</h2>"
        for recipe in recipes_in_cat:
            # Added dynamic data-recipe property converted to string lowercase ("true"/"false")
            is_recipe_str = str(recipe['is_recipe']).lower()

            # Check if the link is None, null, or an empty string
            if not recipe.get('link'):
                # Render without the <a> tag and add a class for CSS styling
                html_content += f"""
            <li id="{recipe['id']}" data-recipe="{is_recipe_str}" class="missing-link">
              <img src="{recipe['img_src']}" width="71" height="48"/>
              <div>{recipe['title']}</div>
            </li>"""
            else:
                # Render normally with the <a> tag
                html_content += f"""
            <li id="{recipe['id']}" data-recipe="{is_recipe_str}">
              <a href="{recipe['link']}">
                <img src="{recipe['img_src']}" width="71" height="48"/>
                <div>{recipe['title']}</div>
              </a>
            </li>"""

# Clôture des balises HTML + Interactivity Script
html_content += """
       </ul>
    </div>
    
    <script>
      document.addEventListener("DOMContentLoaded", function() {
        const tabRecettes = document.getElementById("tab-recettes");
        const tabInspirations = document.getElementById("tab-inspirations");
        const recipeItems = document.querySelectorAll("#categories-list li[data-recipe]");
        const categoryTitles = document.querySelectorAll(".category-title");

        function filterRecipes(showAll) {
          // 1. Toggle recipe items visibility
          recipeItems.forEach(item => {
            const isRecipe = item.getAttribute("data-recipe") === "true";
            if (showAll || isRecipe) {
              item.style.display = "";
            } else {
              item.style.display = "none";
            }
          });

          // 2. Hide category titles if they contain zero visible recipes
          categoryTitles.forEach(title => {
            let nextEl = title.nextElementSibling;
            let hasVisibleRecipes = false;
            
            while (nextEl && nextEl.tagName === "LI") {
              if (nextEl.style.display !== "none") {
                hasVisibleRecipes = true;
                break;
              }
              nextEl = nextEl.nextElementSibling;
            }
            
            if (hasVisibleRecipes) {
              title.classList.remove("category-hidden");
            } else {
              title.classList.add("category-hidden");
            }
          });
        }

        // Tab "Recettes" click handler (Default state)
        tabRecettes.addEventListener("click", function(e) {
          e.preventDefault();
          tabInspirations.classList.remove("active");
          tabRecettes.classList.add("active");
          filterRecipes(false); // Only show "recipe": true
        });

        // Tab "Inspirations" click handler
        tabInspirations.addEventListener("click", function(e) {
          e.preventDefault();
          tabRecettes.classList.remove("active");
          tabInspirations.classList.add("active");
          filterRecipes(true); // Show everything
        });

        // Run on initial page load (Default to filtering out "recipe": false)
        filterRecipes(false);
      });
    </script>
  </body>
</html>
"""

# 5. Écriture du résultat dans le fichier index.html
with open("./docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Le fichier index.html a été recréé avec succès !")