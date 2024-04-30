import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import JoinRoom from './JoinRoom';
import HostRoom from './HostRoom';
import Room from './Room';
import TriviaGame from './TriviaGame'; // Import the TriviaGame component

const socket = io.connect('http://localhost:5000');

function App() {
  const [roomId, setRoomId] = useState('');
  const [players, setPlayers] = useState([]);
  const [playerName, setPlayerName] = useState('');
  const [showNameInput, setShowNameInput] = useState(true);

  useEffect(() => {
    const handleRoomPlayersUpdate = (data) => {
      if (data.room_id === roomId) {
        const playerNames = Object.values(data.players);
        setPlayers(playerNames);
      }
    };
  
    socket.on('room_players_update', handleRoomPlayersUpdate);
  
    return () => {
      socket.off('room_players_update', handleRoomPlayersUpdate);
    };
  }, [roomId]);

  const handleJoinRoom = (roomId) => {
    if (playerName.trim() !== '') {
      socket.emit('join_room', { room_id: roomId, player_name: playerName });
      socket.on('room_joined', (data) => {
        setRoomId(data.room_id);
        setShowNameInput(false);
      });
      socket.on('room_not_found', () => {
        alert('Room not found. Please enter a valid room ID.');
      });
      socket.emit('get_room_players', roomId);
    } else {
      alert('Please enter your name.');
    }
  };
  
  const handleHostRoom = () => {
    if (playerName.trim() !== '') {
      socket.emit('host_room', { player_name: playerName });
      socket.on('room_created', (data) => {
        setRoomId(data.room_id);
        setShowNameInput(false);
        setPlayers([playerName]); 
      });
    } else {
      alert('Please enter your name.');
    }
  };

  const handleNameChange = (e) => {
    setPlayerName(e.target.value);
  };

  return (
    <div className="App">
      <h1>PartyBox</h1>
      {showNameInput && (
        <input
          type="text"
          value={playerName}
          onChange={handleNameChange}
          placeholder="Enter Your Name"
        />
      )}
      {roomId ? (
        <>
          <Room roomId={roomId} playerName={playerName} players={players} />
          <TriviaGame roomId={roomId} socket={socket} /> {/* Pass socket connection to TriviaGame component */}
        </>
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