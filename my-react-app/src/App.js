import React, { useState, useEffect } from 'react';
import JoinRoom from './JoinRoom';
import HostRoom from './HostRoom';
import io from 'socket.io-client';

const socket = io('http://localhost:5000', {
  transports: ['websocket', 'polling'],
  withCredentials: true,
  extraHeaders: {
    'Access-Control-Allow-Origin': 'http://localhost:3000',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
    'Access-Control-Allow-Headers': 'Content-Type',
  },
});




function App() {
  const [roomId, setRoomId] = useState('');

  const handleJoinRoom = (roomId) => {
    socket.emit('join_room', { room_id: roomId });
    socket.on('room_joined', (data) => {
      setRoomId(data.room_id);
    });
    socket.on('room_not_found', () => {
      alert('Room not found. Please enter a valid room ID.');
    });
  };

  const handleHostRoom = () => {
    socket.emit('host_room');
    socket.on('room_created', (data) => {
      setRoomId(data.room_id);
    });
  };

  return (
    <div className="App">
      <h1>PartyBox</h1>
      {roomId ? (
        <div>
          <h2>Room ID: {roomId}</h2>
          <p>Share this ID with others to join the room.</p>
        </div>
      ) : (
        <div>
          <JoinRoom onJoin={handleJoinRoom} />
          <HostRoom onHost={handleHostRoom} />
        </div>
      )}
    </div>
  );
}




export default App;
