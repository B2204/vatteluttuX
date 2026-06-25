/**
 * VatteluttuX - Main Application Component
 */
import { useState } from 'react';
import { Header } from './components/Header';
import { RecognitionPage } from './components/RecognitionPage';
import { CharacterMappingViewer } from './components/CharacterMappingViewer';
import { HistoryPage } from './components/HistoryPage';
import './App.css';

type PageView = 'recognition' | 'mappings' | 'history';

function App() {
  const [currentView, setCurrentView] = useState<PageView>('recognition');

  return (
    <div className="app">
      <Header />
      <nav className="main-nav">
        <button
          className={`nav-button ${currentView === 'recognition' ? 'active' : ''}`}
          onClick={() => setCurrentView('recognition')}
        >
          🔍 OCR Recognition
        </button>
        <button
          className={`nav-button ${currentView === 'mappings' ? 'active' : ''}`}
          onClick={() => setCurrentView('mappings')}
        >
          📖 Character Mappings
        </button>
        <button
          className={`nav-button ${currentView === 'history' ? 'active' : ''}`}
          onClick={() => setCurrentView('history')}
        >
          📜 History
        </button>
      </nav>
      <main className="main-content">
        {currentView === 'recognition' && <RecognitionPage />}
        {currentView === 'mappings' && <CharacterMappingViewer />}
        {currentView === 'history' && <HistoryPage />}
      </main>
      <footer className="footer">
        <p>
          &copy; {new Date().getFullYear()} VatteluttuX - Ancient Tamil Script Recognition
        </p>
      </footer>
    </div>
  );
}

export default App;
