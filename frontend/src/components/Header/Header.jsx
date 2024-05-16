import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

import styles from './Header.module.css';
import logo from '../../assets/images/logo.svg';
import api from '../../utils/api';


function Header() {
  const { isAuthenticated, setIsAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleAuthClick = async () => {
    if (isAuthenticated) {
      try {
        const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
        const token = localStorage.getItem('token'); // Получение токена из локального хранилища
        console.log('Token:', token);
        console.log('CSRF Token:', csrfToken);

        // Выход из системы
        const response = await api.post('accounts/logout/', {}, {
          headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': `Bearer ${token}` // Передача токена аутентификации
          }
        });

        if (response.status === 200) {
          setIsAuthenticated(false);
          localStorage.removeItem('token'); // Удаление токена из локального хранилища при выходе
          console.log('Статус авторизации после выхода:', false);
          navigate('/'); // Переадресация на главную страницу после выхода
        }
      } catch (error) {
        console.error('Ошибка при выходе из системы:', error);
      }
    } else {
      // Переход на страницу авторизации
      navigate('/login');
    }
  };


  return (
    <header className={styles.header}>
        <div className="header-content">
        <div className={styles.headerTop}>
          <img src={logo} alt="Logo" className={styles.logo} />
          <div className={styles.phone}>+7-8352-20-12-09, Telegram</div>
          <button className={styles.authButton} onClick={handleAuthClick}>
            {isAuthenticated ? 'Выйти' : 'Авторизация'}
          </button>
        </div>
        <div className={styles.headerBottom}>
          Электронная сервисная книжка "Мой Силант"
        </div>
      </div>
    </header>
  );
}

export default Header;