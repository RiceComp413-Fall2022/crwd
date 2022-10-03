import React, { useEffect, useState } from 'react';
import '../App.css';
import {
  Link
} from "react-router-dom";
import StatusBox from './StatusBox';
import Chart from './Chart';

function Main() {

  return (
    <div className="Main">
      <div>
        <h2>Main Page</h2>
      </div>
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/status">Status</Link>
          </li>
        </ul>
      </div>
      <StatusBox/>
      <Chart/>
    </div>
  );
}

export default Main;
