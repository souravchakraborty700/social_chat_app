import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log('useEffect triggered - fetching user');
        fetchUser();
    }, []);

    const fetchUser = async () => {
        try {
            const response = await axios.get('https://sourav-social-chat-app-62eb0b733f26.herokuapp.com/myapp/api/check-auth/', { withCredentials: true });
            console.log('Fetched user:', response.data.user);  // Debugging line
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
