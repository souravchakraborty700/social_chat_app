import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { getCsrfToken } from '../utils/csrfToken';

const ReceivedInterests = () => {
    const [interests, setInterests] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:8000/myapp/api/received-interests/', { withCredentials: true })
            .then(response => {
                setInterests(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the received interests!', error);
            });
    }, []);

    const acceptInterest = (interestId) => {
        axios.post(`http://localhost:8000/myapp/api/accept-interest/${interestId}/`, {}, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => {
            if (response.data.status === 'accepted') {
                navigate(`/chat/${response.data.interest_id}`);
            }
        })
        .catch(error => {
            console.error('There was an error accepting the interest!', error);
        });
    };

    return (
        <div>
            <h1>Received Interests</h1>
            <ul>
                {interests.map(interest => (
                    <li key={interest.id}>
                        {interest.sender__username}: {interest.message}
                        <button onClick={() => acceptInterest(interest.id)}>Accept Request</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ReceivedInterests;
