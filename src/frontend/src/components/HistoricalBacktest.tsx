import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { BarChart3, TrendingUp, TrendingDown } from "lucide-react";

interface Investment {
  symbol: string;
  name: string;
  allocation: number;
  expectedReturn: number;
  riskLevel: "low" | "medium" | "high";
}

interface HistoricalBacktestProps {
  investments: Investment[];
  monthlyAmount: number;
}

// Mock historical data - in production, this would come from Yahoo Finance API
const generateHistoricalData = (investments: Investment[], startYear: number, endYear: number, monthlyAmount: number) => {
  const data = [];
  const yearsDiff = endYear - startYear;
  const months = yearsDiff * 12;
  
  // Mock volatility based on portfolio composition
  const avgReturn = investments.reduce((sum, inv) => sum + (inv.expectedReturn * inv.allocation / 100), 0);
  const volatility = investments.some(inv => inv.riskLevel === 'high') ? 0.15 : 
                    investments.some(inv => inv.riskLevel === 'medium') ? 0.10 : 0.06;
  
  let portfolioValue = 0;
  let totalContributions = 0;
  
  for (let month = 0; month <= months; month++) {
    const year = startYear + Math.floor(month / 12);
    const monthInYear = month % 12;
    
    if (month > 0) {
      // Add monthly contribution
      totalContributions += monthlyAmount;
      portfolioValue += monthlyAmount;
      
      // Apply market growth with some randomness
      const monthlyReturn = (avgReturn / 100 / 12) + (Math.random() - 0.5) * volatility / 12;
      portfolioValue *= (1 + monthlyReturn);
    }
    
    data.push({
      date: `${year}-${String(monthInYear + 1).padStart(2, '0')}`,
      value: Math.round(portfolioValue),
      contributions: totalContributions,
      gains: Math.round(portfolioValue - totalContributions)
    });
  }
  
  return data;
};

export const HistoricalBacktest = ({ investments, monthlyAmount }: HistoricalBacktestProps) => {
  const currentYear = new Date().getFullYear();
  const [timeRange, setTimeRange] = useState([currentYear - 3, currentYear]);
  
  const historicalData = generateHistoricalData(investments, timeRange[0], timeRange[1], monthlyAmount);
  const finalValue = historicalData[historicalData.length - 1];
  const totalReturn = finalValue.value - finalValue.contributions;
  const returnPercentage = (totalReturn / finalValue.contributions) * 100;
  
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-primary">
          <BarChart3 className="w-5 h-5" />
          Historical Backtest Simulator
        </CardTitle>
        <p className="text-muted-foreground">
          See how your portfolio would have performed historically
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium">Time Period</label>
            <span className="text-sm text-muted-foreground">
              {timeRange[0]} - {timeRange[1]} ({timeRange[1] - timeRange[0]} years)
            </span>
          </div>
          <Slider
            value={timeRange}
            onValueChange={setTimeRange}
            min={2015}
            max={currentYear}
            step={1}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>2015</span>
            <span>{currentYear}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-primary/10 rounded-lg">
            <div className="text-lg font-bold text-primary">
              ${finalValue.value.toLocaleString()}
            </div>
            <div className="text-xs text-muted-foreground">Final Value</div>
          </div>
          <div className="text-center p-4 bg-accent/30 rounded-lg">
            <div className="text-lg font-bold text-foreground">
              ${finalValue.contributions.toLocaleString()}
            </div>
            <div className="text-xs text-muted-foreground">Total Invested</div>
          </div>
          <div className={`text-center p-4 rounded-lg ${totalReturn >= 0 ? 'bg-success/10' : 'bg-error/10'}`}>
            <div className={`text-lg font-bold ${totalReturn >= 0 ? 'text-success' : 'text-error'}`}>
              ${Math.abs(totalReturn).toLocaleString()}
            </div>
            <div className="text-xs text-muted-foreground">
              {totalReturn >= 0 ? 'Gains' : 'Losses'}
            </div>
          </div>
          <div className="text-center p-4 bg-accent/30 rounded-lg">
            <div className="flex items-center justify-center gap-1">
              {returnPercentage >= 0 ? (
                <TrendingUp className="w-4 h-4 text-success" />
              ) : (
                <TrendingDown className="w-4 h-4 text-error" />
              )}
              <span className={`text-lg font-bold ${returnPercentage >= 0 ? 'text-success' : 'text-error'}`}>
                {Math.abs(returnPercentage).toFixed(1)}%
              </span>
            </div>
            <div className="text-xs text-muted-foreground">Total Return</div>
          </div>
        </div>

        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => value.split('-')[0]}
              />
              <YAxis 
                tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
              />
              <Tooltip 
                formatter={(value: number, name: string) => [
                  `$${value.toLocaleString()}`, 
                  name === 'value' ? 'Portfolio Value' : 'Total Contributions'
                ]}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="hsl(var(--primary))" 
                strokeWidth={3}
                dot={false}
              />
              <Line 
                type="monotone" 
                dataKey="contributions" 
                stroke="hsl(var(--muted-foreground))" 
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-accent/20 rounded-lg p-4">
          <h4 className="font-semibold mb-2">Backtest Analysis</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium">Performance: </span>
              <Badge variant={returnPercentage >= 0 ? "default" : "destructive"}>
                {returnPercentage >= 0 ? "Positive" : "Negative"} Returns
              </Badge>
            </div>
            <div>
              <span className="font-medium">Period: </span>
              <span className="text-muted-foreground">
                {timeRange[1] - timeRange[0]} year{timeRange[1] - timeRange[0] !== 1 ? 's' : ''}
              </span>
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            * Simulated data based on historical market patterns. Actual results may vary.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};