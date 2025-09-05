import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend, BarChart, Bar, XAxis, YAxis } from 'recharts';
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { PieChart as PieChartIcon, BarChart3 } from "lucide-react";

interface Investment {
  symbol: string;
  name: string;
  allocation: number;
  expectedReturn: number;
  riskLevel: "low" | "medium" | "high";
}

interface PortfolioHeatmapProps {
  investments: Investment[];
  monthlyAmount: number;
}

// Define sectors for each investment
const sectorMappings: Record<string, string> = {
  "VOO": "Diversified",
  "VTI": "Diversified", 
  "AAPL": "Technology",
  "MSFT": "Technology",
  "BND": "Bonds",
  "QQQ": "Technology"
};

const COLORS = [
  'hsl(var(--primary))',
  'hsl(var(--success))', 
  'hsl(var(--warning))',
  'hsl(var(--error))',
  'hsl(var(--accent))',
  'hsl(var(--muted-foreground))'
];

const RISK_COLORS = {
  low: 'hsl(var(--success))',
  medium: 'hsl(var(--warning))',
  high: 'hsl(var(--error))'
};

export const PortfolioHeatmap = ({ investments, monthlyAmount }: PortfolioHeatmapProps) => {
  const [viewType, setViewType] = useState<'allocation' | 'sector' | 'risk'>('allocation');

  // Prepare allocation data
  const allocationData = investments.map((investment, index) => ({
    name: investment.symbol,
    fullName: investment.name,
    value: investment.allocation,
    amount: Math.round((monthlyAmount * investment.allocation) / 100),
    color: COLORS[index % COLORS.length]
  }));

  // Prepare sector data
  const sectorData = investments.reduce((acc: any[], investment) => {
    const sector = sectorMappings[investment.symbol] || 'Other';
    const existing = acc.find(item => item.name === sector);
    
    if (existing) {
      existing.value += investment.allocation;
      existing.amount += Math.round((monthlyAmount * investment.allocation) / 100);
    } else {
      acc.push({
        name: sector,
        value: investment.allocation,
        amount: Math.round((monthlyAmount * investment.allocation) / 100),
        color: COLORS[acc.length % COLORS.length]
      });
    }
    
    return acc;
  }, []);

  // Prepare risk data
  const riskData = investments.reduce((acc: any[], investment) => {
    const existing = acc.find(item => item.name === investment.riskLevel);
    
    if (existing) {
      existing.value += investment.allocation;
      existing.amount += Math.round((monthlyAmount * investment.allocation) / 100);
    } else {
      acc.push({
        name: investment.riskLevel,
        value: investment.allocation,
        amount: Math.round((monthlyAmount * investment.allocation) / 100),
        color: RISK_COLORS[investment.riskLevel as keyof typeof RISK_COLORS]
      });
    }
    
    return acc;
  }, []);

  const getCurrentData = () => {
    switch (viewType) {
      case 'sector': return sectorData;
      case 'risk': return riskData;
      default: return allocationData;
    }
  };

  const currentData = getCurrentData();

  const renderCustomLabel = ({ name, value }: any) => {
    return value > 5 ? `${name} ${value}%` : '';
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-primary">
          <PieChartIcon className="w-5 h-5" />
          Portfolio Diversification Analysis
        </CardTitle>
        <p className="text-muted-foreground">
          Visualize your portfolio allocation across different dimensions
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex gap-2 flex-wrap">
          <Button
            variant={viewType === 'allocation' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewType('allocation')}
          >
            By Investment
          </Button>
          <Button
            variant={viewType === 'sector' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewType('sector')}
          >
            By Sector
          </Button>
          <Button
            variant={viewType === 'risk' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewType('risk')}
          >
            By Risk Level
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pie Chart */}
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={currentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={renderCustomLabel}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {currentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value: number, name: string, props: any) => [
                    `${value}% ($${props.payload.amount})`,
                    viewType === 'allocation' ? props.payload.fullName || name : name
                  ]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart */}
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={currentData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                <XAxis 
                  dataKey="name" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  interval={0}
                />
                <YAxis label={{ value: 'Allocation %', angle: -90, position: 'insideLeft' }} />
                <Tooltip 
                  formatter={(value: number, name: string, props: any) => [
                    `${value}% ($${props.payload.amount})`,
                    'Allocation'
                  ]}
                />
                <Bar dataKey="value" fill="hsl(var(--primary))">
                  {currentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Legend and Details */}
        <div className="space-y-4">
          <h4 className="font-semibold">Portfolio Breakdown</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {currentData.map((item, index) => (
              <div key={index} className="flex items-center gap-3 p-3 bg-accent/20 rounded-lg">
                <div 
                  className="w-4 h-4 rounded-full flex-shrink-0"
                  style={{ backgroundColor: item.color }}
                />
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate">
                    {viewType === 'allocation' && item.fullName ? item.fullName : item.name}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {item.value}% • ${item.amount}/month
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Diversification Score */}
        <div className="bg-primary/5 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <BarChart3 className="w-4 h-4 text-primary" />
            <h4 className="font-semibold">Diversification Analysis</h4>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="font-medium">Sector Spread: </span>
              <span className="text-muted-foreground">
                {sectorData.length} sector{sectorData.length !== 1 ? 's' : ''}
              </span>
            </div>
            <div>
              <span className="font-medium">Risk Balance: </span>
              <span className="text-muted-foreground">
                {riskData.length} risk level{riskData.length !== 1 ? 's' : ''}
              </span>
            </div>
            <div>
              <span className="font-medium">Largest Position: </span>
              <span className="text-muted-foreground">
                {Math.max(...allocationData.map(d => d.value))}%
              </span>
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Well-diversified portfolios typically have exposure across multiple sectors and risk levels.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};