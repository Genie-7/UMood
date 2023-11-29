'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import superIcon from './super.png';

async function postEmotion(emote, user) {
  console.log(emote)
  if(user === "NULL"){
    user = 0;
  }
  var emotionid = 0
  if(emote === "happy"){
    emotionid = 1;
  }
  if(emote === "mid"){
    emotionid = 2;
  }
  if(emote === "sad"){
    emotionid = 3;
  }
  console.log(emotionid)
  var hasTouchScreen = false;

  if ("maxTouchPoints" in navigator) {
    hasTouchScreen = navigator.maxTouchPoints > 0;
  } 
  var devicet = 'desktop'
  if(hasTouchScreen){
    devicet = 'mobile';
  }else{
    devicet = 'desktop';
  }
  console.log(emotionid, emote, devicet)
  const res = await fetch('http://127.0.0.1:5000/api/emotions', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'post',
    body: JSON.stringify({ 
      emotion_Id: emotionid,
      emotion: emote,
      device: devicet,
      user_Id: 16
                        })
  })
  const data = await res.json()
  console.log('woohoo')
}

const IconForm = () => {
  const router = useRouter()
  const [selectedIcon, setSelectedIcon] = useState(null);

  const handleIconClick = (icon) => {
    postEmotion(icon, 2)
    router.push('/dashboard')
  };

  return (
    <div>
      
      <div>
        <Icon
          imageSrc="super.png"
          isSelected={selectedIcon === 'icon1'}
          onClick={() => handleIconClick('happy')}
        />
        <Icon
          imageSrc="mid.png"
          isSelected={selectedIcon === 'icon2'}
          onClick={() => handleIconClick('mid')}
        />
        <Icon
          imageSrc="sad.png"
          isSelected={selectedIcon === 'icon3'}
          onClick={() => handleIconClick('sad')}
        />
      </div>
    </div>
  );
};

const Icon = ({ imageSrc, isSelected, onClick }) => {
  return (
    <div
      style={{
        border: isSelected ? '2px solid blue' : '2px solid transparent',
        padding: '10px',
        margin: '5px',
        cursor: 'pointer',
      }}
      onClick={() => onClick()}
    >
      <img
        src={imageSrc}
        alt="icon"
        style={{ width: '50px', height: '50px' }}
      />
    </div>
  );
};

export default IconForm;
