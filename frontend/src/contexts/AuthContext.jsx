import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('nutriplan_user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setIsLoading(false)
  }, [])

  const login = async (email, password) => {
    // Mock login - in real app this would call your API
    if (email === 'test@example.com' && password === 'password') {
      const userData = {
        id: 1,
        email: 'test@example.com',
        name: 'Test User',
        level: 15,
        points: 2450,
        streak: 7,
        avatar: {
          happiness: 85,
          energy: 78,
          strength: 92,
          health: 88
        }
      }
      setUser(userData)
      localStorage.setItem('nutriplan_user', JSON.stringify(userData))
      return { success: true }
    }
    return { success: false, error: 'Invalid credentials' }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('nutriplan_user')
  }

  const updateUserStats = (updates) => {
    if (user) {
      const updatedUser = { ...user, ...updates }
      setUser(updatedUser)
      localStorage.setItem('nutriplan_user', JSON.stringify(updatedUser))
    }
  }

  const value = {
    user,
    isLoading,
    login,
    logout,
    updateUserStats
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

