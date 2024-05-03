import React from 'react';

function HostRoom({ onHost }) {
  const handleHost = () => {
    onHost();
  };

  return (
    <div className="host-room-container">
      <h2>Host Room</h2>
      <button className="host-button" onClick={handleHost}>Host</button>
    </div>
  );
}

export default HostRoom;