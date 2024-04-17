import React, { useState } from 'react';
import io from 'socket.io-client';

const JoinRoom = () => {
    const [username, setUsername] = useState('');
    const [roomCode, setRoomCode] = useState('');

    const joinRoom = () => {
        const socket = io(); // Connect to the websocket server

        socket.emit('join_room', { username, room_code: roomCode });
        
        socket.on('user_joined', (data) => {
            alert(`${data.username} has joined the room.`);
        });
    };

    return (
        <div>
            <h1>Join a Room</h1>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter your username" />
            <input type="text" value={roomCode} onChange={(e) => setRoomCode(e.target.value)} placeholder="Enter room code" />
            <button onClick={joinRoom}>Join Room</button>
        </div>
    );
};

export default JoinRoom;