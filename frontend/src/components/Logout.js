// src/components/Logout.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Logout = () => {
    const navigate = useNavigate();
    const baseUrl = process.env.REACT_APP_API_BASE_URL;

    useEffect(() => {
        axios.post(`${baseUrl}/myapp/api/logout/`, {}, { withCredentials: true })
            .then(response => {
                navigate('/login');
            })
            .catch(error => {
                console.error('There was an error logging out!', error);
            });
    }, [navigate]);

    return <div>Logging out...</div>;
};

export default Logout;
