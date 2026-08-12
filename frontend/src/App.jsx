import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaBars } from 'react-icons/fa';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import AuthPage from './pages/AuthPage';
import ThemeToggle from './components/ThemeToggle';
import { useAuth } from './context/AuthContext';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const { user, loading } = useAuth();
  const [language, setLanguage] = useState('en');
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  

  useEffect(() => {
    axios.get(`${API_URL}/states`)
      .then(response => setStates(response.data))
      .catch(() => {});
  }, []);

  if (loading) {
    return (
      <div className="app-loading">
        <div className="app-loading-spinner" />
      </div>
    );
  }

  if (!user) {
    return <AuthPage />;
  }

  return (
    <>
      <div className="app-bg" />
      <div className="app-container">
        <div
          className={`sidebar-overlay ${sidebarOpen ? 'visible' : ''}`}
          onClick={() => setSidebarOpen(false)}
        />
        <Sidebar
          states={states}
          language={language}
          setLanguage={setLanguage}
          onStateSelect={setSelectedState}
          selectedState={selectedState}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />
        <div className="main-content">
          <header className="app-header">
            <div className="header-inner">
              <div className="header-left">
                <button
                  className="mobile-menu-btn"
                  onClick={() => setSidebarOpen(true)}
                  aria-label="Open menu"
                >
                  <FaBars />
                </button>
                <div className="header-title-group">
                  <h1>💧 INGRES AI Assistant</h1>
                  <p>Intelligent Groundwater Resource & Environmental System</p>
                </div>
              </div>
              <div className="header-actions">
                <div className="header-badge">
                  <span className="header-badge-dot" />
                  Online
                </div>
                <ThemeToggle />
              </div>
            </div>
          </header>
          <ChatWindow
            language={language}
            selectedState={selectedState}
          />
        </div>
      </div>
    </>
  );
}

export default App;
