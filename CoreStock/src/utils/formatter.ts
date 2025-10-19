export const formatEventDate = (dateString: string): string => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

export const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
};

export const formatImpactScore = (score: number): string => {
    return score >= 0 ? `Positive Impact: ${score}` : `Negative Impact: ${Math.abs(score)}`;
};

export const formatOpportunity = (opportunity: { title: string; potentialReturn: number; riskLevel: string }): string => {
    return `${opportunity.title} - ${formatCurrency(opportunity.potentialReturn)} | Risk Level: ${opportunity.riskLevel}`;
};