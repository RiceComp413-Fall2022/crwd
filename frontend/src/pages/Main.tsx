import React from 'react';
import StatusBox from '../components/StatusBox';
import Graph from '../components/Graph';
import { Container } from 'react-bootstrap';

import './Main.css';

function Main() {

  return (
    <div className="main">
      
      <Container>
        <h1 className="title">crwd</h1>
      </Container>

      <Container>
        <StatusBox/>
      </Container>

      <Container>
        <Graph/>
      </Container>

    </div>
  );
}

export default Main;
