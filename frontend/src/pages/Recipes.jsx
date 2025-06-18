import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Search, Loader2, ChefHat, Clock, Users, Heart, Plus } from 'lucide-react'
import ApiService from '../services/api'

const Recipes = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [recipes, setRecipes] = useState(null)
  const [isSearching, setIsSearching] = useState(false)
  const [selectedDiet, setSelectedDiet] = useState('')

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setIsSearching(true)
    try {
      const results = await ApiService.searchRecipes(searchQuery, 12, selectedDiet || null)
      setRecipes(results)
    } catch (error) {
      console.error('Recipe search failed:', error)
    } finally {
      setIsSearching(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const dietOptions = [
    { value: '', label: 'All Diets' },
    { value: 'vegetarian', label: 'Vegetarian' },
    { value: 'vegan', label: 'Vegan' },
    { value: 'gluten-free', label: 'Gluten Free' },
    { value: 'ketogenic', label: 'Keto' },
    { value: 'paleo', label: 'Paleo' },
  ]

  const popularRecipes = [
    { name: 'Mediterranean Quinoa Bowl', time: '25 min', difficulty: 'Easy', rating: 4.8 },
    { name: 'Grilled Salmon with Vegetables', time: '30 min', difficulty: 'Medium', rating: 4.9 },
    { name: 'Chicken Stir Fry', time: '20 min', difficulty: 'Easy', rating: 4.7 },
    { name: 'Vegetarian Buddha Bowl', time: '35 min', difficulty: 'Easy', rating: 4.6 },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Recipes</h1>
        <p className="text-muted-foreground">Discover healthy and delicious recipes</p>
      </div>

      {/* Search Interface */}
      <Card>
        <CardHeader>
          <CardTitle>Find Recipes</CardTitle>
          <CardDescription>
            Search from thousands of healthy recipes with nutritional information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex space-x-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                placeholder="Search recipes (e.g., pasta, chicken, salad)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pl-10"
              />
            </div>
            <select
              value={selectedDiet}
              onChange={(e) => setSelectedDiet(e.target.value)}
              className="px-3 py-2 border border-input bg-background rounded-md text-sm"
            >
              {dietOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <Button onClick={handleSearch} disabled={isSearching || !searchQuery.trim()}>
              {isSearching ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Recipe Results */}
      {recipes && (
        <Card>
          <CardHeader>
            <CardTitle>Recipe Results</CardTitle>
            <CardDescription>
              Found {recipes.total} recipes for "{recipes.query}"
            </CardDescription>
          </CardHeader>
          <CardContent>
            {recipes.results.length === 0 ? (
              <div className="text-center py-8">
                <ChefHat className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">No recipes found. Try a different search term.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recipes.results.map((recipe) => (
                  <Card key={recipe.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                    <div className="aspect-video bg-muted relative">
                      {recipe.image ? (
                        <img 
                          src={recipe.image} 
                          alt={recipe.title}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="flex items-center justify-center h-full">
                          <ChefHat className="h-12 w-12 text-muted-foreground" />
                        </div>
                      )}
                      <div className="absolute top-2 right-2">
                        <Badge variant="secondary" className="bg-black/50 text-white">
                          <Heart className="h-3 w-3 mr-1" />
                          {recipe.spoonacularScore ? Math.round(recipe.spoonacularScore) : 'N/A'}
                        </Badge>
                      </div>
                    </div>
                    <CardContent className="p-4">
                      <h3 className="font-semibold text-lg mb-2 line-clamp-2">{recipe.title}</h3>
                      <div className="flex items-center justify-between text-sm text-muted-foreground mb-3">
                        <div className="flex items-center">
                          <Clock className="h-4 w-4 mr-1" />
                          {recipe.readyInMinutes} min
                        </div>
                        <div className="flex items-center">
                          <Users className="h-4 w-4 mr-1" />
                          {recipe.servings} servings
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-1 mb-3">
                        {recipe.vegetarian && <Badge variant="outline" className="text-xs">Vegetarian</Badge>}
                        {recipe.vegan && <Badge variant="outline" className="text-xs">Vegan</Badge>}
                        {recipe.glutenFree && <Badge variant="outline" className="text-xs">Gluten Free</Badge>}
                        {recipe.dairyFree && <Badge variant="outline" className="text-xs">Dairy Free</Badge>}
                      </div>
                      <div className="flex space-x-2">
                        <Button variant="outline" size="sm" className="flex-1">
                          View Recipe
                        </Button>
                        <Button size="sm" className="flex-1">
                          <Plus className="h-4 w-4 mr-1" />
                          Add to Plan
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Popular Recipes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Popular Recipes</CardTitle>
            <CardDescription>Trending healthy recipes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {popularRecipes.map((recipe, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div>
                    <p className="font-medium">{recipe.name}</p>
                    <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                      <span>{recipe.time}</span>
                      <span>•</span>
                      <span>{recipe.difficulty}</span>
                      <span>•</span>
                      <div className="flex items-center">
                        <Heart className="h-3 w-3 mr-1" />
                        {recipe.rating}
                      </div>
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    View
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recipe Categories</CardTitle>
            <CardDescription>Browse by meal type</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3">
              {['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Desserts', 'Smoothies'].map((category) => (
                <Button
                  key={category}
                  variant="outline"
                  className="h-16 flex flex-col items-center justify-center"
                  onClick={() => {
                    setSearchQuery(category.toLowerCase())
                    handleSearch()
                  }}
                >
                  <ChefHat className="h-5 w-5 mb-1" />
                  {category}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Recipes

