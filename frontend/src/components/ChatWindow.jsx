import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import MessageBubble from './MessageBubble';
import InputBar from './InputBar';

const ChatWindow = ({ language, selectedState }) => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'Hello! I\'m your INGRES AI assistant. Ask me about groundwater data across India! 🌍💧',
      timestamp: new Date().toLocaleTimeString(),
      suggestions: ['Karnataka', 'Mysore', 'Show all states', 'Compare Karnataka and Kerala', 'Rainfall in Bangalore']
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      type: 'user',
      text,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Get API URL from environment variable (for production) or fallback to localhost
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: text,
        language: language
      });

      const botMessage = {
        type: 'bot',
        text: response.data.response,
        data: response.data.data,
        suggestions: response.data.suggestions,
        chartData: response.data.chart_data,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again. 😔',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Chat error:', error);
    } finally {
      setIsTyping(false);
    }
  };

  useEffect(() => {
    if (selectedState) {
      sendMessage(`Tell me about ${selectedState}`);
    }
  }, [selectedState, sendMessage]);  // ← FIXED: Added sendMessage

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <MessageBubble 
            key={idx} 
            message={msg} 
            onSuggestionClick={handleSuggestionClick}
          />
        ))}
        {isTyping && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className="typing-text">INGRES is thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <InputBar onSend={sendMessage} language={language} />
    </div>
  );
};

export default ChatWindow;
