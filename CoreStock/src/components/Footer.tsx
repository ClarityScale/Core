import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <p>
                &copy; {new Date().getFullYear()} Global Event-Driven Market Intelligence Analyst Template. Replace
                placeholder insights with validated research prior to distribution.
            </p>
        </footer>
    );
};

export default Footer;
