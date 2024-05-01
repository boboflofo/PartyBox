import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const TriviaGame = ({ roomId, socket }) => {
  const [question, setQuestion] = useState(null);
  const [options, setOptions] = useState([]);
  const [answered, setAnswered] = useState(false);
  const [scores, setScores] = useState({});
  const [timer, setTimer] = useState(30);
  const [gameFinished, setGameFinished] = useState(false);
  const [winner, setWinner] = useState(null); // State to hold the winner

  useEffect(() => {
    socket.on('start_timer', () => {
      const startTime = Date.now();
      const interval = setInterval(() => {
        const remainingTime = Math.max(30 - Math.floor((Date.now() - startTime) / 1000), 0);
        setTimer(remainingTime);
        if (remainingTime === 0) {
          clearInterval(interval);
        }
      }, 1000);
    });
  
    socket.on('stop_timer', () => {
      // Implement logic to stop the timer if needed
    });
  
    socket.on('game_finished', (gameWinner) => {
      console.log('Game finished! Winner:', gameWinner);
      setGameFinished(true);
      setWinner(gameWinner); // Set the winner when the game finishes
    });
  
    socket.on('new_question', (data) => {
      setQuestion(data.question);
      setOptions(data.options);
      setAnswered(false);
      setGameFinished(false);
      setWinner(null); // Reset winner when new question is received
    });
  
    socket.on('update_scores', (roomScores) => {
      setScores(roomScores);
    });
  
    socket.on('disable_answer', () => {
      setAnswered(true); // Disable answering when receiving disable_answer event
    });
  
    return () => {
      socket.off('start_timer');
      socket.off('stop_timer');
      socket.off('game_finished');
      socket.off('new_question');
      socket.off('update_scores');
      socket.off('disable_answer');
    };
  }, []);

  const handleStartGame = () => {
    socket.emit('start_game', roomId);
    socket.emit('start_timer', roomId);
  };

  const handleAnswer = (option) => {
    if (!answered) {
      socket.emit('answer', { room_id: roomId, sid: socket.id, option });
      setAnswered(true);
    }
    // Always request for a new question after answering
    socket.emit('start_game', roomId);
  };

  return (
    <div>
      <h2>Trivia Quiz</h2>
      {!question && (
        <button onClick={handleStartGame}>Start Trivia Game {roomId}</button>
      )}
      {question && (
        <>
          <p>Time left: {timer}</p>
          <p>{question}</p>
          <ul>
            {options.map((option, index) => (
              <li key={index} onClick={() => handleAnswer(option)} style={{ cursor: answered || gameFinished ? 'not-allowed' : 'pointer' }}>
                {option}
              </li>
            ))}
          </ul>
        </>
      )}
      <h3>Scores:</h3>
      <ul>
        {Object.entries(scores).map(([playerName, score]) => (
          <li key={playerName}>{playerName}: {score}</li>
        ))}
      </ul>
      {gameFinished && (
        <p>Winner: {winner}</p>
      )}
    </div>
  );
};

export default TriviaGame;