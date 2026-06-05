document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('recipe-search');
  const recipeList = document.querySelector('.recipe-list');
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

    // Grab all recipe list items currently in the DOM
    const liItems = recipeList.querySelectorAll('li');

    // If query is less than 2 characters, reset visibility and stop
    if (query.length < 2) {
      // Show all h2 tags again
      h2Headers.forEach(h2 => h2.style.display = '');
      // Show all li tags again
      liItems.forEach(li => li.style.display = '');
      return;
    }

    // Hide all h2 tags during active search
    h2Headers.forEach(h2 => h2.style.display = 'none');

    const matches = [];

    // Evaluate matches and calculate scores for sorting priority
    liItems.forEach(li => {
      const recipeId = li.id;
      const recipe = recipeData[recipeId];

      if (!recipe) {
        // If the ID isn't in the JSON, hide it
        li.style.display = 'none';
        return;
      }

      const title = normalizeText(recipe.title);
      const ingredients = recipe.ingredients || [];

      let score = 0;

      if (title.includes(query)) {
        // Priority 1: Title match (Higher likelihood score)
        score = 2; 
      } else {
        // Priority 2: Ingredients match (Lower likelihood score)
        const ingredientMatch = ingredients.some(ing => normalizeText(ing).includes(query));
        if (ingredientMatch) {
          score = 1;
        }
      }

      if (score > 0) {
        matches.push({ element: li, score: score });
      } else {
        li.style.display = 'none';
      }
    });

    // Sort matches by likelihood (highest score first)
    matches.sort((a, b) => b.score - a.score);

    // Reorder DOM elements based on sorted matches and ensure they are visible
    matches.forEach(match => {
      match.element.style.display = '';
      recipeList.appendChild(match.element); 
    });
  });
});