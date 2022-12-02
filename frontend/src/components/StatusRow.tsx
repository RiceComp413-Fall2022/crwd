import React from 'react';
import { Col, Row } from 'react-bootstrap';
import LocationStatusBox from './StatusBox';


// A row of status boxes for each location
function StatusRow() {

  return (
    <Row>
      <Col sm={true}>
        <LocationStatusBox displayName='Chaus' locationName='chaus'/>
      </Col>

      <Col sm={true}>
        <LocationStatusBox displayName="Brochstein" locationName='brochstein'/>
      </Col>

      <Col sm={true}>
        <LocationStatusBox displayName="Audrey's" locationName='audreys'/>
      </Col>
    </Row>
  );
}

export default StatusRow;