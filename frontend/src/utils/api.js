import axios from 'axios';
import { createBrowserHistory } from 'history';

const history = createBrowserHistory();

const api = axios.create({
  baseURL: 'http://localhost:8000/',
  withCredentials: true,
});


api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Если получена ошибка 401 (Unauthorized), перенаправляю на страницу входа
      history.push('/login');
    }
    return Promise.reject(error);
  }
);

export default api;

