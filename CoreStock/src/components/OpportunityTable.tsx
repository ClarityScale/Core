import React from 'react';
import { OpportunityRow } from '../types';

interface OpportunityTableProps {
    opportunities: OpportunityRow[];
}

const OpportunityTable: React.FC<OpportunityTableProps> = ({ opportunities }) => {
    if (!opportunities || opportunities.length === 0) {
        return <p className="panel__placeholder">No opportunities generated. Add drivers for richer mapping.</p>;
    }

    return (
        <div className="table-wrapper">
            <table className="opportunity-table">
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Company</th>
                        <th>Sector</th>
                        <th>Country</th>
                        <th>Expected Direction</th>
                        <th>Time Horizon</th>
                        <th>Mechanism of Impact</th>
                        <th>Investability Score</th>
                        <th>Rationale</th>
                        <th>Source(s)</th>
                    </tr>
                </thead>
                <tbody>
                    {opportunities.map(
                        ({
                            ticker,
                            company,
                            sector,
                            country,
                            expectedDirection,
                            timeHorizon,
                            mechanism,
                            investabilityScore,
                            rationale,
                            sources,
                        }) => (
                            <tr key={ticker}>
                                <td>{ticker}</td>
                                <td>{company}</td>
                                <td>{sector}</td>
                                <td>{country}</td>
                                <td>{expectedDirection}</td>
                                <td>{timeHorizon}</td>
                                <td>{mechanism}</td>
                                <td>{investabilityScore}</td>
                                <td>{rationale}</td>
                                <td>
                                    {sources.map((source, index) => (
                                        <span key={`${ticker}-source-${index}`}>
                                            {source}
                                            {index < sources.length - 1 ? '; ' : ''}
                                        </span>
                                    ))}
                                </td>
                            </tr>
                        ),
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default OpportunityTable;
