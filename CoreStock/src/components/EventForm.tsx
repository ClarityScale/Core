import React, { useState } from 'react';
import { EventInput } from '../types';

interface EventFormProps {
    onSubmit: (eventInput: EventInput) => void;
    onReset: () => void;
    loading: boolean;
}

const EventForm: React.FC<EventFormProps> = ({ onSubmit, onReset, loading }) => {
    const [name, setName] = useState('');
    const [expectedTiming, setExpectedTiming] = useState('');
    const [description, setDescription] = useState('');
    const [drivers, setDrivers] = useState('');

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const keyDrivers = drivers
            .split('\n')
            .map((line) => line.trim())
            .filter((line) => line.length > 0);

        const payload: EventInput = {
            name,
            expectedTiming,
            description,
            keyDrivers,
        };

        onSubmit(payload);
    };

    const handleReset = () => {
        setName('');
        setExpectedTiming('');
        setDescription('');
        setDrivers('');
        onReset();
    };

    return (
        <section className="panel">
            <header className="panel__header">
                <h2>1. Context Gathering</h2>
                <p className="panel__meta">
                    Provide high-level constraints, timing, and narrative drivers. The model returns a templated view
                    consistent with the sell-side brief requirements.
                </p>
            </header>
            <form className="event-form" onSubmit={handleSubmit}>
                <div className="form-grid">
                    <label className="form-field">
                        <span>Event Headline</span>
                        <input
                            type="text"
                            name="eventName"
                            value={name}
                            onChange={(event) => setName(event.target.value)}
                            placeholder="e.g., EU unveils continent-wide AI safety regime"
                            required
                        />
                    </label>
                    <label className="form-field">
                        <span>Expected Timing</span>
                        <input
                            type="text"
                            name="expectedTiming"
                            value={expectedTiming}
                            onChange={(event) => setExpectedTiming(event.target.value)}
                            placeholder="e.g., Q2 2026 (formal legislation vote)"
                        />
                    </label>
                </div>
                <label className="form-field">
                    <span>Event Narrative</span>
                    <textarea
                        name="description"
                        value={description}
                        onChange={(event) => setDescription(event.target.value)}
                        placeholder="Summarize what, who, and the policy or technology pivot expected."
                        rows={4}
                    />
                </label>
                <label className="form-field">
                    <span>Key Drivers &amp; Catalysts</span>
                    <textarea
                        name="drivers"
                        value={drivers}
                        onChange={(event) => setDrivers(event.target.value)}
                        placeholder="List each driver on a new line (e.g., Subsidy outline, Export control easing, Corporate capex commitments)"
                        rows={4}
                    />
                </label>
                <div className="form-actions">
                    <button type="submit" className="btn btn--primary" disabled={loading}>
                        {loading ? 'Generating...' : 'Generate Assessment'}
                    </button>
                    <button type="button" className="btn btn--ghost" onClick={handleReset} disabled={loading}>
                        Reset
                    </button>
                </div>
            </form>
        </section>
    );
};

export default EventForm;
