import React, { useEffect, useState } from 'react';
import './App.css';

function App() {

  // Store server response
  const [helloWorldResponse, setHelloWorldResponse] = useState("N/A");
  const [dataResponse, setDataResponse] = useState({});

  // Fetch / from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/")
    .then((response) => response.text())
    .then((responseText) => {
      setHelloWorldResponse(responseText);
    });
  }, [])

  // Fetch /getData from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/getData")
    .then((response) => response.json())
    .then((data) => {
      setDataResponse(data);
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
        <p>{helloWorldResponse}</p>

        <p>Data from server (127.0.0.1:500/getData):</p>
        <pre id="GFG_DOWN" style={{"color":"LightGreen", "fontSize":"15px", "fontWeight": "bold"}}>
          <p>{JSON.stringify(dataResponse, undefined, 4)}</p>
        </pre>
      </header>
    </div>
  );
}

export default App;
