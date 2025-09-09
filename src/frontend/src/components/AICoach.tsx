import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";
import { Brain, MessageCircle, Lightbulb, Shield, TrendingUp, DollarSign } from "lucide-react";

interface Investment {
  symbol: string;
  name: string;
  allocation: number;
  expectedReturn: number;
  riskLevel: "low" | "medium" | "high";
  description: string;
}

interface AICoachProps {
  investments: Investment[];
  riskTolerance: string;
  monthlyAmount: number;
  totalExpectedReturn: number;
}

const generateAIExplanation = (investment: Investment, riskTolerance: string) => {
  const explanations = {
    "VOO": {
      reason: "We recommend VOO because it's a diversified ETF tracking the S&P 500. Historically, it has returned ~10% annually with lower volatility than individual stocks.",
      benefits: ["Low expense ratio (0.03%)", "Instant diversification across 500 companies", "Strong long-term track record"],
      riskContext: riskTolerance === "low" ? "Perfect for conservative investors seeking steady growth" : "Solid foundation for any portfolio"
    },
    "VTI": {
      reason: "VTI provides exposure to the entire U.S. stock market, including small and mid-cap companies that can drive higher growth.",
      benefits: ["Total market exposure", "Includes growth potential of smaller companies", "Excellent diversification"],
      riskContext: "Slightly more volatile than S&P 500 but offers broader market participation"
    },
    "AAPL": {
      reason: "Apple is a blue-chip technology stock with strong fundamentals, consistent profitability, and a track record of innovation.",
      benefits: ["Strong brand moat", "Diversified revenue streams", "Regular dividend payments"],
      riskContext: riskTolerance === "high" ? "Good for growth-focused portfolios" : "Selected for stability among tech stocks"
    },
    "MSFT": {
      reason: "Microsoft offers diversified revenue through cloud computing, productivity software, and gaming, making it a stable tech choice.",
      benefits: ["Dominant cloud market position", "Recurring subscription revenue", "Strong balance sheet"],
      riskContext: "Less volatile than many tech stocks while maintaining growth potential"
    },
    "BND": {
      reason: "Bonds provide stability and income generation, helping to balance portfolio risk during market downturns.",
      benefits: ["Regular income payments", "Portfolio stabilization", "Inflation protection"],
      riskContext: riskTolerance === "low" ? "Essential for risk management" : "Provides stability balance"
    },
    "QQQ": {
      reason: "QQQ focuses on technology and growth companies in the Nasdaq-100, offering higher return potential with increased volatility.",
      benefits: ["Exposure to innovative tech companies", "Higher growth potential", "Tech sector leadership"],
      riskContext: "Suitable for risk-tolerant investors seeking growth"
    }
  };

  return explanations[investment.symbol as keyof typeof explanations] || {
    reason: `This investment was selected based on your risk profile and offers an expected return of ${investment.expectedReturn}%.`,
    benefits: ["Diversification", "Risk-adjusted returns", "Long-term growth potential"],
    riskContext: "Aligns with your investment goals and risk tolerance"
  };
};

