import React from "react";
import Avatar from "../component/Avatar";
import Loading from "../component/Loading";
import Error from "../component/Error";
import { useChatbot } from "../hooks/useChatbot";
import config from "../config/config";
import "./Chatbot.css";

const Chatbot = () => {
  const {
    // State
    messages,
    input,
    loading,
    error,
    jobDescription,
    subquestions,
    isEditing,
    isLocked,
    resumes,
    chatEndRef,
    
    // Actions
    setInput,
    setJobDescription,
    handleSubmit,
    handleJobDescriptionSubmit,
    handleEditChange,
    handleEditSubmit,
    handleLockToggle,
    handleRetrieveResumes,
    clearChat,
    clearError,
  } = useChatbot();

  return (
    <div className="chatbot">
      <aside className="chatbot-side-panel">
        <h2>Job Description</h2>
        <textarea
          aria-label="Job description"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Enter job description here..."
        />
        <button
          onClick={handleJobDescriptionSubmit}
          disabled={!jobDescription.trim()}
          className="primary-btn"
        >
          Get Sub-Questions
        </button>
        
        {isEditing && (
          <div className="subquestions">
            <h3>Edit Sub-Questions:</h3>
            <textarea
              aria-label="Edit sub-questions"
              value={subquestions}
              onChange={handleEditChange}
              placeholder="Edit the sub-questions here..."
              disabled={isLocked}
            />
            <div className="button-group">
              <button onClick={handleLockToggle} className="secondary-btn">
                {isLocked ? "Unlock" : "Lock"}
              </button>
              <button onClick={handleRetrieveResumes} className="primary-btn">
                Retrieve Resumes
              </button>
            </div>
          </div>
        )}
        
        {resumes.length > 0 && (
          <div className="retrieved-resumes">
            <h3>Retrieved Resumes ({resumes.length}):</h3>
            <ul>
              {resumes.map((resume, index) => (
                <li key={index} className="resume-item">
                  <span className="resume-number">#{index + 1}</span>
                  <span className="resume-text">{resume}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        
        <div className="side-panel-actions">
          <button onClick={clearChat} className="danger-btn">
            Clear Chat
          </button>
        </div>
      </aside>
      
      <main className="chatbot-main">
        <div className="chatbot-header">
          <h1>{config.APP.NAME}</h1>
          <p>AI-powered HR assistant for resume analysis and job matching</p>
        </div>
        
        <div className="chatbot-messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h3>Welcome to {config.APP.NAME}! 👋</h3>
              <p>Start by entering a job description to generate relevant questions, then ask me anything about resumes and candidates.</p>
            </div>
          )}
          
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <Avatar
                bg={msg.sender === "user" ? "#5437DB" : "#11a27f"}
                className={`avatar ${msg.sender}-avatar`}
                name={msg.sender === "user" ? "You" : "AI Assistant"}
                size="40px"
              />
              <div className="message-content">
                <div className="message-text">{msg.text}</div>
                <div className="message-timestamp">
                  {msg.timestamp?.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {loading && <Loading message="AI is thinking..." />}
          {error && <Error err={error} onRetry={clearError} />}
          <div ref={chatEndRef} />
        </div>
        
        <form className="chatbot-input" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
            maxLength={config.CHAT.MAX_MESSAGE_LENGTH}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "Sending..." : "Send"}
          </button>
        </form>
      </main>
    </div>
  );
};

export default Chatbot;
