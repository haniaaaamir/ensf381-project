// This was created to follow the format of the provided screenshot (only has Homepage link)
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from './Header.module.css';

const Header = () => {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div>
    <header className={styles.header}>
      <div className={styles.logoContainer}>
        <img src="/images/logo.jpg" alt="LMS Logo"className={styles.logo}/>
      </div>
      <h1 className={styles.title}>LMS - Learning Management System</h1>
      </header>
      
      <nav className={styles.nav}>
        <Link to="/" className={styles.navLink}>Home</Link>
      </nav>
 
      </div>
  );
};

export default Header;