export const AICoach = ({ investments, riskTolerance, monthlyAmount, totalExpectedReturn }: AICoachProps) => {
  const [selectedInvestment, setSelectedInvestment] = useState<Investment | null>(null);
  const [showOverallStrategy, setShowOverallStrategy] = useState(true);

  const getOverallStrategy = () => {
    const strategies = {
      low: {
        title: "Conservative Growth Strategy",
        description: "Your portfolio emphasizes stability with moderate growth potential. We've allocated heavily to broad market ETFs and bonds to minimize volatility while still capturing market returns.",
        keyPoints: [
          "60-70% in stable, diversified ETFs",
          "20-30% in bonds for stability",
          "Focus on consistent, long-term growth",
          "Lower volatility during market downturns"
        ]
      },
      medium: {
        title: "Balanced Growth Strategy", 
        description: "Your portfolio balances growth and stability. We've mixed broad market exposure with some individual quality stocks while maintaining some bond allocation for stability.",
        keyPoints: [
          "Diversified across ETFs and quality stocks",
          "Balanced risk-return profile",
          "Moderate exposure to growth sectors",
          "Some bonds for portfolio stability"
        ]
      },
      high: {
        title: "Aggressive Growth Strategy",
        description: "Your portfolio is optimized for maximum growth potential. We've focused on growth-oriented ETFs and individual stocks with higher return expectations.",
        keyPoints: [
          "Heavy allocation to growth ETFs",
          "Individual stock picks for alpha generation", 
          "Minimal bond allocation",
          "Higher expected returns with increased volatility"
        ]
      }
    };

    return strategies[riskTolerance as keyof typeof strategies] || strategies.medium;
  };

  const strategy = getOverallStrategy();

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-primary">
          <Brain className="w-5 h-5" />
          AI Investment Coach
        </CardTitle>
        <p className="text-muted-foreground">
          Plain-language explanations for your investment recommendations
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex gap-2 flex-wrap">
          <Button
            variant={showOverallStrategy ? "default" : "outline"}
            size="sm"
            onClick={() => setShowOverallStrategy(true)}
          >
            Overall Strategy
          </Button>
          {investments.map((investment) => (
            <Button
              key={investment.symbol}
              variant={selectedInvestment?.symbol === investment.symbol ? "default" : "outline"}
              size="sm"
              onClick={() => {
                setSelectedInvestment(investment);
                setShowOverallStrategy(false);
              }}
            >
              {investment.symbol}
            </Button>
          ))}
        </div>

        {showOverallStrategy ? (
          <div className="space-y-4">
            <div className="bg-primary/5 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold text-primary">{strategy.title}</h3>
              </div>
              <p className="text-muted-foreground mb-4">{strategy.description}</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <h4 className="font-medium">Key Strategy Points:</h4>
                  <div className="space-y-1">
                    {strategy.keyPoints.map((point, index) => (
                      <div key={index} className="flex items-start gap-2 text-sm">
                        <div className="w-1 h-1 bg-primary rounded-full mt-2 flex-shrink-0" />
                        <span>{point}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="bg-card border rounded-lg p-3">
                    <div className="text-sm text-muted-foreground">Expected Annual Return</div>
                    <div className="text-xl font-bold text-success">{totalExpectedReturn.toFixed(1)}%</div>
                  </div>
                  <div className="bg-card border rounded-lg p-3">
                    <div className="text-sm text-muted-foreground">Monthly Investment</div>
                    <div className="text-xl font-bold text-primary">${monthlyAmount}</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-accent/20 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Lightbulb className="w-4 h-4 text-warning" />
                <h4 className="font-semibold">Why This Strategy Works</h4>
              </div>
              <div className="text-sm text-muted-foreground space-y-1">
                <p>• <strong>Diversification:</strong> Reduces risk by spreading investments across different assets</p>
                <p>• <strong>Dollar-Cost Averaging:</strong> Regular investing reduces timing risk</p>
                <p>• <strong>Low Costs:</strong> ETFs have lower fees than actively managed funds</p>
                <p>• <strong>Time Horizon:</strong> Long-term approach captures compound growth</p>
              </div>
            </div>
          </div>
        ) : selectedInvestment && (
          <div className="space-y-4">
            <div className="bg-card border rounded-lg p-4">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold">{selectedInvestment.symbol}</h3>
                    <Badge variant="outline">
                      {selectedInvestment.allocation}% allocation
                    </Badge>
                  </div>
                  <h4 className="text-muted-foreground">{selectedInvestment.name}</h4>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-success">
                    {selectedInvestment.expectedReturn.toFixed(1)}%
                  </div>
                  <div className="text-sm text-muted-foreground">Expected Return</div>
                </div>
              </div>
            </div>

            <div className="bg-primary/5 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <MessageCircle className="w-5 h-5 text-primary" />
                <h4 className="font-semibold">Why We Chose This</h4>
              </div>
              <p className="text-muted-foreground mb-4">
                {generateAIExplanation(selectedInvestment, riskTolerance).reason}
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h5 className="font-medium mb-2 flex items-center gap-2">
                    <DollarSign className="w-4 h-4" />
                    Key Benefits
                  </h5>
                  <div className="space-y-1">
                    {generateAIExplanation(selectedInvestment, riskTolerance).benefits.map((benefit, index) => (
                      <div key={index} className="flex items-start gap-2 text-sm">
                        <div className="w-1 h-1 bg-success rounded-full mt-2 flex-shrink-0" />
                        <span>{benefit}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2 flex items-center gap-2">
                    <Shield className="w-4 h-4" />
                    Risk Context
                  </h5>
                  <p className="text-sm text-muted-foreground">
                    {generateAIExplanation(selectedInvestment, riskTolerance).riskContext}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};