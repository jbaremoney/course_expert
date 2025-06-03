//Run this from the frontend folder (../AdviseLLM\frontend\) using the following command
//    npm start

import { useState } from "react";
import './App.css';

function App() {
  const [prompt, setPrompt] = useState("");         // The current input value
  const [responses, setResponses] = useState([]);  // Array to hold responses
  const [loading, setLoading] = useState(false);
  const [defaultMessageVisible, setDefaultMessageVisible] = useState(true);
  
  const handleSubmit = async () => {
    setDefaultMessageVisible(false); // hide default message
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) {
        console.error("Failed to fetch:", res);
        return;
      }

      const data = await res.json();
      setResponses((prevResponses) => [...prevResponses, data]);  // Add new response
      simulateTyping(data);
      setPrompt(""); // Clear the input box after submitting
    } catch (error) {
      console.error("Error in handleSubmit:", error);
    }
    finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResponses([]);  // Clear all responses
    setDefaultMessageVisible(true); // show again
  };

  const simulateTyping = (fullText) => {
    let currentText = "";
    let i = 0;
  
    const interval = setInterval(() => {
      if (i >= fullText.length) {
        clearInterval(interval);
        return;
      }
  
      currentText += fullText[i];
      setResponses((prev) => [...prev.slice(0, -1), currentText]); // Update the last response
      i++;
    }, 20); // Speed: 20ms per character (adjust if needed)
  };

  return (
    <div style={{ textAlign: "center", position: "relative"}}>
      
      <header class = 'accessible' style={{ backgroundColor: "#009A44", height: "150px", display: "flex", alignItems: "center", justifyContent: "center", position: "relative" }}>
        {/* Image aligned left */}
        <img
          src="/newHawk-03-01.png"
          alt="Logo"
          style={{
            height: "120px",
            position: "absolute",
            left: "450px"
          }}
        />

        {/* Centered text */}
        <h1 style={{ fontFamily: "Trade Gothic", color: "white", margin: 0 }}>
          Academic Advising Help
        </h1>
      </header>
      <br></br>

      {/* Top row: input + loader + buttons */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px", marginBottom: "1rem" }}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt"
          style={{
            width: "400px",
            padding: "10px",
            fontSize: "16px",
            fontFamily: "Arial"
          }}
        />

        {/* Loader container (always takes space) */}
        <div style={{ width: "30px", height: "30px", padding: '10px'}}>
          {loading && <div className="loader"></div>}
        </div>

        <button onClick={handleSubmit} style={{ padding: "10px", fontFamily: "Arial", fontSize: '16px' }}>
          Submit
        </button>

        <button onClick={handleClear} style={{ padding: "10px", fontFamily: "Arial", fontSize: '16px' }}>
          Clear Responses
        </button>
      </div>


      <br></br>

      {/* Container for the responses */}
      <div
        style={{
          minHeight: "50px",
          marginTop: "2rem",
          padding: "10px",
          border: "1px solid #ddd",
          borderRadius: "5px",
          width: "80%",
          margin: "0 auto",
          backgroundColor: "#f9f9f9",
        }}
      >
        {/* Display each response as a new item */}
        {defaultMessageVisible ? (
          <p style={{ fontFamily: "Arial", color: "#888" }}>
            Hi I'm KnEd. Ask me any questions that you would normally ask your advisor!
          </p>
        ) : (
          [...responses].reverse().map((response, index) => (
            <div
              key={index}
              style={{
                marginBottom: "1rem",
                padding: "8px",
                backgroundColor: "#e7f3ff",
                borderRadius: "4px",
              }}
            >
              <strong>Response {responses.length - index}:</strong>
              <p style={{ fontFamily: "Arial" }}>{response}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
