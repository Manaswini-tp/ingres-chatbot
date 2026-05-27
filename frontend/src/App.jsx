import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import './App.css';

function App() {
  const [language, setLanguage] = useState('en');
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState(null);

  useEffect(() => {
    // Fetch available states
    const API_URL = 'https://ingres-chatbot-pyv6.onrender.com';
    axios.get(`${API_URL}/states`)
      .then(response => setStates(response.data))
      .catch(error => console.error('Error fetching states:', error));
  }, []);

  return (
    <div className="app-container">
      <Sidebar 
        states={states} 
        language={language}
        setLanguage={setLanguage}
        onStateSelect={setSelectedState}
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
}

export default App;
