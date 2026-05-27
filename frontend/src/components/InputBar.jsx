import React, { useState } from 'react';
import { FaPaperPlane } from 'react-icons/fa';  // ← FIXED: Removed unused FaMicrophone

const InputBar = ({ onSend, language }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={`Ask about groundwater data... (${language.toUpperCase()})`}
        className="message-input"
      />
      <button type="submit" className="send-button" disabled={!input.trim()}>
        <FaPaperPlane />
      </button>
    </form>
  );
};

export default InputBar;
