import React, { useEffect, useState } from 'react';
import './App.css';

function App() {

  // Store server response
  const [serverResponse, setServerResponse] = useState("N/A");

  // Fetch from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/")
    .then((response) => response.text())
    .then((responseText) => {
      setServerResponse(responseText);
    });
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Welcome to crwd.io
        </h1>

        <p>Check out the project on <a href="https://github.com/RiceComp413-Fall2022/crwd">GitHub</a>!</p>
        
        <p>Response from server (127.0.0.1:500):</p>
        <p>{serverResponse}</p>
      </header>
    </div>
  );
}

export default App;
