import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('ingres-user');
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        localStorage.removeItem('ingres-user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password, rememberMe) => {
    await new Promise(resolve => setTimeout(resolve, 1200));
    if (!email || !password) throw new Error('Please fill in all fields');
    if (password.length < 6) throw new Error('Invalid credentials');

    const userData = {
      email,
      name: email.split('@')[0],
      avatar: email.charAt(0).toUpperCase(),
    };

    setUser(userData);
    if (rememberMe) {
      localStorage.setItem('ingres-user', JSON.stringify(userData));
    } else {
      sessionStorage.setItem('ingres-user', JSON.stringify(userData));
    }
    return userData;
  };

  const register = async (email, password, name) => {
    await new Promise(resolve => setTimeout(resolve, 1200));
    if (!email || !password || !name) throw new Error('Please fill in all fields');
    if (password.length < 6) throw new Error('Password must be at least 6 characters');

    const userData = { email, name, avatar: name.charAt(0).toUpperCase() };
    setUser(userData);
    localStorage.setItem('ingres-user', JSON.stringify(userData));
    return userData;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('ingres-user');
    sessionStorage.removeItem('ingres-user');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
