import React from 'react';
import OpportunityTable from './OpportunityTable';
import { AssessmentReport } from '../types';

interface ImpactAssessmentProps {
    report: AssessmentReport | null;
    loading: boolean;
}

const ImpactAssessment: React.FC<ImpactAssessmentProps> = ({ report, loading }) => {
    if (loading) {
        return (
            <section className="panel">
                <header className="panel__header">
                    <h2>Market Intelligence Output</h2>
                </header>
                <div className="panel__body">
                    <p className="panel__placeholder">Running assessment... fetching macro context and building opportunity set.</p>
                </div>
            </section>
        );
    }

    if (!report) {
        return (
            <section className="panel">
                <header className="panel__header">
                    <h2>Market Intelligence Output</h2>
                </header>
                <div className="panel__body">
                    <p className="panel__placeholder">
                        Submit an event to populate the headline summary, context, market impact, and cross-sector opportunity table.
                    </p>
                    <ul className="panel__helper-list">
                        <li>Capture the catalyst, expected timeline, and core policy or corporate levers.</li>
                        <li>The engine responds with a templated institutional-style brief for analyst refinement.</li>
                        <li>Sources are placeholders—replace with verified Bloomberg, Reuters, or filings.</li>
                    </ul>
                </div>
            </section>
        );
    }

    const { headlineSummary, eventContext, marketImpact, opportunities, summaryInsights, riskNote, citations, generatedAt } =
        report;

    return (
        <section className="panel">
            <header className="panel__header">
                <h2>Market Intelligence Output</h2>
                <span className="panel__timestamp">Generated: {new Date(generatedAt).toLocaleString()}</span>
            </header>

            <div className="panel__body">
                <article className="report-section" id="headline">
                    <h3>Headline Summary</h3>
                    <p>{headlineSummary}</p>
                </article>

                <article className="report-section" id="context">
                    <h3>Event Context</h3>
                    <p className="report-section__lead">{eventContext.overview}</p>
                    <div className="report-grid">
                        <div>
                            <h4>Timing</h4>
                            <p>{eventContext.timing}</p>
                        </div>
                        <div>
                            <h4>Significance</h4>
                            <p>{eventContext.significance}</p>
                        </div>
                    </div>
                    <ul className="report-list">
                        {eventContext.contextPoints.map((point, index) => (
                            <li key={`context-${index}`}>{point}</li>
                        ))}
                    </ul>
                </article>

                <article className="report-section" id="analysis">
                    <h3>Market Impact Analysis</h3>
                    <div className="report-grid">
                        <div>
                            <h4>Sentiment</h4>
                            <p>{marketImpact.sentiment}</p>
                        </div>
                        <div>
                            <h4>Macro Themes</h4>
                            <ul className="report-list">
                                {marketImpact.macroThemes.map((theme, index) => (
                                    <li key={`macro-${index}`}>{theme}</li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <h4>Sector Exposure</h4>
                            <ul className="report-list">
                                {marketImpact.sectorOutlook.map((outlook, index) => (
                                    <li key={`sector-${index}`}>{outlook}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                    <div className="horizon-grid">
                        {marketImpact.horizonImpacts.map(({ horizon, outlook }) => (
                            <div key={horizon} className="horizon-card">
                                <h5>{horizon}</h5>
                                <p>{outlook}</p>
                            </div>
                        ))}
                    </div>
                </article>

                <article className="report-section" id="opportunities">
                    <h3>Investment Opportunity Table</h3>
                    <OpportunityTable opportunities={opportunities} />
                </article>

                <article className="report-section">
                    <h3>Summary Insights</h3>
                    <ul className="report-list">
                        {summaryInsights.map((insight, index) => (
                            <li key={`insight-${index}`}>{insight}</li>
                        ))}
                    </ul>
                </article>

                <article className="report-section" id="risks">
                    <h3>Risk Note</h3>
                    <p>{riskNote}</p>
                </article>

                <article className="report-section" id="citations">
                    <h3>Citations</h3>
                    <ul className="report-list">
                        {citations.map((citation, index) => (
                            <li key={`citation-${index}`}>{citation}</li>
                        ))}
                    </ul>
                </article>
            </div>
        </section>
    );
};

export default ImpactAssessment;
