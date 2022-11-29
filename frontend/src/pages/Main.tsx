import React from 'react';
import StatusRow from '../components/StatusRow';
import Graph from '../components/Graph';

import './Main.css';

function Main() {

  return (
    <div className="main">
      
      <div className="mainRow">
        <h1 className="title">crwd.</h1>
      </div>

      <div className="mainRow">
        <StatusRow />
      </div>

      <div className="mainRow">
        <Graph/>
      </div>

    </div>
  );
}

export default Main;
