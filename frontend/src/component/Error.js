// Error.js
import React from "react";
import "./Error.css"; // Optional: if you want to style the error message

const Error = ({ err }) => {
  return (
    <div className="error">
      <p>{err || "An error occurred. Please try again."}</p>
    </div>
  );
};

export default Error;
