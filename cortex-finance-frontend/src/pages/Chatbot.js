// src/pages/Chatbot.js

import React, { useState } from "react";
import "../App.css";

function Chatbot() {

  const [messages, setMessages] = useState([
    {
      text: "Hello 👋 How can I help with your finances?",
      sender: "bot"
    }
  ]);

  const [input, setInput] = useState("");

  // Send Message

  const sendMessage = () => {

    if (input.trim() === "") {
      return;
    }

    // User Message

    const userMessage = {
      text: input,
      sender: "user"
    };

    // Fake AI Reply

    const botMessage = {
      text: "AI is analyzing your financial question...",
      sender: "bot"
    };

    setMessages([
      ...messages,
      userMessage,
      botMessage
    ]);

    setInput("");
  };

  return (

    <div className="chatbot-container">

      {/* Chat Card */}

      <div className="chatbot-card">

        {/* Header */}

        <div className="chatbot-header">

          <h1>
            AI Finance Assistant 🤖
          </h1>

        </div>

        {/* Chat Messages */}

        <div className="chat-messages">

          {
            messages.map((msg, index) => (

              <div
                key={index}
                className={
                  msg.sender === "user"
                    ? "user-message"
                    : "bot-message"
                }
              >
                {msg.text}
              </div>

            ))
          }

        </div>

        {/* Input Area */}

        <div className="chat-input-area">

          <input
            type="text"
            placeholder="Ask financial questions..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="chat-input"
          />

          <button
            onClick={sendMessage}
            className="send-button"
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default Chatbot;
