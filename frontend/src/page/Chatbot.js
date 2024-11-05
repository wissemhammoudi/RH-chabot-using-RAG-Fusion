import React, { useState, useRef, useEffect } from "react";
import Avatar from "../component/Avatar";
import Loading from "../component/Loading";
import Error from "../component/Error";
import "./Chatbot.css"; // Ensure you have appropriate styles

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [subquestions, setSubquestions] = useState("");
  const [isEditing, setIsEditing] = useState(false); // To toggle edit mode
  const [isLocked, setIsLocked] = useState(false); // To toggle lock state
  const [resumes, setResumes] = useState([]);
  const [history, setHistory] = useState([]); // State to store history
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === "") return;
  
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    setLoading(true);
  
    // Determine the prompt_cls value based on whether history is empty
    const promptClsValue = history.length === 0 ? "retrieve_applicant_jd" : "your_alternate_prompt_cls_value";
  
    try {
      const response = await fetch("http://127.0.0.1:8000/generate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: input,
          docs: resumes,
          subquestions: subquestions.split("\n"),
          history: history,
          prompt_cls: promptClsValue,
        }),
      });
  
      if (!response.ok) throw new Error("Failed to fetch bot response");
  
      const data = await response.json();
      const botMessage = { sender: "bot", text: data.message };
  
      setMessages([...messages, { sender: "user", text: input }, botMessage]);
  
      // Add to history
      setHistory([...history, { question: input, answer: data.message }]);
  
    } catch (err) {
      setError("An error occurred while fetching the bot response.");
    } finally {
      setLoading(false);
    }
  };
  
  const handleJobDescriptionSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/generate_subquestions/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ description: jobDescription }),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch sub-questions");
      }
      const data = await response.json();
      setSubquestions(data.subquestions.join("\n")); // Join sub-questions with newline
      setIsEditing(true); // Set editing mode
      setIsLocked(false); // Ensure it's not locked initially
    } catch (err) {
      setError(err.message || "An error occurred while fetching sub-questions");
    }
  };

  const handleEditChange = (e) => {
    if (!isLocked) {
      setSubquestions(e.target.value); // Update sub-questions as the user types
    }
  };

  const handleEditSubmit = () => {
    setMessages([...messages, { sender: "user", text: subquestions }]);
    setIsEditing(false); // Exit editing mode
  };

  const handleLockToggle = () => {
    setIsLocked(!isLocked); // Toggle lock state
  };

  const handleRetrieveResumes = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/retrieve_resumes/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ subquestions: subquestions.split("\n") }), // Convert text area content to array
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error("Failed to retrieve resumes: " + errorText);
      }
      const data = await response.json();
      setResumes(data.resumes); // Store retrieved resumes
    } catch (err) {
      setError(err.message || "An error occurred while retrieving resumes");
    }
  };

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
        <button onClick={handleJobDescriptionSubmit}>Get Sub-Questions</button>
        {isEditing && (
          <div className="subquestions">
            <h3>Edit Sub-Questions:</h3>
            <textarea
              aria-label="Edit sub-questions"
              value={subquestions}
              onChange={handleEditChange}
              placeholder="Edit the sub-questions here..."
              disabled={isLocked} // Disable editing when locked
            />
            <button onClick={handleLockToggle}>
              {isLocked ? "Unlock" : "Lock"}
            </button>
            <button onClick={handleRetrieveResumes}>
              Retrieve Resumes
            </button>
          </div>
        )}
        {resumes.length > 0 && (
          <div className="retrieved-resumes">
            <h3>Retrieved Resumes:</h3>
            <ul>
              {resumes.map((resume, index) => (
                <li key={index}>{resume}</li> // Adjust this to match the structure of your resumes
              ))}
            </ul>
          </div>
        )}
      </aside>
      <main className="chatbot-main">
        <div className="chatbot-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <Avatar
                bg={msg.sender === "user" ? "#5437DB" : "#11a27f"}
                className={`avatar ${msg.sender}-avatar`}
              />
              <div className="message-text">{msg.text}</div>
            </div>
          ))}
          {loading && <Loading />}
          {error && <Error err={error} />}
          <div ref={chatEndRef} />
        </div>
        <form className="chatbot-input" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button type="submit">Send</button>
        </form>
 
      </main>
    </div>
  );
};

export default Chatbot;
