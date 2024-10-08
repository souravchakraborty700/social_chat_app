// src/components/Login.js
import React, { useState, useContext } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { getCsrfToken } from '../utils/csrfToken';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const { login, fetchUser } = useContext(AuthContext);

  const handleSubmit = (event) => {
    event.preventDefault();

    const csrfToken = getCsrfToken();  // Get the CSRF token
    const baseUrl = process.env.REACT_APP_API_BASE_URL;
    
    axios.post(`${baseUrl}/myapp/api/login/`, 
      { username, password }, 
      { 
        withCredentials: true,
        headers: { 
          'X-CSRFToken': csrfToken  // Include the CSRF token in the request headers
        }
      })
      .then(response => {
        if (response.data.message === 'Login successful') {
          login(response.data.user); // Update the user in context
          fetchUser(); // Fetch the user data
          navigate('/');
        } else {
          setErrorMessage('Incorrect username or password.');
        }
      })
      .catch(error => {
        if (error.response && error.response.status === 400) {
          setErrorMessage('Incorrect username or password.');
        } else {
          console.error('There was an error logging in!', error);
        }
      });
  };

  return (
    <div className="form-container">
      <h1>Login</h1>
      {errorMessage && (
        <div className="error-message">
          <p>{errorMessage}</p>
        </div>
      )}
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
        <button type="submit">Login</button>
      </form>
      <div className="register-link">
        <p>Don't have an account? <Link to="/register"><button className="register-button">Register</button></Link></p>
      </div>
    </div>
  );
};

export default Login;
