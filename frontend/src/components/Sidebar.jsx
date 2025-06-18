import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '../contexts/AuthContext'
import {
  LayoutDashboard,
  Calendar,
  Search,
  ChefHat,
  Users,
  Trophy,
  Apple,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Meal Plans', href: '/meal-plans', icon: Calendar },
  { name: 'Food Search', href: '/food-search', icon: Search },
  { name: 'Recipes', href: '/recipes', icon: ChefHat },
  { name: 'Community', href: '/community', icon: Users },
  { name: 'Achievements', href: '/achievements', icon: Trophy },
]

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()
  const { user } = useAuth()

  return (
    <div className={cn(
      "bg-card border-r border-border transition-all duration-300 ease-in-out",
      collapsed ? "w-16" : "w-64"
    )}>
      <div className="flex flex-col h-full">
        {/* Logo and Brand */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          {!collapsed && (
            <div className="flex items-center space-x-2">
              <Apple className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold text-foreground">NutriPlan</span>
            </div>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setCollapsed(!collapsed)}
            className="h-8 w-8 p-0"
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>
        </div>

        {/* User Stats */}
        {!collapsed && user && (
          <div className="p-4 border-b border-border">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Level {user.level}</span>
                <Badge variant="secondary">{user.points} pts</Badge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(user.points % 1000) / 10}%` }}
                ></div>
              </div>
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{user.streak} day streak</span>
                <span>{1000 - (user.points % 1000)} to next level</span>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent",
                  collapsed && "justify-center"
                )}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                {!collapsed && <span>{item.name}</span>}
              </Link>
            )
          })}
        </nav>

        {/* Avatar Stats */}
        {!collapsed && user?.avatar && (
          <div className="p-4 border-t border-border">
            <h3 className="text-sm font-medium mb-3">Avatar Health</h3>
            <div className="space-y-2">
              {Object.entries(user.avatar).map(([stat, value]) => (
                <div key={stat} className="flex items-center justify-between">
                  <span className="text-xs capitalize text-muted-foreground">{stat}</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-secondary rounded-full h-1.5">
                      <div 
                        className="bg-primary h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${value}%` }}
                      ></div>
                    </div>
                    <span className="text-xs font-medium w-8">{value}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Sidebar

