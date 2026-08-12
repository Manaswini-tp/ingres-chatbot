import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import MessageBubble from './MessageBubble';
import InputBar from './InputBar';

const QUICK_QUERIES = ['Show all states', 'Compare Karnataka and Kerala', 'Rainfall in Bangalore'];

const ChatWindow = ({ language, selectedState }) => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: "Hello! I'm your INGRES AI assistant. Ask me about groundwater data across India! 🌍💧",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      suggestions: ['Karnataka', 'Mysore', 'Show all states', 'Compare Karnataka and Kerala', 'Rainfall in Bangalore'],
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const lastStateRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (selectedState && selectedState !== lastStateRef.current) {
      lastStateRef.current = selectedState;
      const message = QUICK_QUERIES.includes(selectedState)
        ? selectedState
        : `Tell me about ${selectedState}`;
      sendMessage(message);
    }
  }, [selectedState]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      type: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        message: text,
        language,
      });

      const botMessage = {
        type: 'bot',
        text: response.data.response,
        data: response.data.data,
        suggestions: response.data.suggestions,
        chartData: response.data.chart_data,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch {
      const errorMessage = {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again. 😔',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <MessageBubble
            key={idx}
            message={msg}
            onSuggestionClick={sendMessage}
          />
        ))}
        {isTyping && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <span />
              <span />
              <span />
            </div>
            <span className="typing-text">INGRES is thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <InputBar onSend={sendMessage} language={language} disabled={isTyping} />
    </div>
  );
};

export default ChatWindow;
