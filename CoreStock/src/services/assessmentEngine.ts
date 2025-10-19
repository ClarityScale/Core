export interface Event {
    id: string;
    title: string;
    description: string;
    date: Date;
    impactLevel: 'low' | 'medium' | 'high';
}

export interface InvestmentOpportunity {
    id: string;
    eventId: string;
    opportunityDescription: string;
    potentialReturn: number;
}

export function assessMarketImpact(event: Event): string {
    switch (event.impactLevel) {
        case 'low':
            return 'Minimal impact expected.';
        case 'medium':
            return 'Moderate impact expected. Consider monitoring.';
        case 'high':
            return 'Significant impact expected. Immediate action recommended.';
        default:
            return 'Unknown impact level.';
    }
}

export function generateOpportunityTable(events: Event[]): InvestmentOpportunity[] {
    return events.map(event => ({
        id: event.id,
        eventId: event.id,
        opportunityDescription: `Opportunity based on event: ${event.title}`,
        potentialReturn: calculatePotentialReturn(event)
    }));
}

function calculatePotentialReturn(event: Event): number {
    switch (event.impactLevel) {
        case 'low':
            return 5; // 5% return
        case 'medium':
            return 10; // 10% return
        case 'high':
            return 20; // 20% return
        default:
            return 0; // No return for unknown impact
    }
}