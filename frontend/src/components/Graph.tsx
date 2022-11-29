import React, { useEffect, useState } from 'react';
import { Button, Card, Col, Row } from 'react-bootstrap';
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
  const [chausData, setChausData] = useState({});
  const [displayDate, setDisplayDate] = useState("");
  const [predictedData, setPredictedData] = useState({});
  const [currentOffset, setCurrentOffset] = useState(0);
  const [shouldAnimateChart, setShouldAnimateChart] = useState(true);

  const SERVER_TIME_FORMAT = 'MM/dd/yyyy HH:mm';

  // Fetch /getDailyData from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getDailyData/chaus/" + currentOffset)
    .then((response) => response.json())
    .then((response) => {
      setChausData(response.historical);
      setDisplayDate(response.msg);
      setPredictedData(response.predicted);
    });
  }, [currentOffset])

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
        data: chausData,
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

  return (
    <>
    <Row className="pb-4">
      {/* Left Arrow: "<" */}
      <Col xs={3} className="d-flex align-items-center justify-content-end">
        <Button size="lg" variant="light" onClick={() => {
          setCurrentOffset(currentOffset - 1);
          // Don't animate after clicking button
          setShouldAnimateChart(false)}}
        >
          &lt;
        </Button>
      </Col>

      {/* Date */}
      <Col>
        <div className="chartTitle">
          {displayDate}
        </div>
      </Col>

      {/* Right Arrow: ">" */}
      <Col xs={3} className="d-flex align-items-center justify-content-start">
        <Button size="lg" variant="light" onClick={() => {
          setCurrentOffset(currentOffset + 1);
          // Don't animate after clicking button
          setShouldAnimateChart(false)}}
        >
          &gt;
        </Button>
      </Col>
    </Row>

    {/* Graph */}
    <Line className="graph" options={chartOptions} data={data} />
  </>
  );
}

export default Graph;