import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface BudgetRiskData {
  monthlyBudget: number;
  riskTolerance: "low" | "medium" | "high";
  investmentGoal: string;
  timeHorizon: string;
}

interface BudgetRiskFormProps {
  onSubmit: (data: BudgetRiskData) => void;
  isLoading?: boolean;
}

export const BudgetRiskForm = ({ onSubmit, isLoading }: BudgetRiskFormProps) => {
  const [monthlyBudget, setMonthlyBudget] = useState<string>("");
  const [riskTolerance, setRiskTolerance] = useState<"low" | "medium" | "high">("low");
  const [investmentGoal, setInvestmentGoal] = useState<string>("");
  const [timeHorizon, setTimeHorizon] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (monthlyBudget && investmentGoal && timeHorizon) {
      onSubmit({
        monthlyBudget: parseFloat(monthlyBudget),
        riskTolerance,
        investmentGoal,
        timeHorizon,
      });
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-bold text-primary">
          Let's Build Your Investment Profile
        </CardTitle>
        <p className="text-muted-foreground">
          Tell us about your goals and we'll create a personalized portfolio recommendation
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="budget" className="text-base font-medium">
              Monthly Investment Budget
            </Label>
            <div className="relative">
              <span className="absolute left-3 top-3 text-muted-foreground">$</span>
              <Input
                id="budget"
                type="number"
                min="10"
                step="5"
                value={monthlyBudget}
                onChange={(e) => setMonthlyBudget(e.target.value)}
                placeholder="25"
                className="pl-8 text-lg"
                required
              />
            </div>
            <p className="text-sm text-muted-foreground">
              Start with as little as $10/month
            </p>
          </div>

          <div className="space-y-3">
            <Label className="text-base font-medium">Risk Tolerance</Label>
            <RadioGroup
              value={riskTolerance}
              onValueChange={(value) => setRiskTolerance(value as "low" | "medium" | "high")}
              className="grid grid-cols-1 gap-3"
            >
              <div className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-accent/50 transition-colors">
                <RadioGroupItem value="low" id="low" />
                <div className="flex-1">
                  <Label htmlFor="low" className="font-medium text-success">
                    Conservative (Low Risk)
                  </Label>
                  <p className="text-sm text-muted-foreground">
                    Prioritize capital preservation with steady, modest returns
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-accent/50 transition-colors">
                <RadioGroupItem value="medium" id="medium" />
                <div className="flex-1">
                  <Label htmlFor="medium" className="font-medium text-warning">
                    Balanced (Medium Risk)
                  </Label>
                  <p className="text-sm text-muted-foreground">
                    Mix of growth and stability for moderate returns
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-accent/50 transition-colors">
                <RadioGroupItem value="high" id="high" />
                <div className="flex-1">
                  <Label htmlFor="high" className="font-medium text-error">
                    Growth-Focused (High Risk)
                  </Label>
                  <p className="text-sm text-muted-foreground">
                    Higher potential returns with increased volatility
                  </p>
                </div>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label htmlFor="goal" className="text-base font-medium">
              Investment Goal
            </Label>
            <Select value={investmentGoal} onValueChange={setInvestmentGoal} required>
              <SelectTrigger>
                <SelectValue placeholder="Select your primary goal" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="emergency-fund">Build Emergency Fund</SelectItem>
                <SelectItem value="laptop">Save for Laptop/Electronics</SelectItem>
                <SelectItem value="long-term-wealth">Build Long-term Wealth</SelectItem>
                <SelectItem value="textbooks">Save for Textbooks</SelectItem>
                <SelectItem value="travel">Save for Travel</SelectItem>
                <SelectItem value="graduation-gift">Graduation Goal</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="timeline" className="text-base font-medium">
              Time Horizon
            </Label>
            <Select value={timeHorizon} onValueChange={setTimeHorizon} required>
              <SelectTrigger>
                <SelectValue placeholder="When do you need the money?" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="3-months">3 months</SelectItem>
                <SelectItem value="6-months">6 months</SelectItem>
                <SelectItem value="1-year">1 year</SelectItem>
                <SelectItem value="2-years">2 years</SelectItem>
                <SelectItem value="5-years">5+ years</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button
            type="submit"
            className="w-full text-lg py-6"
            disabled={isLoading || !monthlyBudget || !investmentGoal || !timeHorizon}
          >
            {isLoading ? "Analyzing Your Profile..." : "Get My Investment Plan"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};