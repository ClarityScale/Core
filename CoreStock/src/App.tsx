import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import './main.css';

const App: React.FC = () => {
    return (
        <div className="app-shell">
            <Header />
            <main className="app-shell__main">
                <Dashboard />
            </main>
            <Footer />
        </div>
    );
};

export default App;
