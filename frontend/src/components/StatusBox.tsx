import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'react-bootstrap';
import { BACKEND_URL } from '../Constants';

import './StatusBox.css'


// The expected data from the server's /getCurrentStatus/chaus endpoint
interface ChausStatus {
  msg1: string;
  msg2: string;
  perc: number;
  time: string;
  backgroundColor: string;
  textColor: string
}

// The expected data from the server's /getCurrentStatus/brochstein endpoint
interface BrochsteinStatus {
  msg1: string;
  msg2: string;
  perc: number;
  time: string;
  backgroundColor: string;
  textColor: string
}

// The expected data from the server's /getCurrentStatus/audreys endpoint
interface AudreysStatus {
  msg1: string;
  msg2: string;
  perc: number;
  time: string;
  backgroundColor: string;
  textColor: string
}

function StatusBox() {

  // Store server response for Chaus
  const [chausStatus, setChausStatus] = useState({
    msg1: 'N/A',
    msg2: 'N/A',
    perc: 0,
    time: 'N/A', 
    backgroundColor: 'transparent',
    textColor: 'white'
  });

  // Store server response for Brochstein
  const [brochsteinStatus, setBrochsteinStatus] = useState({
    msg1: 'N/A',
    msg2: 'N/A',
    perc: 0,
    time: 'N/A', 
    backgroundColor: 'transparent',
    textColor: 'white'
  });

  // Store server response for Audrey's
  const [audreysStatus, setAudreysStatus] = useState({
    msg1: 'N/A',
    msg2: 'N/A',
    perc: 0,
    time: 'N/A', 
    backgroundColor: 'transparent',
    textColor: 'white'
  });


  // Fetch /getCurrentStatus/chaus from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus/chaus")
      .then((response) => response.json())
      .then((chausStatus: ChausStatus) => {
        setChausStatus(chausStatus);
      });
  }, [])

  // Fetch /getCurrentStatus/brochstein from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus/brochstein")
      .then((response) => response.json())
      .then((brochsteinStatus: BrochsteinStatus) => {
        setBrochsteinStatus(brochsteinStatus);
      });
  }, [])

  // Fetch /getCurrentStatus/audreys from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus/audreys")
      .then((response) => response.json())
      .then((audreysStatus: AudreysStatus) => {
        setAudreysStatus(audreysStatus);
      });
  }, [])


  return (
    <Row>
      <Col md={true}>
        <Card className={"textBox"} style={{backgroundColor: chausStatus.backgroundColor, color: chausStatus.textColor}}>
          <Card.Body>
            <h5><b>{chausStatus.msg1}</b></h5>
            <h5><b>{chausStatus.msg2}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
      <Col md={true}>
        <Card className={"textBox"} style={{backgroundColor: brochsteinStatus.backgroundColor, color: brochsteinStatus.textColor}}>
          <Card.Body>
            <h5><b>{brochsteinStatus.msg1}</b></h5>
            <h5><b>{brochsteinStatus.msg2}</b></h5>
          </Card.Body>
        </Card>
      </Col>

      <Col md={true}>
        <Card className={"textBox"} style={{backgroundColor: audreysStatus.backgroundColor, color: audreysStatus.textColor}}>
          <Card.Body>
            <h5><b>{audreysStatus.msg1}</b></h5>
            <h5><b>{audreysStatus.msg2}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
    </Row>
  );
}

export default StatusBox;