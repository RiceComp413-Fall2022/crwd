import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

import './Graph.css'
import { BACKEND_URL } from '../Constants';

function Graph() {
  // Store server response
  const [chausData, setChausData] = useState({});

  // Fetch /getData from server
  useEffect(() => {
    fetch(BACKEND_URL + "/getAllData")
    .then((response) => response.json())
    .then((response) => {
      setChausData(response);
    });
  }, [])

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
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
        ticks: {
          autoSkip: true,
          maxTicksLimit: 8
        },
        grid: {
          display: false
        }
      },
      yAxis: {
        min: 0,
        max: 100,
        grid: {
          display: false
        },
        ticks: {
          min: 0,
          max: 100,
          stepSize: 100,
          suggestedMin: 0,
          suggestedMax: 100,
          callback: function(label: string | number) {
              switch (label) {
                  case 0:
                      return 'Empty';
                  case 100:
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
  };

  /*const labels = ['8:00', '9:00', '10:00'];*/

  const data = {
    /*labels,*/
    datasets: [
      {
        label: 'chausCrowd',
        data: chausData,
        // data: {"30/09/2022 08:48": 40.19607843137255, "30/09/2022 08:06": 49.01960784313725, "30/09/2022 08:49": 40.19607843137255, "30/09/2022 08:05": 49.01960784313725},
        borderColor: '#E07A5F',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  return (
    <Line className="graph" options={chartOptions} data={data} />
  );
}

export default Graph;