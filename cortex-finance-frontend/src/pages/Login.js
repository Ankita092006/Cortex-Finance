// src/pages/Login.js

import React from "react";
import "../index.css";

function Login() {
  return (
    <div className="auth-container">

      <div className="auth-card">

        {/* Title */}
        <h1 className="auth-title">
          Login
        </h1>

        {/* Email Input */}
        <input
          type="email"
          placeholder="Enter Email"
          className="auth-input"
        />

        {/* Password Input */}
        <input
          type="password"
          placeholder="Enter Password"
          className="auth-input"
        />

        {/* Login Button */}
        <button className="auth-button">
          Login
        </button>

        {/* Signup Link */}
        <p className="auth-text">
          Don't have an account?

          <a href="/signup" className="auth-link">
            Sign Up
          </a>
        </p>

      </div>

    </div>
  );
};

export default Login;