// src/components/Connect.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Header from './Header';
import './Connect.css';

const Connect = () => {
    const [contacts, setContacts] = useState([]);

    useEffect(() => {
        fetchContacts();

        const notificationSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/notifications/'
        );

        notificationSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            // Handle notifications if needed
        };

        notificationSocket.onclose = function(e) {
            console.error('Notification socket closed unexpectedly');
        };

        return () => {
            notificationSocket.close();
        };
    }, []);

    const fetchContacts = () => {
        axios.get('http://localhost:8000/myapp/api/connect/', { withCredentials: true })
            .then(response => setContacts(response.data))
            .catch(error => console.error('Error fetching contacts:', error));
    };

    return (
        <>
            <Header />
            <div className="container">
                
                <ul>
                    {contacts.map(contact => (
                        <li key={contact.interest_id}>
                            <div>
                                <span>{contact.contact.username}</span>
                                <Link to={`/chat/${contact.interest_id}`} className="chat-button">Chat</Link>
                                {contact.has_new_messages && <span className="new-messages"> (new messages)</span>}
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
};

export default Connect;
