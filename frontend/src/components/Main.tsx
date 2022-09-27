import React from "react";
import {
  Link
} from "react-router-dom";

function Main() {
    return (
      <>
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
      </>
    );
  }

export default Main;