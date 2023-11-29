'use client'
import { Chart } from "react-google-charts";
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';
import React, { useState } from 'react';

export const options = {
  title: "How everyone else is feeling",
};
export function formatTime(hour) {
  // Ensure the hour is within the valid range [0, 23]
  const roundedHour = hour-5;

  // Get the current date and time
  const currentDate = new Date();
  
  // Set the given hour, and set minutes and seconds to 0
  currentDate.setHours(roundedHour, 0, 0, 0);

  // Format the date
  const formattedDate = currentDate.toISOString().slice(0, 19).replace("T", " ");

  return formattedDate;
}


export default function dashboard() {
  const [time, setTime] = useState(12)
  const [data, setData] = useState([["Emotion", "People per Emotion"],
    ["Amazing",0],
    ["Alright",0],
    ["Down Bad",0],
    ])

  async function getEmotionsIn(starttime) {
  console.log(starttime)
  const formattime = formatTime(time) 
  console.log(formattime)
  const st = 'http://127.0.0.1:5000/api/emotions?start_time=' + formattime;
  const res = await fetch(st, {method: 'get'})
  const load = await res.json()
  console.log(load)
  var datax = [["Emotion", "People per Emotion"],
    ["Amazing",0],
    ["Alright",0],
    ["Down Bad",0],
    ]
  for(const row of load){
    switch(row['Emotion']){
      case "sad":
        datax[3][1] += 1;
        break;
      case "mid":
        datax[2][1] += 1;
        break;
      case "happy":
        datax[1][1] += 1;
        break;
      default:
        break;
    }
  }
  console.log(datax)
  setData(datax)
  return datax;
}


  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h>See how others are doing now or at:</h>
      <Box sx={{ width: 300 }}>
      <Slider
        aria-label="Temperature"
        defaultValue={12}
        valueLabelDisplay="auto"
        onChange={(_, value) => setTime(value)}
        onChangeCommitted={getEmotionsIn}

        step={1}
        marks
        min={0}
        max={24}
      />
    </Box>
      <Chart
      chartType="PieChart"
      data={data}
      options={options}
      width={"100%"}
      height={"400px"}
    />
    </main>
  )
}
