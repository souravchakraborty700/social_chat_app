// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import UserList from './components/UserList';
import ReceivedInterests from './components/ReceivedInterests';
import Connect from './components/Connect';
import Chat from './components/Chat';
import Login from './components/Login';
import Register from './components/Register';
import Logout from './components/Logout';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users" element={<UserList />} />
        <Route path="/received-interests" element={<ReceivedInterests />} />
        <Route path="/connect" element={<Connect />} />
        <Route path="/chat/:interestId" element={<Chat />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
};

export default App;