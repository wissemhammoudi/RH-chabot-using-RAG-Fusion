import React from "react";
import "./Avatar.css";

const Avatar = ({ bg, className, name, size = "40px" }) => {
  const getInitials = (name) => {
    if (!name) return "?";
    return name
      .split(" ")
      .map(word => word.charAt(0))
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div
      className={`avatar ${className}`}
      style={{ 
        backgroundColor: bg, 
        width: size, 
        height: size,
        borderRadius: "50%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "white",
        fontWeight: "bold",
        fontSize: "14px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
      }}
    >
      {getInitials(name)}
    </div>
  );
};

export default Avatar;
