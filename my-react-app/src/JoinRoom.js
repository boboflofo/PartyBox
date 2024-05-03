import React, { useState } from 'react';

export default function JoinRoom({ onJoin }) {
  const [roomId, setRoomId] = useState('');

  const handleChange = (e) => {
    setRoomId(e.target.value);
  };

  const handleJoin = () => {
    onJoin(roomId);
  };

  return (
    <div className="join-room-container">
      <h2>Join Room</h2>
      <input
        type="text"
        value={roomId}
        onChange={handleChange}
        placeholder="Enter Room ID"
        className="room-input"
      />
      <button className="join-button" onClick={handleJoin}>Join</button>
    </div>
  );
}