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
            chaus is 
            <br></br>
            <h5><b>{Math.round(status.perc)}% full</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
      <Col sm={true}>
        <Card className="textBox">
          <Card.Body>
            last updated
            <br></br>
            <h5><b>{status.time}</b></h5>
            {/* <b>{status.time}</b> */}
          </Card.Body>
        </Card>
      </Col>
      
    </Row>
  );
}

export default StatusBox;
