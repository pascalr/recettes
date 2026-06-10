#!/usr/bin/env python3

import json
import os
import glob
import subprocess
import sys
from pathlib import Path

# Configuration
INDEX_FILE = "./docs/index.json"
SYSTEM_PROMPT = """You are a precise data processor. Your task is to take the provided input and generate a valid HTML page.
Here is a recipe template you should follow strictly, without adding any extra elements or sections. The HTML should be well-structured and valid, using appropriate tags for each section.:

<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Recette: Gâteau blanc</title>
    <link rel="stylesheet" href="../assets/reset.css" />
    <link rel="stylesheet" href="../assets/recipe.css" />
  </head>
  <body>
    <a href="../index.html" class="navbar"></a>
    <div class="recipe">
      <div class="recipe-header">
        <div class="recipe-image-container">
          <div class="recipe-image-wrapper">
            <img src="../assets/recipe_placeholder.png" alt="Gâteau blanc" />
          </div>
        </div>
        <div>
          <h1 class="recipe-title">Gâteau blanc</h1>
          <div class="recipe-detail"><b>Préparation: </b>15 minutes</div>
          <div class="recipe-detail"><b>Cuisson: </b>35 minutes</div>
          <div class="recipe-detail"><b>Total: </b>50 minutes</div>
        </div>
      </div>

      <h2>Ingrédients</h2>
      <ul class="ing-list">
        <li>
          <span>1/2 t de <span class="food-name">beurre</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span>1 t de <span class="food-name">sucre</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span>2 <span class="food-name">oeuf</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span><span class="food-name">extrait de vanille</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span>1 1/2 t de <span class="food-name">farine</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span>2 1/2 c. à thé de <span class="food-name">poudre à pâte</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span>1 pincée de <span class="food-name">sel</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
        <li>
          <span>2/3 t de <span class="food-name">lait</span></span>
          <div class="ing-btn"><img src="../assets/pencil-square.svg" /></div>
        </li>
      </ul>

      <h2>Instructions</h2>
      <div class="recipe-instructions">
        <div class="recipe-step">
          Crémer 1/2 t de <span class="food-name">beurre</span>. Ajouter graduellement le sucre, les œufs, la vanille et bien battre
        </div>
        <ul>
          <li>1 t de <span class="food-name">sucre</span></li>
          <li>2 <span class="food-name">oeuf</span></li>
          <li><span class="food-name">extrait de vanille</span></li>
        </ul>
        <div class="recipe-step">
          Dans un autre bol, mélanger la farine, la poudre à pâte et le sel.
        </div>
        <ul>
          <li>1 1/2 t de <span class="food-name">farine</span></li>
          <li>2 1/2 c. à thé de <span class="food-name">poudre à pâte</span></li>
          <li>1 pincée de <span class="food-name">sel</span></li>
        </ul>
        <div class="recipe-step">
          Mélanger à la première préparation en alternant les ingrédients secs avec le lait.
        </div>
        <div class="recipe-step">
          Verser dans un moule beurré et cuire au four préchauffé à 350 degrés F pendant environ 35 min.
        </div>
      </div>
    </div>
  </body>
</html>

Output ONLY the whole HTML page from DOCTYPE to closing html tag. Do not include any conversational filler, markdown formatting (like ```html), or explanations.

Extract from the following:
"""

def copy_to_clipboard(text):
    """Copies text to the Wayland clipboard using wl-copy."""
    try:
        process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
    except FileNotFoundError:
        print("Error: 'wl-copy' is not installed or not running a Wayland session. Install wl-clipboard and ensure you're on Wayland to use this script.")
        sys.exit(1)

def main():

  while True:
    # 1. Ask the user for a name with an example
    print("Please enter a unique recipe name for your new recipe. (ex: 'chocolate_cake')")
    user_input = input("Enter name: ").strip()

    # Basic validation to ensure they didn't give an empty string
    if not user_input:
        print("Name cannot be empty. Please try again.\n")
        continue

    # 2. Define the target file path
    # This automatically handles directory slashes correctly across OS platforms
    target_path = Path(f"./docs/r/{user_input}.html")

    # 3. Check if the file already exists
    if target_path.exists():
        print(f"Error: The file '{target_path}' already exists. Please choose another name.\n")
    else:
      # Break the loop since we successfully created the file
      break
        
  copy_to_clipboard(SYSTEM_PROMPT)

  # Wait for user interaction
  print("Go to your LLM, paste the clipboard, and paste the recipe you want to add.")
  print("Then copy the LLM's JSON response back to the clipboard")
  print("Once copied, return here and press [Enter] to read from clipboard...")
  input("Press Enter when ready...")

  # Read the LLM response from Wayland clipboard using wl-paste
  try:
      result = subprocess.run(['wl-paste', '--no-newline'], capture_output=True, text=True, check=True)
      llm_response = result.stdout.strip()
  except subprocess.CalledProcessError:
      print("Error: Failed to read from clipboard using wl-paste.")
      return

  # Parse the JSON response
  try:
      # Simple cleanup in case the LLM wrapped it in ```html ... ``` markdown blocks
      if llm_response.startswith("```html"):
          llm_response = llm_response.split("```html", 1)[1].rsplit("```", 1)[0].strip()
      elif llm_response.startswith("```"):
          llm_response = llm_response.split("```", 1)[1].rsplit("```", 1)[0].strip()
      
      # Create parent directories (docs/r/) if they don't exist yet
      target_path.parent.mkdir(parents=True, exist_ok=True)
      
      # 4. Write the HTML content to the file
      target_path.write_text(llm_response, encoding="utf-8")
      print(f"Success! File created at: {target_path}")
      
  except Exception as e:
      print(f"An error occurred while creating the file: {e}")
      return

  print("\nProcessing complete!")

if __name__ == "__main__":
    main()