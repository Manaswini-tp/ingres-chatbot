import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import Login from './components/Login';
import { useAuth, AuthProvider } from './context/AuthContext';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const AppContent = () => {
  const [language, setLanguage] = useState('en');
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  
  const { user, isAuthenticated, logout } = useAuth();

  useEffect(() => {
    // Fetch available states
    axios.get(`${API_URL}/states`)
      .then(response => setStates(response.data))
      .catch(error => console.error('Error fetching states:', error));
  }, []);

  return (
    <div className="app-container">
      {showLogin && <Login onClose={() => setShowLogin(false)} />}
      
      <Sidebar 
        states={states} 
        language={language}
        setLanguage={setLanguage}
        onStateSelect={setSelectedState}
        user={user}
        isAuthenticated={isAuthenticated}
        onLoginClick={() => setShowLogin(true)}
        onLogout={logout}
      />
      
      <div className="main-content">
        <header className="app-header">
          <div className="header-gradient">
            <h1>🌊 INGRES AI Assistant</h1>
            <p>Intelligent Groundwater Resource & Environmental System</p>
          </div>
        </header>
        
        <ChatWindow 
          language={language} 
          selectedState={selectedState}
        />
      </div>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
