import React from 'react';
import EventForm from '../components/EventForm';
import ImpactAssessment from '../components/ImpactAssessment';
import { useAssessments } from '../hooks/useAssessments';
import { EventInput } from '../types';

const Dashboard: React.FC = () => {
    const { report, loading, generateReport, resetReport } = useAssessments();

    const handleSubmit = (eventInput: EventInput) => {
        generateReport(eventInput);
    };

    return (
        <div className="dashboard">
            <header className="dashboard__intro">
                <h1>Global Event-Driven Market Intelligence Analyst</h1>
                <p>
                    Outline a forward event, expected timing, and core catalysts to generate a structured mock
                    intelligence brief. The layout mirrors a sell-side style narrative with cross-sector positioning.
                </p>
            </header>
            <EventForm onSubmit={handleSubmit} loading={loading} onReset={resetReport} />
            <ImpactAssessment report={report} loading={loading} />
        </div>
    );
};

export default Dashboard;
