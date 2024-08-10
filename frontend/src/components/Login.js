// src/components/Login.js
import React, { useState, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { getCsrfToken } from '../utils/csrfToken';


const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { login, fetchUser } = useContext(AuthContext);

  const handleSubmit = (event) => {
    event.preventDefault();
  
    const csrfToken = getCsrfToken();  // Get the CSRF token
    
    const baseUrl = process.env.REACT_APP_API_BASE_URL;
    
    axios.post('${baseUrl}/myapp/api/login/', 
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
          console.error('Login failed:', response.data.error);
        }
      })
      .catch(error => {
        console.error('There was an error logging in!', error);
      });
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
