import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";
import { Target, CheckCircle, AlertCircle, TrendingUp, Calendar } from "lucide-react";

interface GoalTrackerProps {
  projectedValue: number;
  monthlyAmount: number;
  timeframe: string;
  expectedReturn: number;
}

export const GoalTracker = ({ projectedValue, monthlyAmount, timeframe, expectedReturn }: GoalTrackerProps) => {
  const [goalAmount, setGoalAmount] = useState(2000);
  const [goalDescription, setGoalDescription] = useState("Emergency Fund");
  const [showRecommendations, setShowRecommendations] = useState(false);

  const timeMultipliers = {
    "3-months": 3,
    "6-months": 6,
    "1-year": 12,
    "2-years": 24,
    "5-years": 60
  };

  const months = timeMultipliers[timeframe as keyof typeof timeMultipliers] || 12;
  const goalProgress = Math.min((projectedValue / goalAmount) * 100, 100);
  const shortfall = Math.max(goalAmount - projectedValue, 0);
  const surplus = Math.max(projectedValue - goalAmount, 0);

  // Calculate required monthly amount to reach goal
  const calculateRequiredMonthly = (targetAmount: number, months: number, annualReturn: number) => {
    const monthlyReturn = annualReturn / 100 / 12;
    if (monthlyReturn === 0) return targetAmount / months;
    
    // PMT calculation for future value of annuity
    return targetAmount * monthlyReturn / (Math.pow(1 + monthlyReturn, months) - 1);
  };

  const requiredMonthly = calculateRequiredMonthly(goalAmount, months, expectedReturn);

  const goalScenarios = [
    { amount: goalAmount * 0.75, label: "Conservative" },
    { amount: goalAmount, label: "Target" },
    { amount: goalAmount * 1.25, label: "Stretch" }
  ];

  const commonGoals = [
    { name: "Emergency Fund", amount: 3000, timeframe: "1-year" },
    { name: "Laptop Fund", amount: 1500, timeframe: "6-months" },
    { name: "Study Abroad", amount: 5000, timeframe: "2-years" },
    { name: "Car Down Payment", amount: 3000, timeframe: "1-year" },
    { name: "Graduate School Fund", amount: 10000, timeframe: "5-years" }
  ];

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-primary">
          <Target className="w-5 h-5" />
          Goal Tracker
        </CardTitle>
        <p className="text-muted-foreground">
          Set a target and see if your investment plan will get you there
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Goal Setting */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="goal-description">Goal Description</Label>
            <Input
              id="goal-description"
              value={goalDescription}
              onChange={(e) => setGoalDescription(e.target.value)}
              placeholder="e.g., Emergency Fund"
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="goal-amount">Target Amount ($)</Label>
            <Input
              id="goal-amount"
              type="number"
              value={goalAmount}
              onChange={(e) => setGoalAmount(Number(e.target.value))}
              className="mt-1"
            />
          </div>
        </div>

        {/* Quick Goal Templates */}
        <div className="space-y-2">
          <Label className="text-sm font-medium">Common Student Goals</Label>
          <div className="flex gap-2 flex-wrap">
            {commonGoals.map((goal) => (
              <Button
                key={goal.name}
                variant="outline"
                size="sm"
                onClick={() => {
                  setGoalDescription(goal.name);
                  setGoalAmount(goal.amount);
                }}
                className="text-xs"
              >
                {goal.name} (${goal.amount.toLocaleString()})
              </Button>
            ))}
          </div>
        </div>

        {/* Goal Progress */}
        <div className="bg-card border rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-lg">{goalDescription}</h3>
            <Badge variant={goalProgress >= 100 ? "default" : goalProgress >= 80 ? "secondary" : "destructive"}>
              {goalProgress >= 100 ? (
                <>
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Goal Achievable
                </>
              ) : (
                <>
                  <AlertCircle className="w-3 h-3 mr-1" />
                  {goalProgress < 80 ? "Needs Adjustment" : "Close to Goal"}
                </>
              )}
            </Badge>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Progress toward ${goalAmount.toLocaleString()}</span>
              <span className="font-medium">{goalProgress.toFixed(1)}%</span>
            </div>
            <Progress value={goalProgress} className="h-3" />
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
              <div className="text-center p-3 bg-primary/10 rounded-lg">
                <div className="text-lg font-bold text-primary">
                  ${projectedValue.toLocaleString()}
                </div>
                <div className="text-xs text-muted-foreground">Projected Value</div>
              </div>
              <div className="text-center p-3 bg-accent/30 rounded-lg">
                <div className="text-lg font-bold text-foreground">
                  ${goalAmount.toLocaleString()}
                </div>
                <div className="text-xs text-muted-foreground">Target Goal</div>
              </div>
              <div className={`text-center p-3 rounded-lg ${shortfall > 0 ? 'bg-error/10' : 'bg-success/10'}`}>
                <div className={`text-lg font-bold ${shortfall > 0 ? 'text-error' : 'text-success'}`}>
                  ${shortfall > 0 ? shortfall.toLocaleString() : surplus.toLocaleString()}
                </div>
                <div className="text-xs text-muted-foreground">
                  {shortfall > 0 ? 'Shortfall' : 'Surplus'}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        {shortfall > 0 && (
          <div className="bg-warning/10 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className="w-5 h-5 text-warning" />
              <h4 className="font-semibold">Goal Achievement Recommendations</h4>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h5 className="font-medium mb-2">Option 1: Increase Monthly Investment</h5>
                <p className="text-sm text-muted-foreground mb-2">
                  To reach your goal of ${goalAmount.toLocaleString()}, you would need to invest:
                </p>
                <div className="bg-card border rounded p-3">
                  <div className="text-xl font-bold text-primary">
                    ${Math.ceil(requiredMonthly)}/month
                  </div>
                  <div className="text-sm text-muted-foreground">
                    (+${Math.ceil(requiredMonthly - monthlyAmount)} more than current)
                  </div>
                </div>
              </div>
              
              <div>
                <h5 className="font-medium mb-2">Option 2: Extend Timeline</h5>
                <p className="text-sm text-muted-foreground mb-2">
                  Keep current monthly amount and extend your timeline:
                </p>
                <div className="bg-card border rounded p-3">
                  <div className="text-xl font-bold text-primary">
                    {Math.ceil((goalAmount / projectedValue) * months)} months
                  </div>
                  <div className="text-sm text-muted-foreground">
                    ({Math.ceil((goalAmount / projectedValue) * months) - months} months longer)
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Goal Scenarios */}
        <div className="space-y-3">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowRecommendations(!showRecommendations)}
          >
            {showRecommendations ? "Hide" : "Show"} Goal Scenarios
          </Button>

          {showRecommendations && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {goalScenarios.map((scenario, index) => {
                const scenarioProgress = Math.min((projectedValue / scenario.amount) * 100, 100);
                const scenarioRequiredMonthly = calculateRequiredMonthly(scenario.amount, months, expectedReturn);
                
                return (
                  <div key={index} className="bg-card border rounded-lg p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <Calendar className="w-4 h-4" />
                      <span className="font-medium">{scenario.label} Goal</span>
                    </div>
                    <div className="text-lg font-bold text-primary mb-1">
                      ${scenario.amount.toLocaleString()}
                    </div>
                    <Progress value={scenarioProgress} className="h-2 mb-2" />
                    <div className="text-xs text-muted-foreground">
                      Requires ${Math.ceil(scenarioRequiredMonthly)}/month
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="bg-accent/20 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-primary" />
            <h4 className="font-semibold">Goal Achievement Tips</h4>
          </div>
          <div className="text-sm text-muted-foreground space-y-1">
            <p>• Start early to take advantage of compound growth</p>
            <p>• Automate your investments to stay consistent</p>
            <p>• Review and adjust your goals quarterly</p>
            <p>• Consider increasing contributions when income grows</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};