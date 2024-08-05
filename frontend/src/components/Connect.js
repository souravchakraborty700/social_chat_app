// src/components/Connect.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

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
        <div>
            <h1>Connect</h1>
            <div>
                {contacts.map(contact => (
                    <div key={contact.interest_id}>
                        {contact.contact.username}
                        <Link to={`/chat/${contact.interest_id}`}>Chat</Link>
                        {contact.has_new_messages && <span> (new messages)</span>}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Connect;
