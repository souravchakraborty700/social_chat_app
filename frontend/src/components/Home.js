// src/components/Home.js
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Home = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Home</h1>
      <nav>
        <ul>
          {user ? (
            <>
              <li><Link to="/users">User List</Link></li>
              <li><Link to="/received-interests">Received Interests</Link></li>
              <li><Link to="/connect">Connect</Link></li>
              <li><Link to="/logout">Logout</Link></li>
            </>
          ) : (
            <>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </>
          )}
        </ul>
      </nav>
    </div>
  );
};

export default Home;
