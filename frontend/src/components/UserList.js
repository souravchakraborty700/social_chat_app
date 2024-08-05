import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getCsrfToken } from '../utils/csrfToken';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get('http://localhost:8000/myapp/api/users/', { withCredentials: true })
            .then(response => {
                setUsers(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the users!', error);
            });
    }, []);

    const sendInterest = (userId) => {
        axios.post(`http://localhost:8000/myapp/api/send-interest/${userId}/`, { message }, {
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
        <div className="container">
            <h1>User List</h1>
            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        {user.username} 
                        {user.status === 'contact' ? 'Contact' : (
                            user.status === 'sent' ? 'Request Sent' : (
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
                            )
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default UserList;
