import React, { useState, useEffect } from 'react';

const TriviaGame = ({ roomId, socket }) => {
  const [question, setQuestion] = useState(null);
  const [options, setOptions] = useState([]);
  const [answered, setAnswered] = useState(false);
  const [scores, setScores] = useState({});
  const [timer, setTimer] = useState(30);
  const [timerRunning, setTimerRunning] = useState(false);

  useEffect(() => {
    let countdownInterval;

    if (timerRunning) {
      countdownInterval = setInterval(() => {
        setTimer((prevTimer) => prevTimer - 1);
      }, 1000);
    }

    return () => clearInterval(countdownInterval);
  }, [timerRunning]);

  useEffect(() => {
    socket.on('start_timer', () => {
      setTimerRunning(true);
    });

    socket.on('stop_timer', () => {
      setTimerRunning(false);
    });

    socket.on('game_finished', (winner) => {
      console.log('Game finished! Winner:', winner);
    });

    return () => {
      socket.off('start_timer');
      socket.off('stop_timer');
      socket.off('game_finished');
    };
  }, []);

  useEffect(() => {
    socket.on('new_question', (data) => {
      setQuestion(data.question);
      setOptions(data.options);
      setAnswered(false);
    });

    socket.on('update_scores', (roomScores) => {
      setScores(roomScores);
    });

    return () => {
      socket.off('new_question');
      socket.off('update_scores');
    };
  }, [roomId]);

  const handleStartGame = () => {
    socket.emit('start_game', roomId);
    socket.emit('start_timer', roomId); // Emit start_timer event with roomId
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
        <button onClick={handleStartGame}>Start Trivia Game {roomId}</button>
      )}
      {question && (
        <>
          <p>Time left: {timer}</p>
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
          <li key={playerName}>{playerName}: {score}</li>
        ))}
      </ul>
    </div>
  );
};

export default TriviaGame;