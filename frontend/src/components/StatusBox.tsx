import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'react-bootstrap';
import { BACKEND_URL } from '../Constants';

import './StatusBox.css'


// The expected data from the server's /getCurrentStatus/location endpoint
interface LocationStatus {
  msg: string;
  updateMsg: string;
  backgroundColor: string;
  textColor: string
}

function StatusBox() {

  const defaultState = {
    msg: 'N/A',
    updateMsg: 'N/A',
    backgroundColor: 'white',
    textColor: 'black'
  };

  // Store server response for Chaus
  const [chausStatus, setChausStatus] = useState(defaultState);

  // Store server response for Brochstein
  const [brochsteinStatus, setBrochsteinStatus] = useState(defaultState);

  // Store server response for Audrey's
  const [audreysStatus, setAudreysStatus] = useState(defaultState);


  // Fetch /getCurrentStatus/chaus from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus/chaus")
      .then((response) => response.json())
      .then((chausStatus: LocationStatus) => {
        setChausStatus(chausStatus);
      });
  }, [])

  // Fetch /getCurrentStatus/brochstein from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus/brochstein")
      .then((response) => response.json())
      .then((brochsteinStatus: LocationStatus) => {
        setBrochsteinStatus(brochsteinStatus);
      });
  }, [])

  // Fetch /getCurrentStatus/audreys from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getCurrentStatus/audreys")
      .then((response) => response.json())
      .then((audreysStatus: LocationStatus) => {
        setAudreysStatus(audreysStatus);
      });
  }, [])

  console.log(chausStatus.msg);

  return (
    <Row>
      <Col md={true}>
        <Card className={"textBox"} style={{backgroundColor: chausStatus.backgroundColor, color: chausStatus.textColor}}>
          <Card.Body>
            <h5><b>Chaus</b></h5>
            <h5><b>{chausStatus.msg}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
      <Col md={true}>
        <Card className={"textBox"} style={{backgroundColor: brochsteinStatus.backgroundColor, color: brochsteinStatus.textColor}}>
          <Card.Body>
            <h5><b>Brochstein</b></h5>
            <h5><b>{brochsteinStatus.msg}</b></h5>
          </Card.Body>
        </Card>
      </Col>

      <Col md={true}>
        <Card className={"textBox"} style={{backgroundColor: audreysStatus.backgroundColor, color: audreysStatus.textColor}}>
          <Card.Body>
            <h5><b>Audrey's</b></h5>
            <h5><b>{audreysStatus.msg}</b></h5>
          </Card.Body>
        </Card>
      </Col>
      
    </Row>
  );
}

export default StatusBox;