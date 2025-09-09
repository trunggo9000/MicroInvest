import { TrendingUp, DollarSign, Shield } from "lucide-react";

export const AppHeader = () => {
  return (
    <header className="border-b bg-card/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-primary/10 p-2 rounded-lg">
              <TrendingUp className="w-8 h-8 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary">MicroInvest</h1>
              <p className="text-sm text-muted-foreground">Smart investing for students</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center gap-6 text-sm">
            <div className="flex items-center gap-2 text-muted-foreground">
              <Shield className="w-4 h-4 text-success" />
              <span>Low-risk focused</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <DollarSign className="w-4 h-4 text-primary" />
              <span>Start with $10</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};