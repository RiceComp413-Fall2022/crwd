import React, { useEffect, useState } from 'react';
import StatusBox from '../components/StatusBox';
import Graph from '../components/Graph';
import { Col, Container, Row } from 'react-bootstrap';

import './Main.css';

function Main() {

  return (
    <div className="main">
      <div>
        <h1 className="title">crwd.io</h1>
      </div>

      <Row className="align-items-center">
        {/* Left half: Graph */}
        <Col className="col-9">
          <Graph/>
        </Col>
        {/* Right half: Status */}
        <Col className="col-3">
          <StatusBox/>
        </Col>
      </Row>
    </div>
  );
}

export default Main;
