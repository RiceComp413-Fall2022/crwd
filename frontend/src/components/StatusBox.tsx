import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'react-bootstrap';
import { BACKEND_URL } from '../Constants';

import './StatusBox.css'


// The expected data from the server's /getCurrentStatus endpoint
interface Status {
  msg: string;
  perc: number;
  time: string;
}

function StatusBox() {

  // Store server response
  const [status, setStatus] = useState({msg: 'N/A', perc: 0, time: 'N/A'});

  // Fetch / from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus")
      .then((response) => response.json())
      .then((status: Status) => {
        setStatus(status);
      });
  }, [])

  return (
    <Row>
      <Col sm={true}>
        <Card className="textBox">
          <Card.Body>
            {status.msg} <br></br> ({Math.round(status.perc)}% full)
          </Card.Body>
        </Card>
      </Col>
      
      <Col sm={true}>
        <Card className="textBox">
          <Card.Body>
            Last Updated: <br></br> {status.time}
          </Card.Body>
        </Card>
      </Col>
      
    </Row>
  );
}

export default StatusBox;
