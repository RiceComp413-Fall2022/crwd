import React, { useEffect, useState } from 'react';
import '../App.css';
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

function Graph() {
  // Store server response
  const [chausData, setChausData] = useState({});

  // Fetch /getData from server
  useEffect(() => {
    fetch("http://127.0.0.1:5000/getCrowd")
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
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Chart.js Line Chart',
      },
    },
  };

  /*const labels = ['8:00', '9:00', '10:00'];*/

  const data = {
    /*labels,*/
    datasets: [
      {
        label: 'Dataset 1',
        data: chausData,
        // data: {"30/09/2022 08:48": 40.19607843137255, "30/09/2022 08:06": 49.01960784313725, "30/09/2022 08:49": 40.19607843137255, "30/09/2022 08:05": 49.01960784313725},
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  return (
    <Line options={chartOptions} data={data} />
  );
}

export default Graph;