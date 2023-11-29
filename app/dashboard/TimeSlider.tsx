import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

function valuetext(value: number) {
  return `${value}00 hr`;
}

export default function TimeSlider({setTime}) {

  const handleChange = (newValue) => {
    setTime(value);
  };

  return (
    <Box sx={{ width: 300 }}>
      <Slider
        aria-label="Temperature"
        defaultValue={30}
        getAriaValueText={valuetext}
        valueLabelDisplay="auto"
        onChange={handleChange}
        step={1}
        marks
        min={0}
        max={24}
      />
    </Box>
  );
}