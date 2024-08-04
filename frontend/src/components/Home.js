// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div>
            <h1>Home</h1>
            <nav>
                <ul>
                    <li><Link to="/users">User List</Link></li>
                    <li><Link to="/received-interests">Received Interests</Link></li>
                    <li><Link to="/connect">Connect</Link></li>
                    <li><Link to="/logout">Logout</Link></li>
                </ul>
            </nav>
        </div>
    );
};

export default Home;
