// Mock investment recommendation engine
// In a real app, this would connect to financial APIs and ML models

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

interface BudgetRiskData {
  monthlyBudget: number;
  riskTolerance: "low" | "medium" | "high";
  investmentGoal: string;
  timeHorizon: string;
}

// Mock investment options
const INVESTMENT_OPTIONS: Investment[] = [
  {
    symbol: "VOO",
    name: "Vanguard S&P 500 ETF",
    allocation: 0,
    expectedReturn: 10.5,
    riskLevel: "low",
    description: "Tracks the S&P 500 index, providing broad market exposure with low fees. Perfect for long-term growth with reduced volatility."
  },
  {
    symbol: "VTI",
    name: "Vanguard Total Stock Market ETF",
    allocation: 0,
    expectedReturn: 10.8,
    riskLevel: "medium",
    description: "Invests in the entire U.S. stock market, including small, mid, and large-cap stocks for comprehensive market exposure."
  },
  {
    symbol: "AAPL",
    name: "Apple Inc.",
    allocation: 0,
    expectedReturn: 12.0,
    riskLevel: "medium",
    description: "Blue-chip technology stock with strong fundamentals and consistent growth. A stable choice for growth-oriented portfolios."
  },
  {
    symbol: "MSFT",
    name: "Microsoft Corporation",
    allocation: 0,
    expectedReturn: 11.5,
    riskLevel: "medium",
    description: "Leading technology company with diversified revenue streams in cloud computing, productivity software, and gaming."
  },
  {
    symbol: "BND",
    name: "Vanguard Total Bond Market ETF",
    allocation: 0,
    expectedReturn: 4.2,
    riskLevel: "low",
    description: "Provides exposure to the entire U.S. investment-grade bond market. Offers stability and income generation."
  },
  {
    symbol: "QQQ",
    name: "Invesco QQQ ETF",
    allocation: 0,
    expectedReturn: 13.2,
    riskLevel: "high",
    description: "Tracks the Nasdaq-100 index, focusing on technology and growth companies. Higher potential returns with increased volatility."
  }
];

export const generatePortfolioRecommendation = (userData: BudgetRiskData): PortfolioData => {
  const { monthlyBudget, riskTolerance, timeHorizon } = userData;
  
  // Calculate time multiplier for projections
  const timeMultipliers = {
    "3-months": 0.25,
    "6-months": 0.5,
    "1-year": 1,
    "2-years": 2,
    "5-years": 5
  };
  
  const timeMultiplier = timeMultipliers[timeHorizon as keyof typeof timeMultipliers] || 1;
  
  let selectedInvestments: Investment[];
  let totalExpectedReturn: number;
  let riskScore: number;
  
  // Algorithm to select investments based on risk tolerance
  switch (riskTolerance) {
    case "low":
      selectedInvestments = [
        { ...INVESTMENT_OPTIONS[0], allocation: 60 }, // VOO
        { ...INVESTMENT_OPTIONS[4], allocation: 30 }, // BND
        { ...INVESTMENT_OPTIONS[2], allocation: 10 }  // AAPL
      ];
      totalExpectedReturn = 7.8;
      riskScore = 2;
      break;
      
    case "medium":
      selectedInvestments = [
        { ...INVESTMENT_OPTIONS[0], allocation: 50 }, // VOO
        { ...INVESTMENT_OPTIONS[2], allocation: 25 }, // AAPL
        { ...INVESTMENT_OPTIONS[3], allocation: 15 }, // MSFT
        { ...INVESTMENT_OPTIONS[4], allocation: 10 }  // BND
      ];
      totalExpectedReturn = 9.8;
      riskScore = 4;
      break;
      
    case "high":
      selectedInvestments = [
        { ...INVESTMENT_OPTIONS[5], allocation: 40 }, // QQQ
        { ...INVESTMENT_OPTIONS[1], allocation: 30 }, // VTI
        { ...INVESTMENT_OPTIONS[2], allocation: 20 }, // AAPL
        { ...INVESTMENT_OPTIONS[3], allocation: 10 }  // MSFT
      ];
      totalExpectedReturn = 12.1;
      riskScore = 7;
      break;
      
    default:
      selectedInvestments = [{ ...INVESTMENT_OPTIONS[0], allocation: 100 }];
      totalExpectedReturn = 10.5;
      riskScore = 3;
  }
  
  // Calculate projected value using compound interest
  const monthlyContribution = monthlyBudget;
  const annualReturn = totalExpectedReturn / 100;
  const monthlyReturn = annualReturn / 12;
  const totalMonths = timeMultiplier * 12;
  
  // Future Value of Annuity formula
  const projectedValue = monthlyContribution * 
    (Math.pow(1 + monthlyReturn, totalMonths) - 1) / monthlyReturn;
  
  return {
    investments: selectedInvestments,
    totalExpectedReturn,
    riskScore,
    monthlyAmount: monthlyBudget,
    projectedValue: Math.round(projectedValue),
    timeframe: timeHorizon
  };
};