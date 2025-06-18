import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Calendar, Clock, Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'

const MealPlans = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Meal Plans</h1>
        <p className="text-muted-foreground">Plan your weekly meals and track nutrition goals</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Weekly Meal Planner
          </CardTitle>
          <CardDescription>Coming soon - Plan your meals for the week ahead</CardDescription>
        </CardHeader>
        <CardContent>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Create Meal Plan
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

export default MealPlans

