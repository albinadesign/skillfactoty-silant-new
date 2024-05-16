import React from 'react';
import { Route, Routes } from 'react-router-dom';
import styles from './Main.module.css';
import Home from './Home/Home';
import AuthPage from './AuthPage/AuthPage';
import Reference from './Reference/Reference';

function Main() {
  return (
    <main className={styles.main}>
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/reference/:directoryName/:name" element={<Reference />} />
        </Routes>
      </div>
    </main>
  );
}

export default Main;