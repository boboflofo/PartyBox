import React, { useState, useEffect } from 'react';

const TriviaGame = ({ roomId, socket }) => {
  const [question, setQuestion] = useState(null);
  const [options, setOptions] = useState([]);
  const [answered, setAnswered] = useState(false);
  const [scores, setScores] = useState({});
  const [timer, setTimer] = useState(30);
  const [gameFinished, setGameFinished] = useState(false);
  const [winner, setWinner] = useState(null); 

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
    
    });
  
    socket.on('game_finished', (gameWinner) => {
      console.log('Game finished! Winner:', gameWinner);
      setGameFinished(true);
      setWinner(gameWinner); 
    });
  
    socket.on('new_question', (data) => {
      setQuestion(data.question);
      setOptions(data.options);
      setAnswered(false);
      setGameFinished(false);
      setWinner(null); 
    });
  
    socket.on('update_scores', (roomScores) => {
      setScores(roomScores);
    });
  
    socket.on('disable_answer', () => {
      setAnswered(true); 
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
    socket.emit('start_game', roomId);
  };

  return (
    <div className="trivia-game-container">
      <h2 className="game-title">Trivia Quiz</h2>
      {!question && (
        <button className="start-button" onClick={handleStartGame}>Start Trivia Game</button>
      )}
      {question && (
        <>
          <p className="timer">Time left: {timer}</p>
          <p className="question">{question}</p>
          <ul className="options-list">
            {options.map((option, index) => (
              <li
                key={index}
                onClick={() => handleAnswer(option)}
                className={`option ${answered || gameFinished ? 'disabled' : ''}`}
              >
                {option}
              </li>
            ))}
          </ul>
        </>
      )}
      <h3 className="scores-title">Scores:</h3>
      <ul className="scores-list">
        {Object.entries(scores).map(([playerName, score]) => (
          <li key={playerName} className="score">{playerName}: {score}</li>
        ))}
      </ul>
      {gameFinished && (
        <p className="winner-message">Winner: {winner}</p>
      )}
    </div>
  );
};

export default TriviaGame;