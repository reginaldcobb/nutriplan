import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Activity, 
  Target, 
  TrendingUp, 
  Calendar,
  Apple,
  Droplets,
  Zap,
  Heart
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

const Dashboard = () => {
  const { user } = useAuth()
  const [todayStats, setTodayStats] = useState({
    calories: { consumed: 1450, target: 2000 },
    protein: { consumed: 85, target: 120 },
    carbs: { consumed: 180, target: 250 },
    fat: { consumed: 55, target: 65 },
    water: { consumed: 6, target: 8 },
    meals: { logged: 3, target: 4 }
  })

  const nutritionData = [
    { name: 'Protein', value: todayStats.protein.consumed, color: '#8884d8' },
    { name: 'Carbs', value: todayStats.carbs.consumed, color: '#82ca9d' },
    { name: 'Fat', value: todayStats.fat.consumed, color: '#ffc658' },
  ]

  const weeklyData = [
    { day: 'Mon', calories: 1800, target: 2000 },
    { day: 'Tue', calories: 2100, target: 2000 },
    { day: 'Wed', calories: 1950, target: 2000 },
    { day: 'Thu', calories: 1750, target: 2000 },
    { day: 'Fri', calories: 2200, target: 2000 },
    { day: 'Sat', calories: 1900, target: 2000 },
    { day: 'Sun', calories: 1450, target: 2000 },
  ]

  const recentMeals = [
    { name: 'Greek Yogurt with Berries', time: '8:30 AM', calories: 180, type: 'Breakfast' },
    { name: 'Grilled Chicken Salad', time: '12:45 PM', calories: 420, type: 'Lunch' },
    { name: 'Apple with Almond Butter', time: '3:15 PM', calories: 190, type: 'Snack' },
  ]

  const achievements = [
    { name: '7-Day Streak', icon: '🔥', unlocked: true },
    { name: 'Protein Master', icon: '💪', unlocked: true },
    { name: 'Hydration Hero', icon: '💧', unlocked: false },
    { name: 'Balanced Eater', icon: '⚖️', unlocked: true },
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Good morning, {user?.name?.split(' ')[0]}!</h1>
          <p className="text-muted-foreground">Let's make today a healthy one</p>
        </div>
        <div className="flex items-center space-x-4">
          <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
            <Zap className="w-3 h-3 mr-1" />
            {user?.streak} day streak
          </Badge>
          <Badge variant="outline" className="bg-secondary/10">
            Level {user?.level}
          </Badge>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Calories Today</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{todayStats.calories.consumed}</div>
            <p className="text-xs text-muted-foreground">
              of {todayStats.calories.target} target
            </p>
            <Progress 
              value={(todayStats.calories.consumed / todayStats.calories.target) * 100} 
              className="mt-2"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Water Intake</CardTitle>
            <Droplets className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{todayStats.water.consumed}</div>
            <p className="text-xs text-muted-foreground">
              of {todayStats.water.target} glasses
            </p>
            <Progress 
              value={(todayStats.water.consumed / todayStats.water.target) * 100} 
              className="mt-2"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Meals Logged</CardTitle>
            <Apple className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{todayStats.meals.logged}</div>
            <p className="text-xs text-muted-foreground">
              of {todayStats.meals.target} planned
            </p>
            <Progress 
              value={(todayStats.meals.logged / todayStats.meals.target) * 100} 
              className="mt-2"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Health Score</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">85</div>
            <p className="text-xs text-muted-foreground">
              +5 from yesterday
            </p>
            <Progress value={85} className="mt-2" />
          </CardContent>
        </Card>
      </div>

      {/* Charts and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Nutrition Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle>Today's Nutrition</CardTitle>
            <CardDescription>Macronutrient breakdown</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={nutritionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {nutritionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center space-x-4 mt-4">
              {nutritionData.map((item, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm">{item.name}: {item.value}g</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Weekly Progress */}
        <Card>
          <CardHeader>
            <CardTitle>Weekly Progress</CardTitle>
            <CardDescription>Calorie intake vs target</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={weeklyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="calories" fill="#8884d8" />
                  <Bar dataKey="target" fill="#82ca9d" opacity={0.6} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Meals and Achievements */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Meals */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Meals</CardTitle>
            <CardDescription>Your latest food entries</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentMeals.map((meal, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div>
                    <p className="font-medium">{meal.name}</p>
                    <p className="text-sm text-muted-foreground">{meal.time} • {meal.type}</p>
                  </div>
                  <Badge variant="secondary">{meal.calories} cal</Badge>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              <Apple className="w-4 h-4 mr-2" />
              Log New Meal
            </Button>
          </CardContent>
        </Card>

        {/* Achievements */}
        <Card>
          <CardHeader>
            <CardTitle>Achievements</CardTitle>
            <CardDescription>Your nutrition milestones</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              {achievements.map((achievement, index) => (
                <div 
                  key={index} 
                  className={`p-4 rounded-lg border-2 transition-all ${
                    achievement.unlocked 
                      ? 'border-primary bg-primary/5' 
                      : 'border-muted bg-muted/50 opacity-60'
                  }`}
                >
                  <div className="text-2xl mb-2">{achievement.icon}</div>
                  <p className="font-medium text-sm">{achievement.name}</p>
                  {achievement.unlocked && (
                    <Badge variant="secondary" className="mt-2 text-xs">
                      Unlocked
                    </Badge>
                  )}
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              <Target className="w-4 h-4 mr-2" />
              View All Achievements
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

