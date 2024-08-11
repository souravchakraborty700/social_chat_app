// src/components/Header.js

import React, { useContext, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Header = () => {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    if (window.innerWidth <= 768) {  // Only toggle the menu on screens smaller than 769px
      setIsOpen(!isOpen);
    }
  };

  return (
    <header className="header">
      <div className="hamburger" onClick={toggleMenu}>
        <div className="hamburger-bar"></div>
        <div className="hamburger-bar"></div>
        <div className="hamburger-bar"></div>
      </div>
      <nav className={`nav-logged-in ${isOpen ? 'open' : ''}`}>
        <ul>
          <li><Link to="/" onClick={() => setIsOpen(false)}>Home</Link></li>
          <li><Link to="/connect" onClick={() => setIsOpen(false)}>Friends</Link></li>
          <li><Link to="/users" onClick={() => setIsOpen(false)}>People</Link></li>
          <li><Link to="/received-interests" onClick={() => setIsOpen(false)}>Notifications</Link></li>
          <li><Link to="/logout" onClick={() => setIsOpen(false)}>Logout</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
