import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io.connect('http://localhost:5000');

const TriviaGame = ({ roomId, socket }) => {
  const [question, setQuestion] = useState(null);
  const [options, setOptions] = useState([]);
  const [answered, setAnswered] = useState(false);
  const [scores, setScores] = useState({});

  useEffect(() => {
    socket.on('new_question', (data) => {
      console.log(data.question)
      setQuestion(data.question);
      setOptions(data.options);
      setAnswered(false);
      console.log("hi")
    });

    socket.on('update_scores', (roomScores) => {
      setScores(roomScores);
    });

    return () => {
      socket.off('new_question');
      socket.off('update_scores');
    };
  }, []);

  const handleStartGame = () => {
    socket.emit('start_game', roomId);
  };

  const handleAnswer = (option) => {
    if (!answered) {
      socket.emit('answer', { room_id: roomId, sid: socket.id, option });
      setAnswered(true);
    }
  };

  return (
    <div>
      <h2>Trivia Quiz</h2>
      {!question && (
        <button onClick={() => handleStartGame()}>Start Trivia Game {roomId}</button>
      )}
      {question && (
        <>
          <p>{question}</p>
          <ul>
            {options.map((option, index) => (
              <li key={index} onClick={() => handleAnswer(option)}>
                {option}
              </li>
            ))}
          </ul>
        </>
      )}
      <h3>Scores:</h3>
      <ul>
  {Object.entries(scores).map(([playerName, score]) => (
    <li key={playerName}>{playerName}: {score}</li>  // Display playerName instead of sid
  ))}
</ul>
    </div>
  );
};

export default TriviaGame