import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Download, FileText, Share2 } from "lucide-react";
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

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

interface PDFExportProps {
  portfolio: PortfolioData;
  riskTolerance: string;
  investmentGoal: string;
}

export const PDFExport = ({ portfolio, riskTolerance, investmentGoal }: PDFExportProps) => {
  const [isGenerating, setIsGenerating] = useState(false);

  const generatePDF = async () => {
    setIsGenerating(true);
    
    try {
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 20;
      let yPosition = margin;

      // Header
      pdf.setFontSize(24);
      pdf.setTextColor(33, 102, 204); // Primary color
      pdf.text('Personalized Investment Portfolio', margin, yPosition);
      yPosition += 15;

      pdf.setFontSize(12);
      pdf.setTextColor(100, 100, 100);
      pdf.text(`Generated on ${new Date().toLocaleDateString()}`, margin, yPosition);
      yPosition += 20;

      // Portfolio Overview
      pdf.setFontSize(16);
      pdf.setTextColor(0, 0, 0);
      pdf.text('Portfolio Overview', margin, yPosition);
      yPosition += 10;

      pdf.setFontSize(11);
      pdf.text(`Risk Profile: ${riskTolerance.charAt(0).toUpperCase() + riskTolerance.slice(1)}`, margin, yPosition);
      yPosition += 6;
      pdf.text(`Investment Goal: ${investmentGoal}`, margin, yPosition);
      yPosition += 6;
      pdf.text(`Time Horizon: ${portfolio.timeframe}`, margin, yPosition);
      yPosition += 6;
      pdf.text(`Monthly Investment: $${portfolio.monthlyAmount}`, margin, yPosition);
      yPosition += 6;
      pdf.text(`Expected Annual Return: ${portfolio.totalExpectedReturn.toFixed(1)}%`, margin, yPosition);
      yPosition += 6;
      pdf.text(`Projected Value: $${portfolio.projectedValue.toLocaleString()}`, margin, yPosition);
      yPosition += 20;

      // Investment Allocation
      pdf.setFontSize(16);
      pdf.text('Recommended Allocation', margin, yPosition);
      yPosition += 15;

      // Table headers
      pdf.setFontSize(10);
      pdf.setTextColor(100, 100, 100);
      const colWidths = [40, 70, 25, 25, 20];
      const colPositions = [margin, margin + colWidths[0], margin + colWidths[0] + colWidths[1], 
                          margin + colWidths[0] + colWidths[1] + colWidths[2], 
                          margin + colWidths[0] + colWidths[1] + colWidths[2] + colWidths[3]];
      
      pdf.text('Symbol', colPositions[0], yPosition);
      pdf.text('Name', colPositions[1], yPosition);
      pdf.text('Allocation', colPositions[2], yPosition);
      pdf.text('Expected Return', colPositions[3], yPosition);
      pdf.text('Risk', colPositions[4], yPosition);
      yPosition += 8;

      // Table content
      pdf.setTextColor(0, 0, 0);
      portfolio.investments.forEach((investment) => {
        if (yPosition > pageHeight - 30) {
          pdf.addPage();
          yPosition = margin;
        }

        pdf.text(investment.symbol, colPositions[0], yPosition);
        pdf.text(investment.name.length > 25 ? investment.name.substring(0, 25) + '...' : investment.name, colPositions[1], yPosition);
        pdf.text(`${investment.allocation}%`, colPositions[2], yPosition);
        pdf.text(`${investment.expectedReturn.toFixed(1)}%`, colPositions[3], yPosition);
        pdf.text(investment.riskLevel, colPositions[4], yPosition);
        yPosition += 6;
      });

      yPosition += 15;

      // Investment Descriptions
      if (yPosition > pageHeight - 50) {
        pdf.addPage();
        yPosition = margin;
      }

      pdf.setFontSize(16);
      pdf.text('Investment Details', margin, yPosition);
      yPosition += 15;

      pdf.setFontSize(10);
      portfolio.investments.forEach((investment) => {
        if (yPosition > pageHeight - 40) {
          pdf.addPage();
          yPosition = margin;
        }

        pdf.setFontSize(12);
        pdf.setTextColor(33, 102, 204);
        pdf.text(`${investment.symbol} - ${investment.name}`, margin, yPosition);
        yPosition += 8;

        pdf.setFontSize(10);
        pdf.setTextColor(0, 0, 0);
        const splitDescription = pdf.splitTextToSize(investment.description, pageWidth - 2 * margin);
        pdf.text(splitDescription, margin, yPosition);
        yPosition += splitDescription.length * 4 + 8;
      });

      // Add projection chart explanation
      if (yPosition > pageHeight - 40) {
        pdf.addPage();
        yPosition = margin;
      }

      pdf.setFontSize(16);
      pdf.text('Growth Projection', margin, yPosition);
      yPosition += 15;

      pdf.setFontSize(11);
      const projectionText = [
        `With a monthly investment of $${portfolio.monthlyAmount} over ${portfolio.timeframe},`,
        `your portfolio is projected to reach $${portfolio.projectedValue.toLocaleString()}.`,
        '',
        'This projection assumes:',
        `• Consistent monthly contributions of $${portfolio.monthlyAmount}`,
        `• Average annual return of ${portfolio.totalExpectedReturn.toFixed(1)}%`,
        '• No withdrawals during the investment period',
        '• Reinvestment of all returns',
        '',
        'Important Disclaimers:',
        '• Past performance does not guarantee future results',
        '• Investment values may fluctuate and principal may be lost',
        '• Projections are estimates based on historical data',
        '• Consider consulting with a financial advisor for personalized advice'
      ];

      projectionText.forEach((line) => {
        if (yPosition > pageHeight - 20) {
          pdf.addPage();
          yPosition = margin;
        }
        pdf.text(line, margin, yPosition);
        yPosition += 5;
      });

      // Footer
      pdf.setFontSize(8);
      pdf.setTextColor(150, 150, 150);
      pdf.text('Generated by AI-Powered Investment Advisor', margin, pageHeight - 10);
      
      pdf.save(`investment-portfolio-${new Date().toISOString().split('T')[0]}.pdf`);
      
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('There was an error generating the PDF. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateCSV = () => {
    const csvContent = [
      ['Investment Portfolio Summary'],
      ['Generated Date', new Date().toLocaleDateString()],
      ['Risk Profile', riskTolerance],
      ['Investment Goal', investmentGoal],
      ['Time Horizon', portfolio.timeframe],
      ['Monthly Investment', `$${portfolio.monthlyAmount}`],
      ['Expected Annual Return', `${portfolio.totalExpectedReturn.toFixed(1)}%`],
      ['Projected Value', `$${portfolio.projectedValue.toLocaleString()}`],
      [''],
      ['Investment Allocations'],
      ['Symbol', 'Name', 'Allocation %', 'Expected Return %', 'Risk Level', 'Monthly Amount'],
      ...portfolio.investments.map(inv => [
        inv.symbol,
        inv.name,
        inv.allocation,
        inv.expectedReturn.toFixed(1),
        inv.riskLevel,
        `$${Math.round((portfolio.monthlyAmount * inv.allocation) / 100)}`
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `investment-portfolio-${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const sharePortfolio = () => {
    const shareText = `My AI-recommended investment portfolio:
Monthly Investment: $${portfolio.monthlyAmount}
Expected Return: ${portfolio.totalExpectedReturn.toFixed(1)}%
Projected Value: $${portfolio.projectedValue.toLocaleString()} in ${portfolio.timeframe}

Allocations:
${portfolio.investments.map(inv => `• ${inv.symbol}: ${inv.allocation}%`).join('\n')}

#investing #portfolio #financialplanning`;

    if (navigator.share) {
      navigator.share({
        title: 'My Investment Portfolio',
        text: shareText,
      });
    } else {
      navigator.clipboard.writeText(shareText).then(() => {
        alert('Portfolio summary copied to clipboard!');
      });
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-primary">
          <FileText className="w-5 h-5" />
          Export & Share Portfolio
        </CardTitle>
        <p className="text-muted-foreground">
          Download your personalized portfolio as PDF or CSV, or share with others
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Button
            onClick={generatePDF}
            disabled={isGenerating}
            className="flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            {isGenerating ? 'Generating...' : 'Download PDF'}
          </Button>
          
          <Button
            onClick={generateCSV}
            variant="outline"
            className="flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Download CSV
          </Button>
          
          <Button
            onClick={sharePortfolio}
            variant="outline"
            className="flex items-center gap-2"
          >
            <Share2 className="w-4 h-4" />
            Share Portfolio
          </Button>
        </div>

        <div className="mt-6 bg-accent/20 rounded-lg p-4">
          <h4 className="font-semibold mb-2">What's Included</h4>
          <div className="text-sm text-muted-foreground space-y-1">
            <p>• <strong>PDF:</strong> Complete portfolio report with allocations, projections, and investment details</p>
            <p>• <strong>CSV:</strong> Spreadsheet-friendly data for further analysis</p>
            <p>• <strong>Share:</strong> Summary text perfect for social media or messaging</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};