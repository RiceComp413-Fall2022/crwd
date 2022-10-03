import React, { useEffect, useState } from 'react';
import '../App.css';
import Alert from 'react-bootstrap/Alert';

function StatusBox() {

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
    <Alert  variant={'success'}>
    {crowdResponse}
  </Alert>
  );
}

export default StatusBox;


// import React, { useEffect, useState } from 'react';
// import '../App.css';
// import {
//   Link
// } from "react-router-dom";

// function Main() {

//   // Store server response
//   const [crowdResponse, setCrowdResponse] = useState("N/A");

//   // Fetch / from server
//   useEffect(() => {
//     fetch("http://127.0.0.1:5000/getCurrentCrowd")
//     .then((response) => response.text())
//     .then((responseText) => {
//       setCrowdResponse(responseText);
//     });
//   }, [])

//   return (
//     <div className="Main">
//         <p>Response from server (127.0.0.1:5000/getCurrentCrowd):</p>
//         <pre id="GFG_DOWN" style={{"color":"Red", "fontSize":"16px"}}>
//           {crowdResponse}
//         </pre>
//     </div>
//   );
// }

// export default Main;
