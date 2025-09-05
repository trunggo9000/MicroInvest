-- Create user profiles table
CREATE TABLE public.profiles (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  email TEXT,
  investor_level TEXT DEFAULT 'Beginner' CHECK (investor_level IN ('Beginner', 'Intermediate', 'Pro')),
  total_simulated_value DECIMAL(12,2) DEFAULT 0,
  portfolios_created INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  UNIQUE(user_id)
);

-- Create portfolios table
CREATE TABLE public.portfolios (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL DEFAULT 'My Portfolio',
  monthly_budget DECIMAL(10,2) NOT NULL,
  risk_tolerance TEXT NOT NULL CHECK (risk_tolerance IN ('low', 'medium', 'high')),
  investment_goal TEXT NOT NULL,
  time_horizon TEXT NOT NULL,
  esg_preference BOOLEAN DEFAULT false,
  allocation JSONB NOT NULL,
  expected_return DECIMAL(5,2) NOT NULL,
  risk_score INTEGER NOT NULL,
  projected_value DECIMAL(12,2) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create investment goals table
CREATE TABLE public.investment_goals (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  goal_name TEXT NOT NULL,
  target_amount DECIMAL(12,2) NOT NULL,
  target_date DATE NOT NULL,
  monthly_contribution DECIMAL(10,2) NOT NULL,
  progress DECIMAL(5,2) DEFAULT 0,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused')),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create risk assessment responses table
CREATE TABLE public.risk_assessments (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  responses JSONB NOT NULL,
  calculated_risk_tolerance TEXT NOT NULL CHECK (calculated_risk_tolerance IN ('low', 'medium', 'high')),
  score INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create leaderboard entries table
CREATE TABLE public.leaderboard_entries (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  portfolio_id UUID NOT NULL REFERENCES public.portfolios(id) ON DELETE CASCADE,
  simulated_return DECIMAL(8,2) NOT NULL,
  timeframe TEXT NOT NULL,
  anonymous_name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.portfolios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.investment_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.risk_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.leaderboard_entries ENABLE ROW LEVEL SECURITY;

-- Create policies for profiles
CREATE POLICY "Users can view their own profile" ON public.profiles
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own profile" ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile" ON public.profiles
  FOR UPDATE USING (auth.uid() = user_id);

-- Create policies for portfolios
CREATE POLICY "Users can view their own portfolios" ON public.portfolios
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own portfolios" ON public.portfolios
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own portfolios" ON public.portfolios
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own portfolios" ON public.portfolios
  FOR DELETE USING (auth.uid() = user_id);

-- Create policies for investment goals
CREATE POLICY "Users can view their own goals" ON public.investment_goals
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own goals" ON public.investment_goals
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own goals" ON public.investment_goals
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own goals" ON public.investment_goals
  FOR DELETE USING (auth.uid() = user_id);

-- Create policies for risk assessments
CREATE POLICY "Users can view their own risk assessments" ON public.risk_assessments
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own risk assessments" ON public.risk_assessments
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create policies for leaderboard (public read for leaderboard viewing)
CREATE POLICY "Anyone can view leaderboard entries" ON public.leaderboard_entries
  FOR SELECT USING (true);

CREATE POLICY "Users can create their own leaderboard entries" ON public.leaderboard_entries
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create function to update timestamps
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SET search_path = public;

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_portfolios_updated_at
  BEFORE UPDATE ON public.portfolios
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_investment_goals_updated_at
  BEFORE UPDATE ON public.investment_goals
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at_column();