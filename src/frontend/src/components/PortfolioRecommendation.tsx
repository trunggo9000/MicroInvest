import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { TrendingUp, Shield, DollarSign } from "lucide-react";
import { DCASimulator } from "./DCASimulator";
import { HistoricalBacktest } from "./HistoricalBacktest";
import { AICoach } from "./AICoach";
import { PortfolioHeatmap } from "./PortfolioHeatmap";
import { GoalTracker } from "./GoalTracker";
import { PDFExport } from "./PDFExport";

interface Investment {
  symbol: string;
  name: string;
  allocation: number;
  expectedReturn: number;
  riskLevel: "low" | "medium" | "high";
  description: string;
}

interface PortfolioData {
  investments: Investment[];
  totalExpectedReturn: number;
  riskScore: number;
  monthlyAmount: number;
  projectedValue: number;
  timeframe: string;
}

interface PortfolioRecommendationProps {
  portfolio: PortfolioData;
  riskTolerance: string;
  investmentGoal: string;
}

export const PortfolioRecommendation = ({ portfolio, riskTolerance, investmentGoal }: PortfolioRecommendationProps) => {
  const getRiskBadgeColor = (risk: string) => {
    switch (risk) {
      case "low":
        return "bg-success text-success-foreground";
      case "medium":
        return "bg-warning text-warning-foreground";
      case "high":
        return "bg-error text-error-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case "low":
        return <Shield className="w-4 h-4" />;
      case "medium":
        return <TrendingUp className="w-4 h-4" />;
      case "high":
        return <TrendingUp className="w-4 h-4" />;
      default:
        return <DollarSign className="w-4 h-4" />;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Portfolio Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-primary">
            <TrendingUp className="w-6 h-6" />
            Your Personalized Investment Plan
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-accent/30 rounded-lg">
              <div className="text-2xl font-bold text-primary">
                ${portfolio.monthlyAmount}
              </div>
              <div className="text-sm text-muted-foreground">Monthly Investment</div>
            </div>
            <div className="text-center p-4 bg-success/10 rounded-lg">
              <div className="text-2xl font-bold text-success">
                {portfolio.totalExpectedReturn.toFixed(1)}%
              </div>
              <div className="text-sm text-muted-foreground">Expected Annual Return</div>
            </div>
            <div className="text-center p-4 bg-primary/10 rounded-lg">
              <div className="text-2xl font-bold text-primary">
                ${portfolio.projectedValue.toLocaleString()}
              </div>
              <div className="text-sm text-muted-foreground">
                Projected Value ({portfolio.timeframe})
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Investment Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Recommended Portfolio Allocation</CardTitle>
          <p className="text-muted-foreground">
            Based on your risk tolerance and investment goals
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {portfolio.investments.map((investment, index) => (
            <div key={index} className="border rounded-lg p-4 hover:bg-accent/20 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-lg">{investment.symbol}</h3>
                    <Badge className={getRiskBadgeColor(investment.riskLevel)}>
                      {getRiskIcon(investment.riskLevel)}
                      {investment.riskLevel} risk
                    </Badge>
                  </div>
                  <h4 className="text-muted-foreground font-medium mb-1">
                    {investment.name}
                  </h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {investment.description}
                  </p>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-primary">
                    {investment.allocation}%
                  </div>
                  <div className="text-sm text-muted-foreground">
                    ${Math.round((portfolio.monthlyAmount * investment.allocation) / 100)}
                  </div>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Allocation</span>
                  <span className="font-medium">{investment.allocation}%</span>
                </div>
                <Progress value={investment.allocation} className="h-2" />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Expected Return</span>
                  <span className="text-success font-medium">
                    +{investment.expectedReturn.toFixed(1)}% annually
                  </span>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Growth Projection */}
      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Investment Growth Projection</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-gradient-to-r from-primary/5 to-success/5 rounded-lg p-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">
                If you invest ${portfolio.monthlyAmount}/month consistently...
              </h3>
              <div className="text-3xl font-bold text-primary mb-1">
                ${portfolio.projectedValue.toLocaleString()}
              </div>
              <p className="text-muted-foreground mb-4">
                Estimated portfolio value in {portfolio.timeframe}
              </p>
              <div className="text-sm text-muted-foreground">
                * Projections based on historical data. Past performance doesn't guarantee future results.
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Portfolio Heatmap */}
      <PortfolioHeatmap 
        investments={portfolio.investments} 
        monthlyAmount={portfolio.monthlyAmount}
      />

      {/* Dollar-Cost Averaging Simulator */}
      <DCASimulator 
        monthlyAmount={portfolio.monthlyAmount}
        timeframe={portfolio.timeframe}
        expectedReturn={portfolio.totalExpectedReturn}
      />

      {/* Historical Backtest */}
      <HistoricalBacktest 
        investments={portfolio.investments}
        monthlyAmount={portfolio.monthlyAmount}
      />

      {/* Goal Tracker */}
      <GoalTracker 
        projectedValue={portfolio.projectedValue}
        monthlyAmount={portfolio.monthlyAmount}
        timeframe={portfolio.timeframe}
        expectedReturn={portfolio.totalExpectedReturn}
      />

      {/* AI Coach */}
      <AICoach 
        investments={portfolio.investments}
        riskTolerance={riskTolerance}
        monthlyAmount={portfolio.monthlyAmount}
        totalExpectedReturn={portfolio.totalExpectedReturn}
      />

      {/* PDF Export */}
      <PDFExport 
        portfolio={portfolio}
        riskTolerance={riskTolerance}
        investmentGoal={investmentGoal}
      />
    </div>
  );
};