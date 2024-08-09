// src/components/ReceivedInterests.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { getCsrfToken } from '../utils/csrfToken';
import Header from './Header';
import './ReceivedInterests.css';

const ReceivedInterests = () => {
    const [interests, setInterests] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('https://sourav-social-chat-app-62eb0b733f26.herokuapp.com/myapp/api/received-interests/', { withCredentials: true })
            .then(response => {
                setInterests(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the received interests!', error);
            });
    }, []);

    const acceptInterest = (interestId) => {
        axios.post(`https://sourav-social-chat-app-62eb0b733f26.herokuapp.com/myapp/api/accept-interest/${interestId}/`, {}, {
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
        <>
            <Header />
            <div className="container">
                
                <ul>
                    {interests.map(interest => (
                        <li key={interest.id}>
                            <div>
                                <span>{interest.sender__username}: {interest.message}</span>
                                <button onClick={() => acceptInterest(interest.id)}>Accept Request</button>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
};

export default ReceivedInterests;
