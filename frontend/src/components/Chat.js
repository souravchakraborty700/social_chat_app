// // src/components/Chat.js
// import React, { useState, useEffect, useContext } from 'react';
// import { useParams } from 'react-router-dom';
// import axios from 'axios';
// import { AuthContext } from '../context/AuthContext';
// import Header from './Header';
// import './Chat.css';

// const Chat = () => {
//     const { interestId } = useParams();
//     const [messages, setMessages] = useState([]);
//     const [newMessage, setNewMessage] = useState('');
//     const [chatSocket, setChatSocket] = useState(null);
//     const { user } = useContext(AuthContext);

//     useEffect(() => {
//         fetchMessages();

//         const socket = new WebSocket(
//             'ws://' + window.location.hostname + ':8000/ws/chat/' + interestId + '/'
//         );

//         socket.onopen = function() {
//             setChatSocket(socket);
//             console.log('WebSocket connection opened');
//         };

//         socket.onmessage = function(e) {
//             const data = JSON.parse(e.data);
//             console.log('WebSocket message received:', data);
//             setMessages((prevMessages) => [...prevMessages, { text: data.message, username: data.username }]);
//         };

//         socket.onerror = function(e) {
//             console.error('WebSocket error:', e);
//         };

//         socket.onclose = function(e) {
//             console.error('Chat socket closed unexpectedly:', e);
//         };

//         return () => {
//             socket.close();
//         };
//     }, [interestId]);

//     const fetchMessages = () => {
//         axios.get(`http://localhost:8000/myapp/api/messages/${interestId}/`, { withCredentials: true })
//             .then(response => {
//                 setMessages(response.data);
//             })
//             .catch(error => console.error('Error fetching messages:', error));
//     };

//     const sendMessage = (e) => {
//         e.preventDefault();
//         if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
//             chatSocket.send(JSON.stringify({
//                 'message': newMessage
//             }));
//             setNewMessage('');
//         } else {
//             console.error('WebSocket is not open. Ready state:', chatSocket?.readyState);
//         }
//     };

//     return (
//         <>
//             <Header />
//             <div className="container">
//                 <h1>Chat</h1>
//                 <div className="chat-box">
//                     {messages.map((message, index) => (
//                         <div key={index} className="message">
//                             <strong>{message.username === user?.username ? 'You' : message.username}:</strong> {message.text}
//                         </div>
//                     ))}
//                 </div>
//                 <form onSubmit={sendMessage} className="chat-form">
//                     <input
//                         type="text"
//                         value={newMessage}
//                         onChange={(e) => setNewMessage(e.target.value)}
//                         placeholder="Type your message here"
//                     />
//                     <button type="submit">Send</button>
//                 </form>
//             </div>
//         </>
//     );
// };

// export default Chat;


// src/components/Chat.js
// src/components/Chat.js
// src/components/Chat.js
import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import Header from './Header';
import './Chat.css';

const Chat = () => {
    const { interestId } = useParams();
    const { user } = useContext(AuthContext);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [chatSocket, setChatSocket] = useState(null);

    useEffect(() => {
        fetchMessages();

        const socket = new WebSocket(
            'ws://' + window.location.hostname + ':8000/ws/chat/' + interestId + '/'
        );

        socket.onopen = function() {
            setChatSocket(socket);
            console.log('WebSocket connection opened');
        };

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log('WebSocket message received:', data);
            setMessages((prevMessages) => [...prevMessages, { text: data.message, username: data.username }]);
        };

        socket.onerror = function(e) {
            console.error('WebSocket error:', e);
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly:', e);
        };

        return () => {
            socket.close();
        };
    }, [interestId]);

    const fetchMessages = () => {
        axios.get(`http://localhost:8000/myapp/api/messages/${interestId}/`, { withCredentials: true })
            .then(response => setMessages(response.data))
            .catch(error => console.error('Error fetching messages:', error));
    };

    const sendMessage = (e) => {
        e.preventDefault();
        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            console.log('Sending message:', newMessage);
            chatSocket.send(JSON.stringify({
                'message': newMessage
            }));
            setNewMessage('');
        } else {
            console.error('WebSocket is not open. Ready state:', chatSocket?.readyState);
        }
    };

    return (
        <>
            <Header />
            <div className="container">
                <h1>Chat</h1>
                <div className="chat-box">
                    {messages.map((message, index) => (
                        <div key={index} className="message">
                            <strong>{message.username === user?.username ? 'You' : message.username}:</strong> {message.text}
                        </div>
                    ))}
                </div>
                <form onSubmit={sendMessage} className="chat-form">
                    <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Type your message here"
                    />
                    <button type="submit">Send</button>
                </form>
            </div>
        </>
    );
};

export default Chat;


