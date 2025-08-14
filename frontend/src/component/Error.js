import React from "react";
import "./Error.css";

const Error = ({ err, onRetry }) => {
  return (
    <div className="error">
      <div className="error-content">
        <div className="error-icon">⚠️</div>
        <p className="error-message">{err || "An error occurred. Please try again."}</p>
        {onRetry && (
          <button className="error-retry-btn" onClick={onRetry}>
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default Error;
