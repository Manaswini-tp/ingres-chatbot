import React, { useState } from 'react';
import { FaEnvelope, FaLock, FaEye, FaEyeSlash, FaUser } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import ThemeToggle from '../components/ThemeToggle';

const AuthPage = () => {
  const { login, register } = useAuth();
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [shake, setShake] = useState(false);

  const triggerShake = (msg) => {
    setError(msg);
    setShake(true);
    setTimeout(() => setShake(false), 600);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'login') {
        await login(email, password, rememberMe);
      } else {
        await register(email, password, name);
      }
    } catch (err) {
      triggerShake(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setMode(prev => (prev === 'login' ? 'register' : 'login'));
    setError('');
    setPassword('');
  };

  return (
    <div className="auth-page">
      <div className="auth-bg-gradient" />
      <div className="auth-bg-pattern" />

      <div className="auth-theme-toggle">
        <ThemeToggle />
      </div>

      <div className={`auth-card ${shake ? 'shake' : ''} fade-in`}>
        <div className="auth-brand">
          <div className="auth-logo">
            <span className="auth-logo-icon">💧</span>
          </div>
          <h1 className="auth-title">INGRES AI</h1>
          <p className="auth-tagline">Intelligent Groundwater Resource System</p>
        </div>

        <div className="auth-form-wrapper">
          <div className={`auth-form-slide ${mode}`}>
            <form onSubmit={handleSubmit} className="auth-form">
              <h2 className="auth-form-title">
                {mode === 'login' ? 'Welcome back' : 'Create account'}
              </h2>
              <p className="auth-form-subtitle">
                {mode === 'login'
                  ? 'Sign in to access groundwater insights'
                  : 'Join us to explore India\'s water data'}
              </p>

              {error && (
                <div className="auth-error" role="alert">
                  {error}
                </div>
              )}

              {mode === 'register' && (
                <div className="auth-input-group">
                  <FaUser className="auth-input-icon" />
                  <input
                    type="text"
                    placeholder="Full name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="auth-input"
                    autoComplete="name"
                  />
                </div>
              )}

              <div className="auth-input-group">
                <FaEnvelope className="auth-input-icon" />
                <input
                  type="email"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="auth-input"
                  autoComplete="email"
                />
              </div>

              <div className="auth-input-group">
                <FaLock className="auth-input-icon" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="auth-input auth-input-password"
                  autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
                />
                <button
                  type="button"
                  className="auth-password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>

              {mode === 'login' && (
                <div className="auth-options">
                  <label className="auth-checkbox">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                    />
                    <span className="auth-checkbox-mark" />
                    Remember me
                  </label>
                  <button type="button" className="auth-link">
                    Forgot password?
                  </button>
                </div>
              )}

              <button
                type="submit"
                className={`auth-submit ${loading ? 'loading' : ''}`}
                disabled={loading}
              >
                {loading ? (
                  <span className="auth-spinner" />
                ) : (
                  mode === 'login' ? 'Sign In' : 'Create Account'
                )}
              </button>
            </form>
          </div>
        </div>

        <div className="auth-switch">
          <span>
            {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
          </span>
          <button type="button" className="auth-switch-btn" onClick={toggleMode}>
            {mode === 'login' ? 'Register' : 'Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
