import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { getCsrfToken } from '../utils/csrfToken';
import Header from './Header';
import './ReceivedInterests.css';

const ReceivedInterests = () => {
    const [interests, setInterests] = useState([]);
    const navigate = useNavigate();
    const baseUrl = process.env.REACT_APP_API_BASE_URL;

    useEffect(() => {
        axios.get(`${baseUrl}/myapp/api/received-interests/`, { withCredentials: true })
            .then(response => {
                setInterests(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the received interests!', error);
            });
    }, [baseUrl]);

    const acceptInterest = (interestId) => {
        axios.post(`${baseUrl}/myapp/api/accept-interest/${interestId}/`, {}, {
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

    const rejectInterest = (interestId) => {
        axios.post(`${baseUrl}/myapp/api/reject-interest/${interestId}/`, {}, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => {
            if (response.status === 200) {
                setInterests(interests.filter(interest => interest.id !== interestId));
            }
        })
        .catch(error => {
            console.error('There was an error rejecting the interest!', error);
        });
    };

    return (
        <>
            <Header />
            <div className="container">
                {interests.length > 0 ? (
                    <ul>
                        {interests.map(interest => (
                            <li key={interest.id}>
                                <div>
                                    <span>{interest.sender__username}: {interest.message}</span>
                                    <button onClick={() => acceptInterest(interest.id)}>Accept Request</button>
                                    <button onClick={() => rejectInterest(interest.id)}>Reject Request</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <div className="no-notification">
                        <p>No notification! You're all good</p>
                    </div>                    
                )}
            </div>
        </>
    );
};

export default ReceivedInterests;
