#!/usr/bin/env python3

import json
import os
import glob
import subprocess
import sys
from pathlib import Path

# Configuration
INDEX_FILE = "./docs/index.json"
SYSTEM_PROMPT = """You are a precise data processor. Your task is to take the provided input and generate a valid JSON object representing a recipe.

Output ONLY valid JSON. Do not include any conversational filler, markdown formatting (like ```json), or explanations.

[STRUCTURAL SCHEMA]
- "title": A string for the recipe name.
- "ingredients": An array of strings. Emphasize the food name by surrounding it with bold tags "<b>" and "</b>".
- "details": An array of objects with the fields:
    - "type": Can be "preparation", "cooking", "total", or "servings".
    - "value": A string.
- "instructions": An array of objects with the fields:
    - "type": Can be "step", "ingredients", "note", or "header".
        - For "step": Include a "value" string. Emphasize food names with "<b>" and "</b>", but ONLY do that when not in a list.
        - For "ingredients": Use this when the previous step includes multiple new ingredients. It repeats the ingredients used in this step. Include an "ingredients" array of strings, formatted exactly like the main "ingredients" array.
        - For "note": Include a "value" string for notes in the recipe.
        - For "header": Include a "value" string for section headers.

[STRICT FORMATTING RULES]
1. Every single ingredient string in 'ingredients' array MUST wrap the food name in <b> tags. Do not leave any raw food names un-tagged."
2. Every ingredients quantity must be repeated in the instructions when used. Either inline in a "step" or in a separate "ingredients" section immediately following the step.

[CORRECT FORMATTING EXAMPLE]
{
  "title": "Gâteau blanc",
  "details": [
    {"type": "preparation", "value": "15 minutes"},
    {"type": "cooking", "value": "35 minutes"},
    {"type": "total", "value": "50 minutes"}
  ],
  "ingredients": [
    "1/2 t de <b>beurre</b>",
    "1 t de <b>sucre</b>",
    "2 <b>oeufs</b>"
  ],
  "instructions": [
    {
      "type": "header",
      "value": "Préparation du gâteau"
    },
    {
      "type": "step",
      "value": "Crémer 1/2 t de <b>beurre</b>. Ajouter graduellement le sucre et les oeufs."
    },
    {
      "type": "ingredients",
      "ingredients": [
        "1 t de <b>sucre</b>",
        "2 <b>oeufs</b>"
      ]
    },
    {
      "type": "note",
      "value": "Le beurre doit être à température ambiante."
    }
  ]
}

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

def generate_html(data):
    """Converts the parsed JSON data into the required HTML format."""
    title = data.get("title", "Nouvelle Recette")
    
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
        f'          <h1 class="recipe-title">{title}</h1>'
    ]

    detail_labels = {
        "preparation": "Préparation: ",
        "cooking": "Cuisson: ",
        "total": "Total: ",
        "servings": "Portions: "
    }
    
    for d in data.get("details", []):
        dtype = d.get("type", "")
        dval = d.get("value", "")
        label = detail_labels.get(dtype, dtype.capitalize() + ": ")
        html.append(f'          <div class="recipe-detail"><b>{label}</b>{dval}</div>')

    html.extend([
        '        </div>',
        '      </div>',
        '',
        '      <h2>Ingrédients</h2>',
        '      <ul class="ing-list">'
    ])

    for ing in data.get("ingredients", []):
        ing_html = ing.replace("<b>", '<span class="food-name">').replace("</b>", "</span>")
        html.extend([
            '        <li>',
            f'          <span>{ing_html}</span>',
            '          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>',
            '        </li>'
        ])

    html.extend([
        '      </ul>',
        '',
        '      <h2>Instructions</h2>',
        '      <div class="recipe-instructions">'
    ])

    for inst in data.get("instructions", []):
        itype = inst.get("type")
        if itype == "header":
            html.append(f'        <h3>{inst.get("value", "")}</h3>')
        elif itype == "note":
            html.append(f'        <div class="recipe-note"><i>Note: {inst.get("value", "")}</i></div>')
        elif itype == "step":
            step_val = inst.get("value", "").replace("<b>", '<span class="food-name">').replace("</b>", "</span>")
            html.extend([
                '        <div class="recipe-step">',
                f'          {step_val}',
                '        </div>'
            ])
        elif itype == "ingredients":
            html.append('        <ul>')
            for sub_ing in inst.get("ingredients", []):
                sub_ing_html = sub_ing.replace("<b>", '<span class="food-name">').replace("</b>", "</span>")
                html.append(f'          <li>{sub_ing_html}</li>')
            html.append('        </ul>')

    html.extend([
        '      </div>',
        '    </div>',
        '  </body>',
        '</html>'
    ])

    return "\n".join(html)

def main():

  # Copy prompt before asking for filename
  copy_to_clipboard(SYSTEM_PROMPT)
  print("The system prompt has been automatically copied to your clipboard.")
  print("1. Go to your LLM, paste the clipboard, and append the recipe you want to add.")
  print("2. Copy the LLM's JSON response back to the clipboard.\n")

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
  input("\nOnce you have copied the LLM's JSON response to your clipboard, press [Enter] to generate the HTML...")

  try:
      result = subprocess.run(['wl-paste', '--no-newline'], capture_output=True, text=True, check=True)
      llm_response = result.stdout.strip()
  except subprocess.CalledProcessError:
      print("Error: Failed to read from clipboard using wl-paste.")
      return

  try:
      # Simple cleanup in case the LLM wrapped it in ```json ... ``` markdown blocks
      if llm_response.startswith("```json"):
          llm_response = llm_response.split("```json", 1)[1].rsplit("```", 1)[0].strip()
      elif llm_response.startswith("```"):
          llm_response = llm_response.split("```", 1)[1].rsplit("```", 1)[0].strip()
      
      # Parse the JSON response
      recipe_data = json.loads(llm_response)
      
      # Convert JSON to HTML
      final_html = generate_html(recipe_data)

      # Create parent directories (docs/r/) if they don't exist yet
      target_path.parent.mkdir(parents=True, exist_ok=True)
      
      # Write the HTML content to the file
      target_path.write_text(final_html, encoding="utf-8")
      print(f"Success! File created at: {target_path}")
      
  except json.JSONDecodeError as e:
      print(f"Error: Could not parse clipboard content as JSON. Ensure the LLM returned valid JSON.\nDetails: {e}")
      return
  except Exception as e:
      print(f"An error occurred while creating the file: {e}")
      return

  print("\nProcessing complete!")

if __name__ == "__main__":
    main()