document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('recipe-search');
  const categoriesList = document.getElementById('categories-list');
  const searchList = document.getElementById('search-list');
  const h2Headers = document.querySelectorAll('h2');
  let recipeData = {};

  // Fetch the recipe data once the page loads
  fetch('./index.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      recipeData = data;
    })
    .catch(error => console.error('Error fetching recipe data:', error));

  // Helper function to normalize text (lowercase and remove accents)
  const normalizeText = (text) => {
    if (!text) return '';
    return text
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  };

  // Handle the input event
  searchInput.addEventListener('input', (e) => {
    const query = normalizeText(e.target.value.trim());

    // Grab all original recipe list items from the categories list
    const originalItems = categoriesList.querySelectorAll('li');

    // Reset the search list container on every keypress
    searchList.innerHTML = '';

    // IF NOT SEARCHING: Query is less than 2 characters
    if (query.length < 2) {
      h2Headers.forEach(h2 => h2.style.display = '');  // Show h2 titles
      categoriesList.style.display = '';              // Show original layout
      searchList.style.display = 'none';              // Hide search results
      return;
    }

    // IF SEARCHING: Hide headers and the original categories list
    h2Headers.forEach(h2 => h2.style.display = 'none');
    categoriesList.style.display = 'none';
    searchList.style.display = '';

    const matches = [];

    // Evaluate matching elements based on data in index.json
    originalItems.forEach(li => {
      const recipeId = li.id;
      const recipe = recipeData[recipeId];

      if (!recipe) return; // Skip if ID isn't mapped in JSON

      const title = normalizeText(recipe.title);
      const ingredients = recipe.ingredients || [];

      let score = 0;

      if (title.includes(query)) {
        score = 2; // Priority 1: Title match
      } else {
        const ingredientMatch = ingredients.some(ing => normalizeText(ing).includes(query));
        if (ingredientMatch) {
          score = 1; // Priority 2: Ingredients match
        }
      }

      // If it's a match, clone the element and store its weight
      if (score > 0) {
        const clonedLi = li.cloneNode(true);
        // Ensure the cloned item is visible (in case it was hidden by CSS elsewhere)
        clonedLi.style.display = ''; 
        matches.push({ element: clonedLi, score: score });
      }
    });

    // Sort matches by likelihood (highest score first)
    matches.sort((a, b) => b.score - a.score);

    // Append the sorted, cloned elements into the search list container
    matches.forEach(match => {
      searchList.appendChild(match.element);
    });
  });
});