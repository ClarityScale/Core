export type Sentiment = 'Bullish' | 'Bearish' | 'Neutral';

export type TimeHorizon = 'Short-term (0–3 months)' | 'Medium-term (3–12 months)' | 'Long-term (1–5 years)';

export interface EventInput {
    name: string;
    expectedTiming: string;
    description: string;
    keyDrivers: string[];
}

export interface EventContext {
    overview: string;
    timing: string;
    significance: string;
    contextPoints: string[];
}

export interface TimeHorizonImpact {
    horizon: TimeHorizon;
    outlook: string;
}

export interface MarketImpact {
    sentiment: Sentiment;
    macroThemes: string[];
    sectorOutlook: string[];
    horizonImpacts: TimeHorizonImpact[];
}

export interface OpportunityRow {
    ticker: string;
    company: string;
    sector: string;
    country: string;
    expectedDirection: Sentiment;
    timeHorizon: TimeHorizon;
    mechanism: string;
    investabilityScore: number;
    rationale: string;
    sources: string[];
}

export interface AssessmentReport {
    generatedAt: string;
    headlineSummary: string;
    eventContext: EventContext;
    marketImpact: MarketImpact;
    opportunities: OpportunityRow[];
    summaryInsights: string[];
    riskNote: string;
    citations: string[];
}
