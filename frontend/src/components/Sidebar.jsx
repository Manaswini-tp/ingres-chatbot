import React, { useState } from 'react';
import {
  FaGlobe, FaChevronDown, FaChevronUp, FaSearch,
  FaChartBar, FaBalanceScale, FaCloudRain, FaSignOutAlt
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';

const Sidebar = ({ states, language, setLanguage, onStateSelect, isOpen, onClose, selectedState }) => {
  const { user, logout } = useAuth();
  const [showStates, setShowStates] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳' },
    { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
    { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
    { code: 'bn', name: 'বাংলা', flag: '🇮🇳' },
    { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳' },
  ];

  const filteredStates = states.filter(state =>
    state.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const quickActions = [
    { icon: FaChartBar, label: 'Show all states', query: 'Show all states' },
    { icon: FaBalanceScale, label: 'Compare states', query: 'Compare Karnataka and Kerala' },
    { icon: FaCloudRain, label: 'Rainfall data', query: 'Rainfall in Bangalore' },
  ];

  const handleStateClick = (state) => {
    onStateSelect(state);
    onClose?.();
  };

  const handleQuickAction = (query) => {
    onStateSelect(query);
    onClose?.();
  };

  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">💧</div>
          <div className="sidebar-brand-text">
            <h2>INGRES AI</h2>
            <span>Groundwater System</span>
          </div>
        </div>
      </div>

      {user && (
        <div className="sidebar-profile">
          <div className="sidebar-avatar">{user.avatar}</div>
          <div className="sidebar-profile-info">
            <div className="sidebar-profile-name">{user.name}</div>
            <div className="sidebar-profile-email">{user.email}</div>
          </div>
          <button className="sidebar-logout" onClick={logout} title="Sign out">
            <FaSignOutAlt />
          </button>
        </div>
      )}

      <div className="sidebar-section">
        <div className="sidebar-section-title">
          <FaGlobe /> Language
        </div>
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
          <>
            <div className="states-search-wrapper">
              <FaSearch className="states-search-icon" />
              <input
                type="text"
                className="states-search"
                placeholder="Search states..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <div className="states-list">
              {filteredStates.map(state => (
                <button
                  key={state}
                  className={`state-item ${selectedState === state ? 'active' : ''}`}
                  onClick={() => handleStateClick(state)}
                >
                  {state}
                </button>
              ))}
              {filteredStates.length === 0 && (
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', padding: '8px 12px' }}>
                  No states found
                </p>
              )}
            </div>
          </>
        )}
      </div>

      <div className="sidebar-section">
        <div className="sidebar-section-title">Quick Actions</div>
        <div className="quick-actions">
          {quickActions.map(({ icon: Icon, label, query }) => (
            <button
              key={label}
              className="quick-action-btn"
              onClick={() => handleQuickAction(query)}
            >
              <Icon /> {label}
            </button>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <p>💧 Powered by AI</p>
        <p className="version">v2.0</p>
      </div>
    </aside>
  );
};

export default Sidebar;

