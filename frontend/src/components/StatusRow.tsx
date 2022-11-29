import React from 'react';
import { Col, Row } from 'react-bootstrap';
import LocationStatusBox from './StatusBox';


// A row of status boxes for each location
function StatusRow() {

  return (
    <Row>
      <Col md={true}>
        <LocationStatusBox displayName='Chaus' locationName='chaus'/>
      </Col>

      <Col md={true}>
        <LocationStatusBox displayName="Brochstein" locationName='brochstein'/>
      </Col>

      <Col md={true}>
        <LocationStatusBox displayName="Audrey's" locationName='audreys'/>
      </Col>
    </Row>
  );
}

export default StatusRow;