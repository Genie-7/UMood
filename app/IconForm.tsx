'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import superIcon from './super.png';
const IconForm = () => {
  const router = useRouter()
  const [selectedIcon, setSelectedIcon] = useState(null);

  const handleIconClick = (icon) => {
    setSelectedIcon(icon);
    router.push('/dashboard')
  };

  return (
    <div>
      <h2>How do you feel?</h2>
      <div>
        <Icon
          imageSrc="super.png"
          isSelected={selectedIcon === 'icon1'}
          onClick={() => handleIconClick('icon1')}
        />
        <Icon
          imageSrc="mid.png"
          isSelected={selectedIcon === 'icon2'}
          onClick={() => handleIconClick('icon2')}
        />
        <Icon
          imageSrc="sad.png"
          isSelected={selectedIcon === 'icon3'}
          onClick={() => handleIconClick('icon3')}
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
