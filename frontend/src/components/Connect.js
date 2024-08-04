// src/components/Connect.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Connect = () => {
    const [contacts, setContacts] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/myapp/api/connect/', { withCredentials: true })
            .then(response => setContacts(response.data))
            .catch(error => console.error('There was an error fetching the contacts!', error));
    }, []);

    return (
        <div>
            <h1>Connect</h1>
            <ul>
                {contacts.map(contact => (
                    <li key={contact.id}>
                        {contact.sender__username} - {contact.recipient__username}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Connect;
