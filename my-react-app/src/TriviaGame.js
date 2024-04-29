import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io.connect('http://localhost:5000');

const TriviaGame = () => {
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState([]);
  const [answered, setAnswered] = useState(false);

  useEffect(() => {
    socket.on('new_question', (data) => {
      setQuestion(data.question);
      setOptions(data.options);
      setAnswered(false);
    });

    return () => {
      socket.off('new_question');
    };
  }, []);

  const handleAnswer = (option) => {
    if (!answered) {
      socket.emit('answer', { option });
      setAnswered(true);
    }
  };

  return (
    <div>
      <h2>Trivia Quiz</h2>
      <p>{question}</p>
      <ul>
        {options.map((option, index) => (
          <li key={index} onClick={() => handleAnswer(option)}>
            {option}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TriviaGame;