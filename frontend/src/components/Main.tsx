import React, { useEffect, useState } from 'react';
import '../App.css';
import {
  Link
} from "react-router-dom";
import StatusBox from './StatusBox';
import Chart from './Chart';
import { Col, Container, Row } from 'react-bootstrap';

function Main() {

  return (
    <div className="Main">
      <div>
        <h2 style={ {textAlign:"center"} }>crwd.io</h2>
      </div>

      <Container>
        <Row>
        <Col>
          <Chart/>
        </Col>
        <Col>
          <StatusBox/>
        </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Main;
