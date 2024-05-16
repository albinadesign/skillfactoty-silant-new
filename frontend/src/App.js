import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext'; 

import './App.css';
import './assets/fonts.css';
import Header from './components/Header/Header';
import Main from './components/Main/Main';
import Footer from './components/Footer/Footer';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Header />
          <Main />
          <Footer />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
