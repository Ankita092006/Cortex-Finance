// src/pages/Dashboard.js

import React from "react";
import { Link } from "react-router-dom";

import Navbar from "../components/Navbar";
import Welcome from "../components/Welcome";
import SummaryCard from "../components/SummaryCard";
import TransactionTable from "../components/TransactionTable";
import Charts from "../components/Charts";

import "../App.css";

function Dashboard() {

  return (

    <div className="dashboard-container">

      {/* Navbar */}

      <Navbar />

      {/* Welcome Section */}

      <Welcome />

      {/* Summary Cards */}

      <div className="card-grid">

        <SummaryCard
          title="Total Income"
          amount="₹50,000"
        />

        <SummaryCard
          title="Total Expense"
          amount="₹35,000"
        />

        <SummaryCard
          title="Savings"
          amount="₹15,000"
        />

        <SummaryCard
          title="Financial Score"
          amount="85%"
        />

      </div>

      {/* Charts */}

      <Charts />

      {/* Transactions */}

      <TransactionTable />

      {/* AI Insights */}

      <div className="insight-section">

        <h2>AI Insights 🤖</h2>

        <div className="insight-card">
          You spent 20% more on food this month.
        </div>

        <div className="insight-card">
          Your highest expense category is Shopping.
        </div>

        <div className="insight-card">
          You can save ₹5,000 by reducing weekend spending.
        </div>

        {/* Open Chatbot Button */}

        <Link to="/chatbot">

          <button className="chatbot-open-btn">
            Open AI Assistant 🤖
          </button>

        </Link>

      </div>

    </div>
  );
}

export default Dashboard;