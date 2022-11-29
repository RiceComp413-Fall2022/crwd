import React, { ReactElement, useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import { BACKEND_URL } from '../Constants';

import './StatusBox.css'


// The expected data from the server's /getCurrentStatus/<location> endpoint
interface LocationStatus {
  msg: string;
  updateMsg: string;
  backgroundColor: string;
  textColor: string
}

// The props for the StatusBox component
interface StatusBoxProps {
  // The name to display with the box
  displayName: string,
  // The name of the location to fetch on the server (/getCurrentStatus/<locationName>)
  locationName: string
}

// A component that shows the status (% full / closed) for a single location 
function LocationStatusBox(props: StatusBoxProps): ReactElement {

  const defaultState = {
    msg: 'N/A',
    updateMsg: 'N/A',
    backgroundColor: 'white',
    textColor: 'black'
  };

  // Store the status (received from server) for a single location
  const [locationStatus, setLocationStatus] = useState(defaultState);

  // Fetch /getCurrentStatus/<location> from server
  useEffect(() => {
    fetch(BACKEND_URL + "/currentStatus/" + props.locationName)
      .then((response) => response.json())
      .then((status: LocationStatus) => {
        setLocationStatus(status);
      });
  }, [props.locationName])

  return (
    <Card className={"textBox"} style={{backgroundColor: locationStatus.backgroundColor, color: locationStatus.textColor}}>
      <Card.Body>
        <div className="desktopOnly">
          <h5><b>{props.displayName}</b></h5>
          <h5><b>{locationStatus.msg}</b></h5>
        </div>
        <div className="mobileOnly">
          <h5><b>{props.displayName} {locationStatus.msg}</b></h5>
        </div>
      </Card.Body>
    </Card>
  );
}

export default LocationStatusBox;