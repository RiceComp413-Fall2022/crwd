import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';

import './StatusBox.css'

function StatusBox() {

  // Store server response
  const [crowdResponse, setCrowdResponse] = useState("N/A");

  // Fetch / from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/getCurrentStatus")
      .then((response) => response.json())
      .then((responseText) => {
        setCrowdResponse("Last Updated: " + responseText.time + " – " + responseText.msg);
      });
  }, [])

  return (
    <Card className="textBox">
      <Card.Body>
        {crowdResponse}
      </Card.Body>
    </Card>
  );
}

export default StatusBox;
