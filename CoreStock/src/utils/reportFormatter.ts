import { AssessmentReport, OpportunityRow } from '../types';

const escapePipes = (value: string): string => value.replace(/\|/g, '\\|').replace(/\r?\n|\r/g, ' ');

const formatOpportunityRow = (row: OpportunityRow): string => {
    const cells = [
        row.ticker,
        row.company,
        row.sector,
        row.country,
        row.expectedDirection,
        row.timeHorizon,
        row.mechanism,
        row.investabilityScore.toString(),
        row.rationale,
        row.sources.join('; '),
    ];

    return `| ${cells.map((cell) => escapePipes(cell)).join(' | ')} |`;
};

export const formatReportAsMarkdown = (report: AssessmentReport): string => {
    const lines: string[] = [];

    lines.push('# Headline Summary');
    lines.push(report.headlineSummary.trim());
    lines.push('');

    lines.push('## Event Context');
    lines.push(report.eventContext.overview.trim());
    lines.push('');
    lines.push(`- **Timing:** ${report.eventContext.timing}`);
    lines.push(`- **Significance:** ${report.eventContext.significance}`);
    if (report.eventContext.contextPoints.length > 0) {
        lines.push('- **Key Drivers:**');
        report.eventContext.contextPoints.forEach((point) => {
            lines.push(`  - ${point}`);
        });
    }
    lines.push('');

    lines.push('## Market Impact Analysis');
    lines.push(`- **Sentiment:** ${report.marketImpact.sentiment}`);
    lines.push(`- **Macro Themes:** ${report.marketImpact.macroThemes.join('; ')}`);
    lines.push(`- **Sector Exposure:** ${report.marketImpact.sectorOutlook.join('; ')}`);
    if (report.marketImpact.horizonImpacts.length > 0) {
        lines.push('- **Time Horizons:**');
        report.marketImpact.horizonImpacts.forEach(({ horizon, outlook }) => {
            lines.push(`  - ${horizon}: ${outlook}`);
        });
    }
    lines.push('');

    lines.push('## Investment Opportunity Table');
    lines.push(
        '| Ticker | Company | Sector | Country | Expected Direction | Time Horizon | Mechanism of Impact | Investability Score | Rationale | Source(s) |',
    );
    lines.push('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |');
    report.opportunities.forEach((row) => {
        lines.push(formatOpportunityRow(row));
    });
    lines.push('');

    lines.push('## Summary Insights');
    report.summaryInsights.forEach((insight) => {
        lines.push(`- ${insight}`);
    });
    lines.push('');

    lines.push('## Risk Note');
    lines.push(report.riskNote.trim());
    lines.push('');

    lines.push('## Citations');
    report.citations.forEach((citation) => {
        lines.push(`- ${citation}`);
    });
    lines.push('');

    lines.push(`_Generated ${new Date(report.generatedAt).toLocaleString()}_`);

    return lines.join('\n');
};

export default formatReportAsMarkdown;
