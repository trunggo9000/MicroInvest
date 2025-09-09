import { useState } from "react";
import { AppHeader } from "@/components/AppHeader";
import { BudgetRiskForm } from "@/components/BudgetRiskForm";
import { PortfolioRecommendation } from "@/components/PortfolioRecommendation";
import { generatePortfolioRecommendation } from "@/utils/investmentEngine";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, Sparkles, TrendingUp, Shield, DollarSign } from "lucide-react";

interface BudgetRiskData {
  monthlyBudget: number;
  riskTolerance: "low" | "medium" | "high";
  investmentGoal: string;
  timeHorizon: string;
}

const Index = () => {
  const [step, setStep] = useState<"welcome" | "form" | "results">("welcome");
  const [isLoading, setIsLoading] = useState(false);
  const [portfolioData, setPortfolioData] = useState(null);
  const [formData, setFormData] = useState<BudgetRiskData | null>(null);

  const handleFormSubmit = async (data: BudgetRiskData) => {
    setIsLoading(true);
    
    // Simulate API processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const recommendation = generatePortfolioRecommendation(data);
    setPortfolioData(recommendation);
    setFormData(data);
    setIsLoading(false);
    setStep("results");
  };

  const handleStartOver = () => {
    setStep("welcome");
    setPortfolioData(null);
    setFormData(null);
  };

  const renderWelcome = () => (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-success/5">
      <AppHeader />
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Hero Section */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium">
              <Sparkles className="w-4 h-4" />
              AI-Powered Investment Advisor
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-foreground leading-tight">
              Start Investing with
              <span className="text-primary"> Just $10</span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Get personalized, data-driven investment recommendations designed specifically for students. 
              Build wealth with micro-investments that fit your budget and risk tolerance.
            </p>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">
            <Card className="p-6 hover:shadow-lg transition-all duration-300 border-primary/10">
              <CardContent className="text-center space-y-4 p-0">
                <div className="bg-success/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                  <Shield className="w-8 h-8 text-success" />
                </div>
                <h3 className="text-lg font-semibold">Low-Risk Focus</h3>
                <p className="text-muted-foreground">
                  Conservative strategies prioritizing capital preservation and steady growth
                </p>
              </CardContent>
            </Card>
            
            <Card className="p-6 hover:shadow-lg transition-all duration-300 border-primary/10">
              <CardContent className="text-center space-y-4 p-0">
                <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                  <TrendingUp className="w-8 h-8 text-primary" />
                </div>
                <h3 className="text-lg font-semibold">Data-Driven</h3>
                <p className="text-muted-foreground">
                  ML-powered recommendations based on historical market data and trends
                </p>
              </CardContent>
            </Card>
            
            <Card className="p-6 hover:shadow-lg transition-all duration-300 border-primary/10">
              <CardContent className="text-center space-y-4 p-0">
                <div className="bg-warning/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                  <DollarSign className="w-8 h-8 text-warning" />
                </div>
                <h3 className="text-lg font-semibold">Micro-Investing</h3>
                <p className="text-muted-foreground">
                  Start with small amounts and build your portfolio gradually over time
                </p>
              </CardContent>
            </Card>
          </div>

          {/* CTA Button */}
          <div className="pt-8">
            <Button 
              size="lg" 
              className="text-lg px-8 py-6 shadow-lg hover:shadow-xl transition-all duration-300"
              onClick={() => setStep("form")}
            >
              Get My Investment Plan
              <Sparkles className="ml-2 w-5 h-5" />
            </Button>
          </div>

          {/* Disclaimer */}
          <div className="pt-8 text-sm text-muted-foreground max-w-2xl mx-auto">
            <p>
              * This tool provides educational guidance and general investment suggestions. 
              Always consult with a financial advisor for personalized advice. 
              Past performance doesn't guarantee future results.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderForm = () => (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-success/5">
      <AppHeader />
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Button 
            variant="outline" 
            onClick={() => setStep("welcome")}
            className="gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
        </div>
        <BudgetRiskForm onSubmit={handleFormSubmit} isLoading={isLoading} />
      </div>
    </div>
  );

  const renderResults = () => (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-success/5">
      <AppHeader />
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6 flex justify-between items-center">
          <Button 
            variant="outline" 
            onClick={() => setStep("form")}
            className="gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Modify Profile
          </Button>
          <Button 
            variant="outline" 
            onClick={handleStartOver}
          >
            Start Over
          </Button>
        </div>
        {portfolioData && formData && (
          <PortfolioRecommendation 
            portfolio={portfolioData} 
            riskTolerance={formData.riskTolerance}
            investmentGoal={formData.investmentGoal}
          />
        )}
      </div>
    </div>
  );

  switch (step) {
    case "welcome":
      return renderWelcome();
    case "form":
      return renderForm();
    case "results":
      return renderResults();
    default:
      return renderWelcome();
  }
};

export default Index;