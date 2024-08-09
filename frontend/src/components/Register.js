// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post('https://sourav-social-chat-app-62eb0b733f26.herokuapp.com/myapp/api/register/', { username, password }, { withCredentials: true })
            .then(response => {
                if (response.data.message === 'User registered successfully') {
                    navigate('/login');
                } else {
                    console.error('Registration failed:', response.data.error);
                }
            })
            .catch(error => {
                console.error('There was an error registering!', error);
            });
    };

    return (
        <div>
            <h1>Register</h1>
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
