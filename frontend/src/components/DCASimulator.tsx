import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Calculator, TrendingUp } from "lucide-react";

interface DCASimulatorProps {
  monthlyAmount: number;
  timeframe: string;
  expectedReturn: number;
}

export const DCASimulator = ({ monthlyAmount, timeframe, expectedReturn }: DCASimulatorProps) => {
  const [customMonthly, setCustomMonthly] = useState(monthlyAmount);
  const [showComparison, setShowComparison] = useState(false);

  const timeMultipliers = {
    "3-months": 3,
    "6-months": 6,
    "1-year": 12,
    "2-years": 24,
    "5-years": 60
  };

  const months = timeMultipliers[timeframe as keyof typeof timeMultipliers] || 12;
  const monthlyReturn = expectedReturn / 100 / 12;

  const generateDCAData = () => {
    const data = [];
    let dcaValue = 0;
    const lumpSum = customMonthly * months;
    let lumpSumValue = lumpSum;

    for (let month = 0; month <= months; month++) {
      if (month > 0) {
        dcaValue = (dcaValue + customMonthly) * (1 + monthlyReturn);
        lumpSumValue = lumpSumValue * (1 + monthlyReturn);
      }

      data.push({
        month,
        dca: Math.round(dcaValue),
        lumpSum: Math.round(lumpSumValue),
        contributions: month * customMonthly
      });
    }

    return data;
  };

  const chartData = generateDCAData();
  const finalDCA = chartData[chartData.length - 1].dca;
  const finalLumpSum = chartData[chartData.length - 1].lumpSum;
  const totalContributions = customMonthly * months;

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-primary">
          <Calculator className="w-5 h-5" />
          Dollar-Cost Averaging Simulator
        </CardTitle>
        <p className="text-muted-foreground">
          Compare regular monthly investing vs. lump-sum investment
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <Label htmlFor="monthly-amount">Monthly Investment</Label>
            <Input
              id="monthly-amount"
              type="number"
              value={customMonthly}
              onChange={(e) => setCustomMonthly(Number(e.target.value))}
              className="mt-1"
            />
          </div>
          <Button 
            onClick={() => setShowComparison(!showComparison)}
            variant="outline"
            className="mt-6"
          >
            {showComparison ? "Hide" : "Show"} Comparison
          </Button>
        </div>

        {showComparison && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="text-center p-4 bg-primary/10 rounded-lg">
                <div className="text-xl font-bold text-primary">
                  ${finalDCA.toLocaleString()}
                </div>
                <div className="text-sm text-muted-foreground">DCA Final Value</div>
              </div>
              <div className="text-center p-4 bg-accent/30 rounded-lg">
                <div className="text-xl font-bold text-foreground">
                  ${finalLumpSum.toLocaleString()}
                </div>
                <div className="text-sm text-muted-foreground">Lump Sum Final Value</div>
              </div>
              <div className="text-center p-4 bg-success/10 rounded-lg">
                <div className="text-xl font-bold text-success">
                  ${totalContributions.toLocaleString()}
                </div>
                <div className="text-sm text-muted-foreground">Total Contributions</div>
              </div>
            </div>

            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                  <XAxis 
                    dataKey="month" 
                    label={{ value: 'Months', position: 'insideBottom', offset: -10 }}
                  />
                  <YAxis 
                    label={{ value: 'Value ($)', angle: -90, position: 'insideLeft' }}
                    tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
                  />
                  <Tooltip 
                    formatter={(value: number, name: string) => [
                      `$${value.toLocaleString()}`, 
                      name === 'dca' ? 'DCA Growth' : 'Lump Sum Growth'
                    ]}
                    labelFormatter={(label) => `Month ${label}`}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="dca" 
                    stroke="hsl(var(--success))" 
                    strokeWidth={3}
                    name="DCA Growth"
                    dot={false}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="lumpSum" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={3}
                    name="Lump Sum Growth"
                    dot={false}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="contributions" 
                    stroke="hsl(var(--muted-foreground))" 
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    name="Contributions"
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-accent/20 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-4 h-4 text-primary" />
                <h4 className="font-semibold">Key Insights</h4>
              </div>
              <div className="text-sm text-muted-foreground space-y-1">
                <p>• DCA reduces timing risk by spreading purchases over time</p>
                <p>• Lump sum can perform better in consistently rising markets</p>
                <p>• DCA is psychologically easier and builds investing habits</p>
                <p>• Both strategies benefit from long-term compound growth</p>
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
};