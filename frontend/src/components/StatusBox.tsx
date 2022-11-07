import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'react-bootstrap';
import { BACKEND_URL } from '../Constants';

import './StatusBox.css'


// The expected data from the server's /getCurrentStatus endpoint
interface Status {
  msg1: string;
  msg2: string;
  perc: number;
  time: string;
  backgroundColor: string;
  textColor: string
}

function StatusBox() {

  // Store server response
  const [status, setStatus] = useState({
    msg1: 'N/A',
    msg2: 'N/A',
    perc: 0,
    time: 'N/A', 
    backgroundColor: 'transparent',
    textColor: 'white'
  });

  const [isChausOpen, setIsChausOpen] = useState(true);

  // Fetch / from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus")
      .then((response) => response.json())
      .then((status: Status) => {
        setStatus(status);
      });
  }, [])

  useEffect(() => {
    fetch(BACKEND_URL + "/isChausOpen")
      .then((response) => response.text())
      .then((chausOpen) => {
        setIsChausOpen(chausOpen !== 'false') // Assume open if any value other than false is returned
    });
  }, [])

  return (
    <Row>
      <Col sm={true}>
        <Card className={"textBox"} style={{backgroundColor: status.backgroundColor, color: status.textColor}}>
          <Card.Body>
            <h5><b>{status.msg1}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
      <Col sm={true}>
        <Card className={"textBox"} style={{backgroundColor: status.backgroundColor, color: status.textColor}}>
          <Card.Body>
            <h5><b>{status.msg2}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
    </Row>
  );
}

export default StatusBox;