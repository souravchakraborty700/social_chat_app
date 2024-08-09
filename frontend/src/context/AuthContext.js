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
            console.log('Full response:', response);  // Log the full response for debugging
            setUser(response.data.user);  // Make sure you're setting the correct part of the response
            console.log('User state after fetch:', response.data.user);  // Check if the user is set correctly
        } catch (error) {
            console.error('Error fetching user:', error);
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
