import React, { useEffect, useState } from 'react';
import StatusBox from '../components/StatusBox';
import Graph from '../components/Graph';
import { Row } from 'react-bootstrap';

import './Main.css';

function Main() {

  return (
    <div className="main">
      
      <Row>
        <h1 className="title">crwd.io</h1>
      </Row>

      <Row>
        <StatusBox/>
      </Row>

      <Row>
        <Graph/>
      </Row>

    </div>
  );
}

export default Main;
