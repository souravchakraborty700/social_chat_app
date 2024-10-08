import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUser();
    }, []);
    const baseUrl = process.env.REACT_APP_API_BASE_URL;


    const fetchUser = async () => {
        try {
            const response = await axios.get(`${baseUrl}/myapp/api/check-auth/`, { withCredentials: true });
            setUser(response.data.user);
        } catch {
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    const login = (userData) => {
        setUser(userData);
    };

    const logout = () => {
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading, fetchUser }}>
            {children}
        </AuthContext.Provider>
    );
};
