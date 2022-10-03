import React, { useEffect, useState } from 'react';
import StatusBox from '../components/StatusBox';
import Graph from '../components/Graph';
import { Col, Container, Row } from 'react-bootstrap';

function Main() {

  return (
    <div className="Main">
      <div>
        <h2 style={ {textAlign:"center"} }>crwd.io</h2>
      </div>

      <Container>
        <Row>
          {/* Left half: Graph */}
          <Col>
            <Graph/>
          </Col>
          {/* Right half: Status */}
          <Col>
            <StatusBox/>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Main;
