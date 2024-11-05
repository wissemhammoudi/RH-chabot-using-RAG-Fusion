// Loading.js
import React from "react";
import "./Loading.css"; // Optional: if you want to style the spinner

const Loading = () => {
  return (
    <div className="loading">
      <div className="spinner"></div>
      <p>Loading...</p>
    </div>
  );
};

export default Loading;
