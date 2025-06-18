import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Search, Loader2, Apple, Barcode, Plus } from 'lucide-react'
import ApiService from '../services/api'

const FoodSearch = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedDatabase, setSelectedDatabase] = useState('all')
  const [searchResults, setSearchResults] = useState(null)
  const [isSearching, setIsSearching] = useState(false)

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setIsSearching(true)
    try {
      const results = await ApiService.searchFoods(searchQuery, selectedDatabase)
      setSearchResults(results)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setIsSearching(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const { data: dbStats } = useQuery({
    queryKey: ['database-stats'],
    queryFn: ApiService.getDatabaseStats
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Food Search</h1>
        <p className="text-muted-foreground">Search our comprehensive food database</p>
      </div>

      {/* Database Stats */}
      {dbStats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Foods</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dbStats.total_foods.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">Across all databases</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">USDA Foods</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dbStats.usda.total_foods.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">{dbStats.usda.branded_foods} branded items</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Child Nutrition</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dbStats.child_nutrition.total_foods.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">School meal focused</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Search Interface */}
      <Card>
        <CardHeader>
          <CardTitle>Search Foods</CardTitle>
          <CardDescription>
            Find nutritional information for millions of foods
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Tabs value={selectedDatabase} onValueChange={setSelectedDatabase}>
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="all">All Databases</TabsTrigger>
              <TabsTrigger value="usda">USDA Only</TabsTrigger>
              <TabsTrigger value="cn">Child Nutrition</TabsTrigger>
            </TabsList>
          </Tabs>

          <div className="flex space-x-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                placeholder="Search for foods (e.g., chicken breast, apple, milk)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pl-10"
              />
            </div>
            <Button onClick={handleSearch} disabled={isSearching || !searchQuery.trim()}>
              {isSearching ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
            </Button>
            <Button variant="outline">
              <Barcode className="h-4 w-4 mr-2" />
              Scan
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Search Results */}
      {searchResults && (
        <Card>
          <CardHeader>
            <CardTitle>Search Results</CardTitle>
            <CardDescription>
              Found {searchResults.total} results for "{searchResults.query}"
            </CardDescription>
          </CardHeader>
          <CardContent>
            {searchResults.results.length === 0 ? (
              <div className="text-center py-8">
                <Apple className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">No foods found. Try a different search term.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {searchResults.results.map((food, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent transition-colors">
                    <div className="flex-1">
                      <h3 className="font-medium">{food.description}</h3>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge variant="outline" className="text-xs">
                          {food.source}
                        </Badge>
                        {food.category && (
                          <Badge variant="secondary" className="text-xs">
                            {food.category}
                          </Badge>
                        )}
                        {food.brand && (
                          <Badge variant="outline" className="text-xs">
                            {food.brand}
                          </Badge>
                        )}
                        {food.data_type && (
                          <span className="text-xs text-muted-foreground capitalize">
                            {food.data_type.replace('_', ' ')}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
                      <Button size="sm">
                        <Plus className="h-4 w-4 mr-1" />
                        Add to Meal
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {searchResults.total_pages > 1 && (
              <div className="flex justify-center mt-6">
                <div className="flex items-center space-x-2">
                  <Button variant="outline" size="sm" disabled={searchResults.page === 1}>
                    Previous
                  </Button>
                  <span className="text-sm text-muted-foreground">
                    Page {searchResults.page} of {searchResults.total_pages}
                  </span>
                  <Button variant="outline" size="sm" disabled={searchResults.page === searchResults.total_pages}>
                    Next
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Popular Searches</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {['Chicken breast', 'Brown rice', 'Broccoli', 'Salmon', 'Greek yogurt', 'Avocado'].map((term) => (
                <Button
                  key={term}
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setSearchQuery(term)
                    handleSearch()
                  }}
                >
                  {term}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Recent Searches</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {['Oatmeal', 'Banana', 'Almonds'].map((term, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-sm">{term}</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setSearchQuery(term)
                      handleSearch()
                    }}
                  >
                    Search again
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default FoodSearch

