// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { getCsrfToken } from '../utils/csrfToken';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();

    const csrfToken = getCsrfToken();  // Get the CSRF token
    const baseUrl = process.env.REACT_APP_API_BASE_URL;

    axios.post(`${baseUrl}/myapp/api/register/`, 
      { username, password }, 
      { 
        withCredentials: true,
        headers: { 
          'X-CSRFToken': csrfToken  // Include the CSRF token in the request headers
        }
      })
      .then(() => {
        // Directly redirect to the home page after successful registration
        navigate('/');
      })
      .catch(error => {
        console.error('There was an error registering!', error);
        // Optionally log the error or show a generic message
      });
  };

  return (
    <div className="form-container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
          />
        </div>
        <div>
          <label>Password</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
          />
        </div>
        <button type="submit">Register</button>
      </form>
      <div className="login-link">
        <p>Already have an account? <Link to="/login"><button className="login-button">Login</button></Link></p>
      </div>
    </div>
  );
};

export default Register;
