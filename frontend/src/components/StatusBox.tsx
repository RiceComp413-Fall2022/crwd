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
  const [chausOpen, setChausOpen] = useState("N/A");

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
        setChausOpen(chausOpen)
    });
  }, [])

  const isChausOpen = chausOpen.toLowerCase() === "true";

  return (
    <Row>
      <Col sm={true}>
        <Card className={isChausOpen ? "textBox open" : "textBox closed"}>
          <Card.Body>
            <h5><b>{isChausOpen ? status.msg : "Chaus is CLOSED!"}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
      <Col sm={true}>
        <Card className={isChausOpen ? "textBox open" : "textBox closed"}>
          <Card.Body>
            <h5><b> {isChausOpen ? "Updated " + status.time : "Chaus will be open at _______"}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
    </Row>
  );
}

export default StatusBox;
