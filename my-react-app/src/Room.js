import React from 'react';

function Room({ roomId, playerName, players }) {
  return (
    <div>
      <h2>Room ID: {roomId}</h2>
      <p>Welcome, {playerName}!</p>
      <p>Share this ID with others to join the room.</p>
      <h3>Players:</h3>
      <ul>
        {players.map((player, index) => (
          <li key={index}>{player}</li>
        ))}
      </ul>
    </div>
  );
}

export default Room;