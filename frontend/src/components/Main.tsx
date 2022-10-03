import React, { useEffect, useState } from 'react';
import '../App.css';
import {
  Link
} from "react-router-dom";

function Main() {

  // Store server response
  const [crowdResponse, setCrowdResponse] = useState("N/A");

  // Fetch / from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/getCurrentCrowd")
    .then((response) => response.text())
    .then((responseText) => {
      setCrowdResponse(responseText);
    });
  }, [])

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
        <p>Response from server (127.0.0.1:5000/getCurrentCrowd):</p>
        <pre id="GFG_DOWN" style={{"color":"Red", "fontSize":"16px"}}>
          {crowdResponse}
        </pre>
    </div>
  );
}

export default Main;
