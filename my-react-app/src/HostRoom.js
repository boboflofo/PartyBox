import React from 'react';

function HostRoom({ onHost }) {
  const handleHost = () => {
    onHost();
  };

  return (
    <div>
      <h2>Host Room</h2>
      <button onClick={handleHost}>Host</button>
    </div>
  );
}

export default HostRoom;