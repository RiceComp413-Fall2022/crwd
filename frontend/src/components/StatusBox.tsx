import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import { BACKEND_URL } from '../Constants';

import './StatusBox.css'

function StatusBox() {

  // Store server response
  const [crowdResponse, setCrowdResponse] = useState("N/A");

  // Fetch / from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus")
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
