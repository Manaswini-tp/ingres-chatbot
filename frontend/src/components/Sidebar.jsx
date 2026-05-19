import React, { useState } from 'react';
import { FaGlobe, FaChevronDown, FaChevronUp } from 'react-icons/fa';

const Sidebar = ({ states, language, setLanguage, onStateSelect }) => {
  const [showStates, setShowStates] = useState(false);

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳' },
    { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
    { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
    { code: 'bn', name: 'বাংলা', flag: '🇮🇳' },
    { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳' }
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>🗺️ Navigation</h2>
      </div>
      
      <div className="sidebar-section">
        <h3><FaGlobe /> Language</h3>
        <select 
          className="language-select"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          {languages.map(lang => (
            <option key={lang.code} value={lang.code}>
              {lang.flag} {lang.name}
            </option>
          ))}
        </select>
      </div>

      <div className="sidebar-section">
        <div 
          className="section-header"
          onClick={() => setShowStates(!showStates)}
        >
          <h3>📍 States ({states.length})</h3>
          {showStates ? <FaChevronUp /> : <FaChevronDown />}
        </div>
        
        {showStates && (
          <div className="states-list">
            {states.map(state => (
              <button
                key={state}
                className="state-item"
                onClick={() => onStateSelect(state)}
              >
                {state}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <p>💧 Powered by AI</p>
        <p className="version">v2.0</p>
      </div>
    </div>
  );
};

export default Sidebar;
