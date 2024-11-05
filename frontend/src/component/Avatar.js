// Avatar.js
import React from "react";

const Avatar = ({ bg, className }) => {
  return (
    <div
      className={`avatar ${className}`}
      style={{ backgroundColor: bg }}
    >
      {/* Add avatar content here */}
    </div>
  );
};

export default Avatar;
