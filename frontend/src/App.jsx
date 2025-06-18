import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import MealPlans from './pages/MealPlans'
import FoodSearch from './pages/FoodSearch'
import Recipes from './pages/Recipes'
import Community from './pages/Community'
import Achievements from './pages/Achievements'
import Login from './pages/Login'
import './App.css'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-background">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<Layout />}>
                <Route index element={<Dashboard />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="meal-plans" element={<MealPlans />} />
                <Route path="food-search" element={<FoodSearch />} />
                <Route path="recipes" element={<Recipes />} />
                <Route path="community" element={<Community />} />
                <Route path="achievements" element={<Achievements />} />
              </Route>
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App

