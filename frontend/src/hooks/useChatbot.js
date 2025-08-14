import { useState, useRef, useEffect } from "react";
import apiService from "../services/apiService";

export const useChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [subquestions, setSubquestions] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isLocked, setIsLocked] = useState(false);
  const [resumes, setResumes] = useState([]);
  const [history, setHistory] = useState([]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const clearError = () => setError(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === "" || loading) return;

    const userMessage = { sender: "user", text: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    const promptClsValue = history.length === 0 ? "retrieve_applicant_jd" : "your_alternate_prompt_cls_value";

    try {
      const data = await apiService.generateResponse({
        question: input,
        docs: resumes,
        subquestions: subquestions.split("\n"),
        history: history,
        prompt_cls: promptClsValue,
      });

      const botMessage = {
        sender: "bot",
        text: data.message,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      setHistory(prev => [...prev, { question: input, answer: data.message }]);

    } catch (err) {
      setError(err.message || "An error occurred while fetching the bot response.");
    } finally {
      setLoading(false);
    }
  };

  const handleJobDescriptionSubmit = async () => {
    if (!jobDescription.trim()) {
      setError("Please enter a job description first.");
      return;
    }

    setError(null);
    try {
      const data = await apiService.generateSubquestions(jobDescription);
      setSubquestions(data.subquestions.join("\n"));
      setIsEditing(true);
      setIsLocked(false);
    } catch (err) {
      setError(err.message || "An error occurred while fetching sub-questions");
    }
  };

  const handleEditChange = (e) => {
    if (!isLocked) {
      setSubquestions(e.target.value);
    }
  };

  const handleEditSubmit = () => {
    if (subquestions.trim()) {
      const userMessage = {
        sender: "user",
        text: `Sub-questions: ${subquestions}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, userMessage]);
      setIsEditing(false);
    }
  };

  const handleLockToggle = () => {
    setIsLocked(!isLocked);
  };

  const handleRetrieveResumes = async () => {
    if (!subquestions.trim()) {
      setError("Please generate sub-questions first.");
      return;
    }

    setError(null);
    try {
      const data = await apiService.retrieveResumes(subquestions.split("\n"));
      setResumes(data.resumes);
    } catch (err) {
      setError(err.message || "An error occurred while retrieving resumes");
    }
  };

  const clearChat = () => {
    setMessages([]);
    setHistory([]);
    setResumes([]);
    setError(null);
  };

  return {
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
  };
};
