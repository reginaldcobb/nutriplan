import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Users, MessageCircle, Heart, Share, TrendingUp, Award } from 'lucide-react'

const Community = () => {
  const posts = [
    {
      id: 1,
      user: { name: 'Sarah Johnson', avatar: '', level: 12 },
      content: 'Just completed my 30-day healthy eating challenge! Lost 8 pounds and feel amazing. The key was meal prepping on Sundays.',
      image: null,
      likes: 24,
      comments: 8,
      time: '2 hours ago',
      tags: ['weight-loss', 'meal-prep']
    },
    {
      id: 2,
      user: { name: 'Mike Chen', avatar: '', level: 8 },
      content: 'Amazing quinoa bowl recipe I tried today! High in protein and so satisfying. Recipe in comments.',
      image: null,
      likes: 15,
      comments: 12,
      time: '4 hours ago',
      tags: ['recipe', 'quinoa', 'protein']
    },
    {
      id: 3,
      user: { name: 'Emma Davis', avatar: '', level: 15 },
      content: 'Hit my 100-day streak today! 🎉 Consistency really is key. Thanks to this amazing community for the motivation!',
      image: null,
      likes: 42,
      comments: 18,
      time: '6 hours ago',
      tags: ['milestone', 'streak']
    }
  ]

  const challenges = [
    {
      name: 'Hydration Hero',
      description: 'Drink 8 glasses of water daily for 7 days',
      participants: 156,
      daysLeft: 3,
      reward: '50 points'
    },
    {
      name: 'Veggie Variety',
      description: 'Try 5 different vegetables this week',
      participants: 89,
      daysLeft: 5,
      reward: '75 points'
    },
    {
      name: 'Meal Prep Master',
      description: 'Prep meals for 3 consecutive days',
      participants: 234,
      daysLeft: 2,
      reward: '100 points'
    }
  ]

  const leaderboard = [
    { rank: 1, name: 'Alex Rodriguez', points: 3450, streak: 45 },
    { rank: 2, name: 'Jessica Kim', points: 3200, streak: 38 },
    { rank: 3, name: 'David Wilson', points: 2980, streak: 42 },
    { rank: 4, name: 'Lisa Thompson', points: 2750, streak: 29 },
    { rank: 5, name: 'You', points: 2450, streak: 7 }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Community</h1>
        <p className="text-muted-foreground">Connect with others on their nutrition journey</p>
      </div>

      <Tabs defaultValue="feed" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="feed">Feed</TabsTrigger>
          <TabsTrigger value="challenges">Challenges</TabsTrigger>
          <TabsTrigger value="leaderboard">Leaderboard</TabsTrigger>
          <TabsTrigger value="groups">Groups</TabsTrigger>
        </TabsList>

        <TabsContent value="feed" className="space-y-6">
          {/* Create Post */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex space-x-4">
                <Avatar>
                  <AvatarFallback className="bg-primary text-primary-foreground">U</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="bg-muted rounded-lg p-3 mb-3">
                    <p className="text-muted-foreground">Share your nutrition journey...</p>
                  </div>
                  <div className="flex space-x-2">
                    <Button size="sm">Share Progress</Button>
                    <Button variant="outline" size="sm">Add Photo</Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Posts */}
          <div className="space-y-4">
            {posts.map((post) => (
              <Card key={post.id}>
                <CardContent className="pt-6">
                  <div className="flex space-x-4">
                    <Avatar>
                      <AvatarFallback className="bg-primary text-primary-foreground">
                        {post.user.name.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <h3 className="font-semibold">{post.user.name}</h3>
                        <Badge variant="outline" className="text-xs">
                          Level {post.user.level}
                        </Badge>
                        <span className="text-sm text-muted-foreground">{post.time}</span>
                      </div>
                      <p className="mb-3">{post.content}</p>
                      <div className="flex flex-wrap gap-1 mb-3">
                        {post.tags.map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            #{tag}
                          </Badge>
                        ))}
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                        <button className="flex items-center space-x-1 hover:text-foreground">
                          <Heart className="h-4 w-4" />
                          <span>{post.likes}</span>
                        </button>
                        <button className="flex items-center space-x-1 hover:text-foreground">
                          <MessageCircle className="h-4 w-4" />
                          <span>{post.comments}</span>
                        </button>
                        <button className="flex items-center space-x-1 hover:text-foreground">
                          <Share className="h-4 w-4" />
                          <span>Share</span>
                        </button>
                      </div>
                    </div>
                  </div>
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
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Participants</span>
                      <span className="font-medium">{challenge.participants}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Days left</span>
                      <span className="font-medium">{challenge.daysLeft}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Reward</span>
                      <Badge variant="secondary">{challenge.reward}</Badge>
                    </div>
                    <Button className="w-full">Join Challenge</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="leaderboard" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2" />
                Weekly Leaderboard
              </CardTitle>
              <CardDescription>Top performers this week</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {leaderboard.map((user) => (
                  <div 
                    key={user.rank} 
                    className={`flex items-center justify-between p-3 rounded-lg ${
                      user.name === 'You' ? 'bg-primary/10 border border-primary/20' : 'bg-muted'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                        user.rank === 1 ? 'bg-yellow-500 text-white' :
                        user.rank === 2 ? 'bg-gray-400 text-white' :
                        user.rank === 3 ? 'bg-amber-600 text-white' :
                        'bg-muted-foreground text-white'
                      }`}>
                        {user.rank}
                      </div>
                      <div>
                        <p className="font-medium">{user.name}</p>
                        <p className="text-sm text-muted-foreground">{user.streak} day streak</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold">{user.points.toLocaleString()}</p>
                      <p className="text-sm text-muted-foreground">points</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="groups" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Weight Loss Warriors</CardTitle>
                <CardDescription>Support group for weight management</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <Users className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">1,234 members</span>
                  </div>
                  <Badge variant="secondary">Active</Badge>
                </div>
                <Button className="w-full">Join Group</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Plant-Based Nutrition</CardTitle>
                <CardDescription>Vegetarian and vegan meal ideas</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <Users className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">856 members</span>
                  </div>
                  <Badge variant="secondary">Active</Badge>
                </div>
                <Button className="w-full">Join Group</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Fitness & Nutrition</CardTitle>
                <CardDescription>Combining exercise with healthy eating</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <Users className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">2,103 members</span>
                  </div>
                  <Badge variant="secondary">Very Active</Badge>
                </div>
                <Button className="w-full">Join Group</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Meal Prep Masters</CardTitle>
                <CardDescription>Tips and tricks for meal preparation</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <Users className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">1,567 members</span>
                  </div>
                  <Badge variant="secondary">Active</Badge>
                </div>
                <Button className="w-full">Join Group</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default Community

