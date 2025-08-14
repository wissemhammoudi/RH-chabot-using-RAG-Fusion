import React from "react";
import "./Loading.css";

const Loading = ({ message = "Thinking..." }) => {
  return (
    <div className="loading">
      <div className="loading-content">
        <div className="spinner"></div>
        <p className="loading-text">{message}</p>
      </div>
    </div>
  );
};

export default Loading;
