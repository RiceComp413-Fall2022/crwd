import React, { useEffect, useState } from 'react';
import { Button, Col, Row, Dropdown, Card } from 'react-bootstrap';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';

import './Graph.css'
import { BACKEND_URL } from '../Constants';

function Graph() {
  // Store server response
  const [historicalData, setHistoricalData] = useState({});
  const [predictedData, setPredictedData] = useState({});
  const [displayDate, setDisplayDate] = useState("");
  // Save the offset of the day to fetch (e.g. 0: today, -1: yesterday, +1: tomorrow)
  const [selectedOffsetDays, setSelectedOffsetDays] = useState(0);
  const [shouldAnimateChart, setShouldAnimateChart] = useState(true);
  const [selectedLocation, setSelectedLocation] = useState('chaus')
  const [prettyLocation, setPrettyLocation] = useState('Chaus')

  const SERVER_TIME_FORMAT = 'MM/dd/yyyy HH:mm';

  // Fetch /dailyData from server
  useEffect(() => {
    fetch(`${BACKEND_URL}/dailyData/${selectedLocation}/${selectedOffsetDays}`)
    .then((response) => response.json())
    .then((response) => {
      setHistoricalData(response.historical);
      setDisplayDate(response.msg);
      setPredictedData(response.predicted);
    });
  }, [selectedOffsetDays, selectedLocation])

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
  );

  const chartOptions = {
    responsive: true,
    borderColor: 'white',
    backgroundColor: 'white',
    maintainAspectRatio: false,
    height: '100%',
    
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      xAxis: {
        grid: {
          display: false
        },
        // As const for type-checking
        type: 'time' as const,
        time: {
          parser: SERVER_TIME_FORMAT,
          unit: 'hour' as const
        }
      },
      yAxis: {
        // Go from -1 to 101 to avoid cutting off the boundaries
        min: -1,
        max: 101,
        grid: {
          display: false
        },
        ticks: {
          // min: 0,
          // stepSize: 101,
          callback: function(label: string | number) {
              switch (label) {
                  case -1:
                      return 'Empty';
                  case 101:
                      return 'Full';
              }
          }
        }
      }
    },
    elements: {
      point:{
        radius: 0 // no dots
      },
      line: {
        tension: 0.4 // how straight (0) or curvy the line is
      }
    },
    // Turn animation on/off
    animation: (shouldAnimateChart ? {} : { duration: 0 })
  };

  const data = {
    /*labels,*/
    datasets: [
      {
        label: 'chausCrowd',
        data: historicalData,
        // data: {"30/09/2022 08:48": 40.19607843137255, "30/09/2022 08:06": 49.01960784313725, "30/09/2022 08:49": 40.19607843137255, "30/09/2022 08:05": 49.01960784313725},
        borderColor: '#322620',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'chausCrowdPredicted',
        data: predictedData,
        borderColor: '#322620',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderDash: [10,5]
      },
    ],
  };

  // Check wether there is data to show (e.g. a day when the location never opens will have no data)
  const shouldShowGraph: boolean = Object.keys(historicalData).length > 0 || Object.keys(predictedData).length > 0

  return (
    <>

    <Row className="pb-3">
      {/* Arrows and Title ( < Title > ) */}
      <Col sm={8}>
        <Row>   
        {/* Left Arrow: "<" */}
          <Col xs={2} className="d-flex align-items-center justify-content-start">
            <Button size="lg" variant="light" onClick={() => {
              setSelectedOffsetDays(selectedOffsetDays - 1);
              // Don't animate after clicking button
              setShouldAnimateChart(false)}}
            >
              &lt;
            </Button>
          </Col>

          {/* Date */}
          <Col xs={8} className="d-flex align-items-center justify-content-center">
            <div className="chartTitle">
              {displayDate}
            </div>
          </Col>

          {/* Right Arrow: ">" */}
          <Col xs={2} className="d-flex align-items-center justify-content-end">
            <Button size="lg" variant="light" onClick={() => {
              setSelectedOffsetDays(selectedOffsetDays + 1);
              // Don't animate after clicking button
              setShouldAnimateChart(false)}}
            >
              &gt;
            </Button>
          </Col>
        </Row>
        {/* Spacing between rows on mobile */}
        <div className="d-block d-sm-none py-1"></div>
      </Col>

      {/* Dropdown to choose which cafe to display on the graph */}
      <Col sm={4} className="d-flex align-items-center justify-content-end">
        
        <Dropdown className="w-100">
          {/* <Dropdown.Toggle variant="success" id="dropdown-basic"> */}
          <Dropdown.Toggle className="w-100" size="lg" variant="light" style={{color: 'pink'}} id="dropdown-basic">
            {prettyLocation}
          </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Item onClick={() => {setSelectedLocation('chaus'); setPrettyLocation('Chaus');}}>Chaus</Dropdown.Item>
            <Dropdown.Item onClick={() => {setSelectedLocation('brochstein'); setPrettyLocation('Brochstein');}}>Brochstein</Dropdown.Item>
            <Dropdown.Item onClick={() => {setSelectedLocation('audreys'); setPrettyLocation('Audrey\'s');}}>Audrey's</Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </Col>
    </Row>

    {/* Graph (or "No data!") */}
    {shouldShowGraph ?
      // Graph
      <Line className="graph" options={chartOptions} data={data} />
      :
      // No data!
      <Card className={"noDataTextBox"}>
        <Card.Body className={"d-flex align-items-center justify-content-center"}>
            <h5 className="noDataText">No data!</h5>
        </Card.Body>
      </Card>
    }
  </>
  );
}

export default Graph;