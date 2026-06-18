#!/usr/bin/env python3

import os
import glob
import subprocess
import sys
import re
import json
from pathlib import Path

# Configuration
INDEX_FILE = "./docs/index.json"
SYSTEM_PROMPT = """You are a precise data processor. Your task is to take the provided input and generate structural HTML representing a recipe.

Output ONLY valid HTML content. Do not include any conversational filler or explanations.

[STRUCTURAL SCHEMA]
- <title></title>: A text element for the recipe name.
- <category></category>: One of "Déjeuners", "Entrées", "Soupes", "Plats principaux", "Desserts", "Boissons", "Autres".
- <div class="recipe-detail"></div>: Used for recipe details like "Préparation:", "Cuisson:", "Total:", or "Portions:". Wrap the label in <b> tags.
- <h2>Ingrédients</h2>: Header followed by a <ul class="ing-list"> where each item contains a <span> for the text, a <span class="food-name"> wrapping the ingredient food name, and the edit icon markup.
- <h2>Instructions</h2>: Header followed by a <div class="recipe-instructions"> block containing steps (<div class="recipe-step">), notes (<div class="recipe-note">), headers (<h3>), and lists (<ul>) repeating the used ingredients.

[STRICT FORMATTING RULES]
1. Every single ingredient item must wrap its core food name in a <span class="food-name"> tag. Do not leave any raw food names un-tagged.
2. Every ingredients quantity must be repeated in the instructions when used, either inline or in a separate <ul> block.

[CORRECT FORMATTING EXAMPLE]
<title>Pain blanc à la machine à pain</title>
<category>Autres</category>

<div class="recipe-detail"><b>Préparation: </b>5 minutes</div>
<div class="recipe-detail"><b>Cuisson: </b>26 minutes</div>
<div class="recipe-detail"><b>Total: </b>2 heures</div>

<h2>Ingrédients</h2>
<ul class="ing-list">
    <li>
        <span>1 1/2 c. à thé de <span class="food-name">levure sèche active</span></span>
        <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
    </li>
    <li>
        <span>3 1/2 t de <span class="food-name">farine</span></span>
        <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
    </li>
    <li>
        <span>2 c. à soupe de <span class="food-name">sucre</span></span>
        <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
    </li>
    <li>
        <span>2 c. à soupe de <span class="food-name">huile</span></span>
        <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
    </li>
    <li>
        <span>1 1/2 t d'<span class="food-name">eau tiède</span></span>
        <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
    </li>
    <li>
        <span>1 c. à thé de <span class="food-name">sel</span></span>
        <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
    </li>
</ul>

<h2>Instructions</h2>
<div class="recipe-instructions">
    <div class="recipe-note">
        Une machine à pain est utile pour sauver du temps. Par contre, la cuisson y est parfois décevante. Je suggère d’utiliser l’appareil en mode pétrissage, puis de cuire la pâte au four
    </div>
    <div class="recipe-step">
        Dans le contenant de la machine à pain, ajouter un peu de farine, la levure, puis le reste de la farine pour protéger la levure du sel
    </div>
    <ul>
        <li>1 1/2 c. à thé de <span class="food-name">levure sèche active</span></li>
        <li>3 1/2 t de <span class="food-name">farine</span></li>
    </ul>
    <div class="recipe-step">
        Ajouter les autres ingrédients
    </div>
    <ul>
        <li>2 c. à soupe de <span class="food-name">sucre</span></li>
        <li>2 c. à soupe de <span class="food-name">huile</span></li>
        <li>1 1/2 t d'<span class="food-name">eau tiède</span></li>
        <li>1 c. à thé de <span class="food-name">sel</span></li>
    </ul>
    <div class="recipe-step">
        Démarrer la machine au mode pétrissage ou la programmer avec un minuteur pour une période future.
    </div>
    <div class="recipe-step">
        Façonner la pâte selon la forme désirée (ex miche ou petits pains). Déposer sur une plaque recouverte d’un tapis de cuisson en silicone. Cuire au four préchauffé à 180 °C (350 °F) pendant 26 minutes.
    </div>
    <h3>Notes</h3>
    <div class="recipe-note">
        Si la levure est vielle et vous n'êtes pas certain si elle est encore bonne, vous pouvez la tester avant de risquer de rater un pain entier. Ajouter le sucre et levure à 1/2 t d'eau tiède. Si la levure est encore efficace, elle devrait réagir et former des petites bulles. Utiliser le mélange comme à la place de la levure normale dans la recette. N'oubliez pas de mettre 1/2 t d'eau tiède de moins!
    </div>
    <div class="recipe-note">
        Le sel peut tuer la levure. Il est primordial que ces ingrédients ne soient pas en contact direct. Ainsi, je recommande de faire un petit nid dans la farine pour la levure.
    </div>
    <div class="recipe-note">
        Le plus important pour s'assurer que le pain lève est la température de l'eau. Elle doit être à peu près à la température du corps humain. Pas trop chaud, ni trop froid.
    </div>
</div>

Extract and structure the recipe from the following:
"""

def copy_to_clipboard(text):
    """Copies text to the Wayland clipboard using wl-copy."""
    try:
        process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
    except FileNotFoundError:
        print("Error: 'wl-copy' is not installed or not running a Wayland session. Install wl-clipboard and ensure you're on Wayland to use this script.")
        sys.exit(1)

