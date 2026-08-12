import React, { useState } from 'react';
import { FaPaperPlane } from 'react-icons/fa';

const MAX_CHARS = 500;

const InputBar = ({ onSend, language, disabled }) => {
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;

    setSending(true);
    onSend(input);
    setInput('');
    setTimeout(() => setSending(false), 300);
  };

  const charCount = input.length;
  const nearLimit = charCount > MAX_CHARS * 0.85;

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <div className="input-bar-inner">
        <span className="lang-badge">{language.toUpperCase()}</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value.slice(0, MAX_CHARS))}
          placeholder="Ask about groundwater data..."
          className="message-input"
          disabled={disabled}
        />
        {charCount > 0 && (
          <span className={`char-counter ${nearLimit ? 'near-limit' : ''}`}>
            {charCount}
          </span>
        )}
        <button
          type="submit"
          className={`send-button ${sending ? 'sending' : ''}`}
          disabled={!input.trim() || disabled}
          aria-label="Send message"
        >
          <FaPaperPlane />
        </button>
      </div>
    </form>
  );
};

export default InputBar;
