import React, { useState } from 'react';
import { FaGlobe, FaChevronDown, FaChevronUp, FaUser, FaSignOutAlt } from 'react-icons/fa';

const Sidebar = ({ 
  states, 
  language, 
  setLanguage, 
  onStateSelect,
  user,
  isAuthenticated,
  onLoginClick,
  onLogout
}) => {
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

      {/* ========== ADD AUTH SECTION ========== */}
      <div style={{ marginTop: 'auto', borderTop: '1px solid #e5e7eb' }}>
        {isAuthenticated ? (
          <div style={{ padding: '16px' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              gap: '12px'
            }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ 
                  fontWeight: '600', 
                  fontSize: '14px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  <FaUser style={{ color: '#667eea' }} />
                  <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {user?.full_name || user?.username}
                  </span>
                </div>
                <div style={{ fontSize: '12px', color: '#6b7280' }}>
                  {user?.query_count || 0} queries
                </div>
              </div>
              <button 
                onClick={onLogout}
                style={{
                  padding: '6px 14px',
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '13px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  whiteSpace: 'nowrap'
                }}
              >
                <FaSignOutAlt size={12} /> Logout
              </button>
            </div>
          </div>
        ) : (
          <div style={{ padding: '16px' }}>
            <button 
              onClick={onLoginClick}
              style={{
                width: '100%',
                padding: '10px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '600',
                transition: 'transform 0.2s, box-shadow 0.2s'
              }}
              onMouseEnter={(e) => {
                e.target.style.transform = 'scale(1.02)';
                e.target.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = 'none';
              }}
            >
              🔐 Sign In / Register
            </button>
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <p>💧Unlocking groundwater data, one question at a time</p>
        <p className="version">v3.0</p>
      </div>
    </div>
  );
};

export default Sidebar;
