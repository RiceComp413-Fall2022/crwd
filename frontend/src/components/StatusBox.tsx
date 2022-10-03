import React, { useEffect, useState } from 'react';
import '../App.css';
import Alert from 'react-bootstrap/Alert';

function StatusBox() {

  // Store server response
  const [crowdResponse, setCrowdResponse] = useState("N/A");

  // Fetch / from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/getCurrentCrowd")
      .then((response) => response.text())
      .then((responseText) => {
        setCrowdResponse(responseText);
      });
  }, [])

  return (
    <Alert  variant={'success'}>
    {crowdResponse}
  </Alert>
  );
}

export default StatusBox;
