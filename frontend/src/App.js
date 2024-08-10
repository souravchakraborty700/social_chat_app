import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import UserList from './components/UserList';
import ReceivedInterests from './components/ReceivedInterests';
import Connect from './components/Connect';
import Login from './components/Login';
import Register from './components/Register';
import Logout from './components/Logout';
import Chat from './components/Chat';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    
                    <Route element={<ProtectedRoute />}>
                        <Route path="/users" element={<UserList />} />
                        <Route path="/received-interests" element={<ReceivedInterests />} />
                        <Route path="/connect" element={<Connect />} />
                        <Route path="/logout" element={<Logout />} />
                        <Route path="/chat/:interestId" element={<Chat />} />
                    </Route>
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;
