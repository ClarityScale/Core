import { useCallback, useState } from 'react';
import { AssessmentReport, EventInput } from '../types';
import { buildMockReport } from '../utils/mockReport';

export const useAssessments = () => {
    const [report, setReport] = useState<AssessmentReport | null>(null);
    const [lastEvent, setLastEvent] = useState<EventInput | null>(null);
    const [loading, setLoading] = useState(false);

    const generateReport = useCallback(async (eventInput: EventInput) => {
        setLoading(true);
        setLastEvent(eventInput);

        // Simulate processing latency to mirror an asynchronous analysis workflow.
        await new Promise((resolve) => setTimeout(resolve, 350));

        const nextReport = buildMockReport(eventInput);
        setReport(nextReport);
        setLoading(false);
    }, []);

    const resetReport = useCallback(() => {
        setReport(null);
        setLastEvent(null);
        setLoading(false);
    }, []);

    return {
        report,
        lastEvent,
        loading,
        generateReport,
        resetReport,
    };
};

export default useAssessments;
