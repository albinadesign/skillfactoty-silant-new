import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../../context/AuthContext';
import './AuthPage.css';

function AuthPage() {
  const modalRef = useRef();
  const navigate = useNavigate();
  const { setIsAuthenticated, setUser } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  function getCsrfToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
  }

  const handleClickOutside = (event) => {
    if (modalRef.current && !modalRef.current.contains(event.target)) {
      navigate('/');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const csrfToken = getCsrfToken();

    try {
      const response = await axios.post('http://localhost:8000/accounts/login/', {
        username: username,
        password: password
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true
      });

      if (response.status === 200 && response.data.message === 'Авторизация успешна') {
        console.log('Авторизация успешна');
        const token = response.data.token; // Получение токена из ответа
        localStorage.setItem('token', token); // Сохранение токена в localStorage
        setIsAuthenticated(true);
        navigate('/');
        const userDetailsResponse = await axios.get(`http://localhost:8000/accounts/user/details/${username}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setUser(userDetailsResponse.data);
        navigate('/');
      } else {
        setError('Неправильный логин или пароль');
      }
    } catch (error) {
      console.error('Ошибка при аутентификации:', error);
      setError('Ошибка при попытке входа');
    }
  };



  return (
    <div className="auth-page" onClick={handleClickOutside}>
      <div className="auth-form" ref={modalRef}>
        <h1>Авторизация</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Логин"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            autoComplete="current-password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Войти</button>
        </form>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default AuthPage;
