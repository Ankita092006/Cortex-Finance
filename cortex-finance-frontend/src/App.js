// src/App.js

import React from "react";

import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

/* Pages */

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Sign from "./pages/Sign";
import Upload from "./pages/Upload";
import Processing from "./pages/Processing";
import Dashboard from "./pages/Dashboard";
import Chatbot from "./pages/Chatbot";

/* CSS */

import "./App.css";

const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/dashboard/*" element={<Dashboard />} />
      </Routes>
    </AnimatePresence>
  );
};

function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* Landing Page */}
        <Route
          path="/"
          element={<Landing />}
        />

        {/* Login Page */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Signup Page */}
        <Route
          path="/signup"
          element={<Sign />}
        />

        {/* Upload Page */}
        <Route
          path="/upload"
          element={<Upload />}
        />

        {/* Processing Page */}
        <Route
          path="/processing"
          element={<Processing />}
        />

        {/* Dashboard Page */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        {/* Chatbot Page */}
        <Route
          path="/chatbot"
          element={<Chatbot />}
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;