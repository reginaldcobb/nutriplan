import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Trophy, Star, Target, Zap, Award, Lock, CheckCircle } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Achievements = () => {
  const { user } = useAuth()

  const achievements = [
    {
      id: 1,
      name: 'First Steps',
      description: 'Log your first meal',
      icon: '🍽️',
      points: 10,
      unlocked: true,
      unlockedAt: '2024-01-15'
    },
    {
      id: 2,
      name: '7-Day Streak',
      description: 'Log meals for 7 consecutive days',
      icon: '🔥',
      points: 50,
      unlocked: true,
      unlockedAt: '2024-01-22'
    },
    {
      id: 3,
      name: 'Protein Champion',
      description: 'Meet protein goals for 5 days',
      icon: '💪',
      points: 75,
      unlocked: true,
      unlockedAt: '2024-01-28'
    },
    {
      id: 4,
      name: 'Hydration Hero',
      description: 'Drink 8 glasses of water daily for 7 days',
      icon: '💧',
      points: 100,
      unlocked: false,
      progress: 5,
      target: 7
    },
    {
      id: 5,
      name: 'Balanced Eater',
      description: 'Maintain balanced macros for 10 days',
      icon: '⚖️',
      points: 150,
      unlocked: true,
      unlockedAt: '2024-02-05'
    },
    {
      id: 6,
      name: 'Recipe Explorer',
      description: 'Try 20 different recipes',
      icon: '👨‍🍳',
      points: 200,
      unlocked: false,
      progress: 12,
      target: 20
    },
    {
      id: 7,
      name: 'Consistency King',
      description: 'Maintain a 30-day logging streak',
      icon: '👑',
      points: 500,
      unlocked: false,
      progress: 7,
      target: 30
    },
    {
      id: 8,
      name: 'Nutrition Master',
      description: 'Reach level 20',
      icon: '🎓',
      points: 1000,
      unlocked: false,
      progress: 15,
      target: 20
    }
  ]

  const challenges = [
    {
      name: 'Weekly Warrior',
      description: 'Complete all daily goals this week',
      progress: 5,
      target: 7,
      reward: '100 points',
      timeLeft: '2 days'
    },
    {
      name: 'Veggie Variety',
      description: 'Eat 5 different vegetables this week',
      progress: 3,
      target: 5,
      reward: '75 points',
      timeLeft: '4 days'
    },
    {
      name: 'Meal Prep Master',
      description: 'Prep meals for 3 consecutive days',
      progress: 1,
      target: 3,
      reward: '150 points',
      timeLeft: '6 days'
    }
  ]

  const badges = [
    { name: 'Early Bird', description: 'Log breakfast before 9 AM', rarity: 'Common', unlocked: true },
    { name: 'Night Owl', description: 'Log dinner after 8 PM', rarity: 'Common', unlocked: true },
    { name: 'Macro Master', description: 'Perfect macro balance', rarity: 'Rare', unlocked: true },
    { name: 'Streak Keeper', description: '14-day logging streak', rarity: 'Epic', unlocked: false },
    { name: 'Nutrition Guru', description: 'Help 10 community members', rarity: 'Legendary', unlocked: false },
  ]

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'Common': return 'bg-gray-500'
      case 'Rare': return 'bg-blue-500'
      case 'Epic': return 'bg-purple-500'
      case 'Legendary': return 'bg-yellow-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Achievements</h1>
          <p className="text-muted-foreground">Track your nutrition journey milestones</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary">{user?.points || 0}</div>
          <div className="text-sm text-muted-foreground">Total Points</div>
        </div>
      </div>

      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Achievements Unlocked</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {achievements.filter(a => a.unlocked).length}/{achievements.length}
            </div>
            <Progress 
              value={(achievements.filter(a => a.unlocked).length / achievements.length) * 100} 
              className="mt-2"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Current Level</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Level {user?.level || 1}</div>
            <Progress 
              value={((user?.points || 0) % 1000) / 10} 
              className="mt-2"
            />
            <div className="text-xs text-muted-foreground mt-1">
              {1000 - ((user?.points || 0) % 1000)} points to next level
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold flex items-center">
              <Zap className="h-6 w-6 text-orange-500 mr-2" />
              {user?.streak || 0} days
            </div>
            <div className="text-xs text-muted-foreground mt-2">
              Keep logging to maintain your streak!
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="achievements" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="achievements">Achievements</TabsTrigger>
          <TabsTrigger value="challenges">Active Challenges</TabsTrigger>
          <TabsTrigger value="badges">Badges</TabsTrigger>
        </TabsList>

        <TabsContent value="achievements" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {achievements.map((achievement) => (
              <Card 
                key={achievement.id} 
                className={`transition-all ${
                  achievement.unlocked 
                    ? 'border-primary bg-primary/5' 
                    : 'opacity-75'
                }`}
              >
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="text-3xl">{achievement.icon}</div>
                    {achievement.unlocked ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <Lock className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{achievement.name}</h3>
                  <p className="text-sm text-muted-foreground mb-3">{achievement.description}</p>
                  
                  {achievement.unlocked ? (
                    <div className="space-y-2">
                      <Badge variant="secondary" className="bg-green-100 text-green-800">
                        <Trophy className="h-3 w-3 mr-1" />
                        {achievement.points} points
                      </Badge>
                      <div className="text-xs text-muted-foreground">
                        Unlocked on {new Date(achievement.unlockedAt).toLocaleDateString()}
                      </div>
                    </div>
                  ) : achievement.progress !== undefined ? (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Progress</span>
                        <span>{achievement.progress}/{achievement.target}</span>
                      </div>
                      <Progress value={(achievement.progress / achievement.target) * 100} />
                      <Badge variant="outline">{achievement.points} points</Badge>
                    </div>
                  ) : (
                    <Badge variant="outline">{achievement.points} points</Badge>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="challenges" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {challenges.map((challenge, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-lg">{challenge.name}</CardTitle>
                  <CardDescription>{challenge.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span>Progress</span>
                        <span>{challenge.progress}/{challenge.target}</span>
                      </div>
                      <Progress value={(challenge.progress / challenge.target) * 100} />
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <Badge variant="secondary">{challenge.reward}</Badge>
                      <span className="text-muted-foreground">{challenge.timeLeft} left</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="badges" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {badges.map((badge, index) => (
              <Card 
                key={index} 
                className={`transition-all ${
                  badge.unlocked 
                    ? 'border-primary bg-primary/5' 
                    : 'opacity-60'
                }`}
              >
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${getRarityColor(badge.rarity)}`}>
                      <Award className="h-6 w-6 text-white" />
                    </div>
                    {badge.unlocked ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <Lock className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{badge.name}</h3>
                  <p className="text-sm text-muted-foreground mb-3">{badge.description}</p>
                  <Badge 
                    variant="outline" 
                    className={`${getRarityColor(badge.rarity)} text-white border-0`}
                  >
                    {badge.rarity}
                  </Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default Achievements

