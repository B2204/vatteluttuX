import { useState, useEffect } from 'react';
import { checkHealth } from '../utils/api';
import './Header.css';

export function Header() {
    const [isApiOnline, setIsApiOnline] = useState<boolean | null>(null);

    useEffect(() => {
        const verifyHealth = async () => {
            try {
                const health = await checkHealth();
                setIsApiOnline(health.status === 'healthy');
            } catch (error) {
                console.error('API health check failed:', error);
                setIsApiOnline(false);
            }
        };

        verifyHealth();
        // Check every 30 seconds
        const interval = setInterval(verifyHealth, 30000);
        return () => clearInterval(interval);
    }, []);

    return (
        <header className="header">
            <div className="header-content">
                <div className="logo">
                    <span className="logo-icon">𑀅</span>
                    <h1>VatteluttuX</h1>
                </div>
                <div className="header-right">
                    <p className="tagline">Ancient Tamil Script Recognition</p>
                    <div className={`api-status ${isApiOnline === true ? 'online' : isApiOnline === false ? 'offline' : 'checking'}`}>
                        <span className="status-dot"></span>
                        <span className="status-text">
                            {isApiOnline === true ? 'API Online' : isApiOnline === false ? 'API Offline' : 'Checking API...'}
                        </span>
                    </div>
                </div>
            </div>
        </header>
    );
}