def extract_ingredients(html):
    ingredients = re.findall(
        r'<span\s+class="food-name">(.*?)</span>',
        html,
        re.IGNORECASE | re.DOTALL
    )

    cleaned = []

    for ingredient in ingredients:
        ingredient = re.sub(r"<.*?>", "", ingredient)
        ingredient = ingredient.strip()

        if ingredient and ingredient not in cleaned:
            cleaned.append(ingredient)

    return cleaned

def load_index():
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_index(index_data):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)

def parse_and_clean_html(raw_html):
    """
    Parses out the title and details from the LLM HTML body,
    returning clean layout fragments.
    """
    title = "Nouvelle Recette"
    category = "Autres"
    details_list = []
    
    # 1. Extract and clean Title
    if "<title>" in raw_html and "</title>" in raw_html:
        try:
            title_part = raw_html.split("<title>", 1)[1]
            title = title_part.split("</title>", 1)[0].strip()
            raw_html = raw_html.replace(f"<title>{title}</title>", "")
        except Exception:
            pass

    # 2. Extract all 'recipe-detail' lines dynamically using regex
    detail_pattern = r'(<div class="recipe-detail">.*?</div>)'
    details_matches = re.findall(detail_pattern, raw_html)
    
    for match in details_matches:
        details_list.append(f"          {match.strip()}")
        # Remove it from the main body content stream
        raw_html = raw_html.replace(match, "")

    category_match = re.search(r"<category>(.*?)</category>", raw_html, re.DOTALL)
    if category_match:
        category = category_match.group(1).strip()
        raw_html = raw_html.replace(category_match.group(0), "")

    # Clean leftover whitespace fragments
    cleaned_body = raw_html.strip()
    
    return title, category, "\n".join(details_list), cleaned_body

def generate_html_page(html_content):
    """Wraps the inner recipe HTML generated by the LLM into the structural page template."""
    
    title, category, details_html, body_content = parse_and_clean_html(html_content)
    
    html = [
        "<!DOCTYPE html>",
        '<html lang="fr">',
        "  <head>",
        '    <meta charset="UTF-8" />',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />',
        f'    <title>Recette: {title}</title>',
        '    <link rel="stylesheet" href="../assets/reset.css" />',
        '    <link rel="stylesheet" href="../assets/recipe.css" />',
        "  </head>",
        "  <body>",
        '    <a href="../index.html" class="navbar"></a>',
        '    <div class="recipe">',
        '      <div class="recipe-header">',
        '        <div class="recipe-image-container">',
        '          <div class="recipe-image-wrapper">',
        f'            <img src="../assets/recipe_placeholder.png" alt="{title}" />',
        '          </div>',
        '        </div>',
        '        <div>',
        f'          <h1 class="recipe-title">{title}</h1>',
        # Injected the cleanly isolated recipe details right here!
        details_html,
        '        </div>',
        '      </div>',
        # Injected remaining data elements (Ingredients and Instructions sections)
        f'      {body_content}',
        '    </div>',
        '  </body>',
        '</html>'
    ]

    return "\n".join(html), title, category

def main():

    # Copy prompt before asking for filename
    copy_to_clipboard(SYSTEM_PROMPT)
    print("The system prompt has been automatically copied to your clipboard.")
    print("1. Go to your LLM, paste the clipboard, and append the recipe you want to add.")
    print("2. Copy the LLM's HTML response back to the clipboard.\n")

    while True:
        print("Please enter a unique recipe name for your new recipe file. (ex: 'chocolate_cake')")
        user_input = input("Enter name: ").strip()

        if not user_input:
            print("Name cannot be empty. Please try again.\n")
            continue

        target_path = Path(f"./docs/r/{user_input}.html")

        if target_path.exists():
            print(f"Error: The file '{target_path}' already exists. Please choose another name.\n")
        else:
            break
            
    # Wait for user interaction
    input("\nOnce you have copied the LLM's HTML response to your clipboard, press [Enter] to generate the HTML...")

    try:
        result = subprocess.run(['wl-paste', '--no-newline'], capture_output=True, text=True, check=True)
        llm_response = result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Failed to read from clipboard using wl-paste.")
        return

    try:
        # Clean up if the LLM wrapped it inside ```html ... ``` markdown codeblocks
        if llm_response.startswith("```html"):
            llm_response = llm_response.split("```html", 1)[1].rsplit("```", 1)[0].strip()
        elif llm_response.startswith("```"):
            llm_response = llm_response.split("```", 1)[1].rsplit("```", 1)[0].strip()
        
        # Process and generate full valid HTML page
        final_html, title, category = generate_html_page(llm_response)

        # Create parent directories (docs/r/) if they don't exist yet
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the HTML content to the file
        target_path.write_text(final_html, encoding="utf-8")

        ingredients = extract_ingredients(llm_response)

        index_data = load_index()

        index_data[user_input] = {
            "title": title,
            "image": "",
            "ingredients": ingredients,
            "category": category,
            "recipe": True,
            "link": f"./r/{user_input}.html"
        }

        save_index(index_data)

        try:
            script_dir = Path(__file__).parent

            generate_script = script_dir / "generate_index_html.py"

            subprocess.run(
                [sys.executable, str(generate_script)],
                check=True
            )
            print("Successfully regenerated index.html")
        except subprocess.CalledProcessError as e:
            print(f"Warning: generate_index_html.py failed: {e}")

        print(f"Success! File created at: {target_path}")
        
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")
        return

    print("\nProcessing complete!")

if __name__ == "__main__":
    main()