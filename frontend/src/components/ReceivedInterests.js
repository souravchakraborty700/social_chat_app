// src/components/ReceivedInterests.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ReceivedInterests = () => {
    const [interests, setInterests] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/myapp/api/received-interests/', { withCredentials: true })
            .then(response => setInterests(response.data))
            .catch(error => console.error('There was an error fetching the interests!', error));
    }, []);

    return (
        <div>
            <h1>Received Interests</h1>
            <ul>
                {interests.map(interest => (
                    <li key={interest.id}>{interest.sender__username}: {interest.message}</li>
                ))}
            </ul>
        </div>
    );
};

export default ReceivedInterests;
