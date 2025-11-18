import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import dynamic from 'next/dynamic';
import { Send, Mic, MicOff, Download, MapPin, Filter } from 'lucide-react';

// Fix: Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { 
  ssr: false 
});

const EnhancedChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [isRecording, setIsRecording] = useState(false);
  const [availableStates, setAvailableStates] = useState([]);
  const [availableDistricts, setAvailableDistricts] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const messagesEndRef = useRef(null);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi' },
    { code: 'ta', name: 'Tamil' },
    { code: 'te', name: 'Telugu' },
    { code: 'kn', name: 'Kannada' },
    { code: 'ml', name: 'Malayalam' },
    { code: 'bn', name: 'Bengali' },
    { code: 'mr', name: 'Marathi' },
    { code: 'gu', name: 'Gujarati' }
  ];

  useEffect(() => {
    fetchAvailableStates();
    scrollToBottom();
  }, []);

  useEffect(() => {
    if (selectedState) {
      fetchAvailableDistricts(selectedState);
    } else {
      setAvailableDistricts([]);
    }
  }, [selectedState]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchAvailableStates = async () => {
    try {
      const response = await axios.get('http://localhost:8000/states');
      setAvailableStates(response.data.states);
    } catch (error) {
      console.error('Error fetching states:', error);
    }
  };

  const fetchAvailableDistricts = async (state) => {
    try {
      const response = await axios.get(`http://localhost:8000/districts?state=${encodeURIComponent(state)}`);
      setAvailableDistricts(response.data.districts);
    } catch (error) {
      console.error('Error fetching districts:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    let finalMessage = inputText;
    
    // Add location context to the message
    if (selectedDistrict) {
      finalMessage = `${finalMessage} for ${selectedDistrict} district`;
    } else if (selectedState) {
      finalMessage = `${finalMessage} in ${selectedState} state`;
    }

    const userMessage = {
      id: Date.now(),
      text: finalMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/query', {
        message: finalMessage,
        language: selectedLanguage,
        session_id: 'demo-session'
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.text,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        chart_data: response.data.chart_data,
        raw_data: response.data.raw_data,
        intent: response.data.intent
      };

      setMessages(prev => [...prev, botMessage]);
      
      // Update available districts based on response
      if (response.data.available_districts) {
        setAvailableDistricts(response.data.available_districts);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
  };

  const downloadData = (data, filename) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const quickActions = [
    { text: "Show groundwater recharge", emoji: "💧" },
    { text: "Compare extraction across districts", emoji: "📊" },
    { text: "Water availability for future use", emoji: "🔮" },
    { text: "Storage capacity analysis", emoji: "💾" }
  ];

  const handleQuickAction = (actionText) => {
    setInputText(actionText);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">🌊 Advanced Groundwater Insights</h1>
          <p className="text-blue-100">Comprehensive groundwater data analysis across Indian states and districts</p>
        </div>
      </div>

      {/* Location and Language Selector */}
      <div className="bg-white border-b p-3">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* State Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-1">
                <MapPin size={16} />
                State:
              </label>
              <select 
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All States</option>
                {availableStates.map(state => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>
            </div>

            {/* District Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-1">
                <Filter size={16} />
                District:
              </label>
              <select 
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                disabled={!selectedState}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                <option value="">All Districts</option>
                {availableDistricts.map(district => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))}
              </select>
            </div>

            {/* Language Selector */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Language:
              </label>
              <select 
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {languages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Quick Stats */}
            <div className="flex items-center">
              <div className="text-sm text-gray-600">
                <div><strong>{availableStates.length}</strong> States</div>
                <div><strong>{availableDistricts.length}</strong> Districts</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-blue-50 border-b p-3">
        <div className="container mx-auto">
          <div className="flex flex-wrap gap-2">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={() => handleQuickAction(action.text)}
                className="flex items-center gap-2 bg-white border border-blue-200 rounded-full px-4 py-2 text-sm text-blue-700 hover:bg-blue-100 transition-colors"
              >
                <span>{action.emoji}</span>
                {action.text}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 container mx-auto">
        <div className="space-y-4 max-w-6xl mx-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-4xl rounded-lg p-4 ${
                  message.sender === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : message.isError
                    ? 'bg-red-100 text-red-800 border border-red-300'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.text}</div>
                
                {message.intent && (
                  <div className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mt-2">
                    {message.intent.replace('_', ' ')}
                  </div>
                )}
                
                {message.chart_data && (
                  <div className="mt-4">
                    <Plot
                      data={message.chart_data.data}
                      layout={message.chart_data.layout}
                      config={{ responsive: true }}
                      className="w-full"
                    />
                    {message.raw_data && (
                      <button
                        onClick={() => downloadData(message.raw_data, 'groundwater_analysis.json')}
                        className="mt-2 flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700"
                      >
                        <Download size={16} />
                        Download Analysis Data
                      </button>
                    )}
                  </div>
                )}
                <div className={`text-xs mt-2 ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                  {message.timestamp}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-lg rounded-bl-none p-4 max-w-xs">
                <div className="flex items-center gap-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                  <span className="text-sm text-gray-500">Analyzing groundwater data...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-4">
        <div className="container mx-auto max-w-6xl">
          <div className="flex gap-2">
            <button
              onClick={toggleRecording}
              className={`p-3 rounded-lg ${
                isRecording ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            <div className="flex-1 relative">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about groundwater recharge, extraction, availability, storage... (e.g., कर्नाटक में भूजल रिचार्ज दिखाएं, Compare water extraction in Bangalore and Mumbai)"
                className="w-full border border-gray-300 rounded-lg py-3 px-4 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows="2"
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputText.trim()}
              className="bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={20} />
            </button>
          </div>
          <div className="text-xs text-gray-500 mt-2 text-center">
            Try: "groundwater recharge in Karnataka", "water extraction comparison", "future availability analysis", "storage capacity"
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedChatInterface;