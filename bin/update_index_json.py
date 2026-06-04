#!/usr/bin/env python3

import json
import os
import glob
import subprocess
import sys

# Configuration
INDEX_FILE = "./docs/index.json"
SYSTEM_PROMPT = """You are a precise data processor. Your sole task is to take the provided input and generate a valid JSON object. 
You must strictly extract the following fields from the input:
1. "title": The name of the recipe.
2. "image": The filename of the image used. It's the last part of the img tag src attribute (e.g., "280.png" from "./images/thumb/280.png").
3. "ingredients": An array of ingredients used.
4. "category": Determine and assign the most appropriate category that this item fits into. Options are: "Déjeuners", "Entrées", "Plats principaux", "Desserts", "Boissons", "Autres".

Output ONLY the raw JSON object. Do not include any conversational filler, markdown formatting (like ```json), or explanations.
"""

def load_index():
    """Loads the index.json file. Creates an empty dict if it doesn't exist."""
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {INDEX_FILE} is corrupted. Starting with an empty index.")
            return {}
    return {}

def save_index(index_data):
    """Saves the dict back to index.json with nice formatting."""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)

def copy_to_clipboard(text):
    """Copies text to the Wayland clipboard using wl-copy."""
    try:
        process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
    except FileNotFoundError:
        print("Error: 'wl-copy' is not installed or not running a Wayland session. Install wl-clipboard and ensure you're on Wayland to use this script.")
        sys.exit(1)

def main():
    index_data = load_index()
    
    # Find all .html files in the current directory
    html_files = glob.glob("./docs/*.html")
    
    if not html_files:
        print("No .html files found in the docs directory.")
        return

    is_first_copy = True

    for file_path in html_files:
        # Get just the filename (e.g., 'about.html' from 'docs/about.html')
        file_name = os.path.basename(file_path)

        # Skip index.html specifically
        if file_name.lower() == "index.html":
            continue

        # Strip the extension to get the clean key (e.g., 'about')
        base_name = os.path.splitext(file_name)[0]
        
        # Check if it's already indexed
        if base_name in index_data:
            print(f"Skipping '{file_path}': Already exists in {INDEX_FILE}.")
            continue
        
        print(f"\n--- Processing: {file_path} ---")
        
        # Read the HTML content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
            continue

        # Determine what to copy to the clipboard
        if is_first_copy:
            clipboard_payload = f"{SYSTEM_PROMPT}\n\n{file_content}"
            print("-> Copied System Prompt AND file content to clipboard.")
            is_first_copy = False
        else:
            clipboard_payload = file_content
            print("-> Copied ONLY file content to clipboard.")
            
        copy_to_clipboard(clipboard_payload)

        # Wait for user interaction
        print("Go to your LLM, paste the clipboard, and copy the JSON response.")
        print("Once copied, return here and press [Enter] to read from clipboard...")
        input("Press Enter when ready...")

        # Read the LLM response from Wayland clipboard using wl-paste
        try:
            result = subprocess.run(['wl-paste', '--no-newline'], capture_output=True, text=True, check=True)
            llm_response = result.stdout.strip()
        except subprocess.CalledProcessError:
            print("Error: Failed to read from clipboard using wl-paste. Skipping this file.")
            continue

        # Parse the JSON response
        try:
            # Simple cleanup in case the LLM wrapped it in ```json ... ``` markdown blocks
            if llm_response.startswith("```json"):
                llm_response = llm_response.split("```json", 1)[1].rsplit("```", 1)[0].strip()
            elif llm_response.startswith("```"):
                llm_response = llm_response.split("```", 1)[1].rsplit("```", 1)[0].strip()

            parsed_json = json.loads(llm_response)
            
            # Add to index and save immediately to prevent data loss
            index_data[base_name] = parsed_json
            save_index(index_data)
            print(f"Successfully added '{base_name}' to {INDEX_FILE}.")
            
        except json.JSONDecodeError:
            print("Error: Clipboard content was not valid JSON. Response received was:")
            print("-" * 40)
            print(llm_response)
            print("-" * 40)
            retry = input("Skip this file and continue to next? (y/n): ")
            if retry.lower() != 'y':
                break

    print("\nProcessing complete!")

if __name__ == "__main__":
    main()