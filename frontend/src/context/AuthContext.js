import { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  const fetchUserDetails = async (username) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/accounts/user/details/${username}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user details:', error);
    }
  };

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await axios.get('http://localhost:8000/accounts/check_auth_status/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        console.log('Auth check response:', response.data);
        if (response.data.is_authenticated) {
          setIsAuthenticated(true);
          await fetchUserDetails(response.data.username);
        } else {
          logout();
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        logout();
      }
    } else {
      setLoading(false);
    }
    setLoading(false);
  };

  const logout = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        await axios.post('http://localhost:8000/accounts/logout/', {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/login');
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, user, setUser, logout, loading, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);








