const API_BASE_URL = 'http://localhost:5001/api'

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Food search endpoints
  async searchFoods(query, database = 'all', page = 1, pageSize = 20) {
    return this.request(`/foods/search?q=${encodeURIComponent(query)}&database=${database}&page=${page}&page_size=${pageSize}`)
  }

  async searchUSDAFoods(query, dataType = null, category = null) {
    let url = `/foods/usda/search?q=${encodeURIComponent(query)}`
    if (dataType) url += `&data_type=${dataType}`
    if (category) url += `&category=${category}`
    return this.request(url)
  }

  async searchByBarcode(barcode) {
    return this.request(`/foods/barcode/${barcode}`)
  }

  async getFoodSuggestions(query, database = 'all', limit = 10) {
    return this.request(`/foods/suggestions?q=${encodeURIComponent(query)}&database=${database}&limit=${limit}`)
  }

  async getDatabaseStats() {
    return this.request('/foods/stats')
  }

  // Recipe endpoints
  async searchRecipes(query, number = 12, diet = null, intolerances = null) {
    let url = `/external/spoonacular/recipes?q=${encodeURIComponent(query)}&number=${number}`
    if (diet) url += `&diet=${diet}`
    if (intolerances) url += `&intolerances=${intolerances}`
    return this.request(url)
  }

  async getRecipeDetails(recipeId) {
    return this.request(`/external/spoonacular/recipe/${recipeId}`)
  }

  async searchIngredients(query, number = 10) {
    return this.request(`/external/spoonacular/ingredients?q=${encodeURIComponent(query)}&number=${number}`)
  }

  // Nutrition analysis
  async analyzeNutrition(ingredients) {
    return this.request('/external/edamam/nutrition', {
      method: 'POST',
      body: JSON.stringify({ ingredients }),
    })
  }

  // Open Food Facts
  async getProductByBarcode(barcode) {
    return this.request(`/external/openfoodfacts/product/${barcode}`)
  }

  // API status
  async getStatus() {
    return this.request('/status')
  }
}

export default new ApiService()

