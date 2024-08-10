// src/components/UserList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getCsrfToken } from '../utils/csrfToken';
import Header from './Header';
import './UserList.css';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [message, setMessage] = useState('');
    const baseUrl = process.env.REACT_APP_API_BASE_URL;


    useEffect(() => {
        axios.get(`${baseUrl}/myapp/api/users/`, { withCredentials: true })
            .then(response => {
                setUsers(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the users!', error);
            });
    }, []);

    const sendInterest = (userId) => {
        axios.post(`${baseUrl}/myapp/api/send-interest/${userId}/`, { message }, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => {
            setUsers(users.map(user => 
                user.id === userId ? { ...user, status: 'sent' } : user
            ));
            setSelectedUser(null);
            setMessage('');
        })
        .catch(error => {
            console.error('There was an error sending interest!', error);
        });
    };

    const openMessageBox = (userId) => {
        setSelectedUser(userId);
    };

    return (
        <>
            <Header />
            <div className="container">
                
                <ul>
                    {users.map(user => (
                        <li key={user.id}>
                            <div>
                                <span>{user.username}</span>
                                {user.status === 'contact' ? (
                                    <button className="status-button">Contact</button>
                                ) : user.status === 'sent' ? (
                                    <button className="status-button">Request Sent</button>
                                ) : (
                                    selectedUser === user.id ? (
                                        <div>
                                            <textarea
                                                value={message}
                                                onChange={(e) => setMessage(e.target.value)}
                                                placeholder="Write your message here"
                                            />
                                            <button onClick={() => sendInterest(user.id)}>Send</button>
                                        </div>
                                    ) : (
                                        <button onClick={() => openMessageBox(user.id)}>Send Interest</button>
                                    )
                                )}
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
};

export default UserList;
