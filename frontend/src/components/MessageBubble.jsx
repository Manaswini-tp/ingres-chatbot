import React from 'react';
import DataCard from './DataCard';
import ChartDisplay from './ChartDisplay';

const MessageBubble = ({ message, onSuggestionClick }) => {
  return (
    <div className={`message-bubble ${message.type}`}>
      <div className="message-content">
        <p className="message-text">{message.text}</p>
        
        {message.chartData && (
          <ChartDisplay chartData={message.chartData} />
        )}
        
        {message.data && message.data.length > 0 && (
          <div className="data-cards">
            {message.data.map((item, idx) => (
              <DataCard key={idx} data={item} />
            ))}
          </div>
        )}
        
        {message.suggestions && message.suggestions.length > 0 && (
          <div className="suggestions">
            <span className="suggestions-label">Try these:</span>
            {message.suggestions.map((suggestion, idx) => (
              <button 
                key={idx} 
                className="suggestion-chip"
                onClick={() => onSuggestionClick(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}
      </div>
      <span className="message-time">{message.timestamp}</span>
    </div>
  );
};

export default MessageBubble;
