import React from 'react';

const Header: React.FC = () => {
    return (
        <header className="header">
            <div className="header__content">
                <div>
                    <h1 className="header__title">Global Event-Driven Market Intelligence Analyst</h1>
                    <p className="header__subtitle">
                        Event-triggered, cross-sector investment mapping built for rapid institutional workflows.
                    </p>
                </div>
                <nav className="header__nav">
                    <a href="#context">Context</a>
                    <a href="#analysis">Market Analysis</a>
                    <a href="#opportunities">Opportunities</a>
                    <a href="#risks">Risks</a>
                </nav>
            </div>
        </header>
    );
};

export default Header;
