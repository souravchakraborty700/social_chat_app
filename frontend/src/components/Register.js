import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { getCsrfToken } from '../utils/csrfToken';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
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
            .then(response => {
                if (response.data.message === 'User registered successfully') {
                    navigate('/login');
                }
            })
            .catch(error => {
                if (error.response && error.response.status === 400) {
                    setErrorMessage('This user already exists. Try Login or register with a different Username.');
                } else {
                    console.error('There was an error registering!', error);
                }
            });
    };

    return (
        <div className="form-container">
            <h1>Register</h1>
            {errorMessage && (
                <div className="error-message">
                    <p>{errorMessage}</p>
                    <Link to="/login">
                        <button>Login</button>
                    </Link>
                </div>
            )}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div>
                    <label>Password</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;
