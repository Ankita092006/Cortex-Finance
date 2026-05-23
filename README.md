# Cortex Finance AI 💰🤖

AI-Powered Bank Statement Analyzer built for Hackathon.

Cortex Finance AI analyzes Indian bank statements using AI, generates financial insights, categorizes expenses, detects recurring payments, identifies unusual transactions, and provides conversational financial intelligence using RAG (Retrieval-Augmented Generation).

---

# 🚀 Problem Statement

Participants are required to build an AI-powered application capable of analyzing a single Indian bank statement uploaded by the user. The system should automatically extract transaction data, categorize expenses and income, perform financial analysis, and generate meaningful insights and summaries.

---

# 🎯 Project Objective

The objective of this project is to simplify personal finance analysis using Artificial Intelligence and data analytics.

The system helps users:
- Understand spending habits
- Track expenses
- Detect recurring subscriptions
- Identify unusual transactions
- Receive AI-generated financial recommendations
- Interact with financial data using conversational AI

---

# ✨ Features

# 📄 File Upload
- Upload PDF Bank Statements
- Upload CSV Statements
- Secure file handling

---

# 🧾 Transaction Extraction
Automatically extracts:
- Date
- Narration
- Debit
- Credit
- Balance

Supports:
- Semi-structured Indian bank statements
- Multiple bank formats

---

# 🧠 AI Expense Categorization
Automatically categorizes transactions into:
- Food
- Shopping
- Travel
- Rent
- Salary
- EMI
- Utilities
- Entertainment
- Subscriptions
- UPI Transfers

Uses:
- Rule-based categorization
- Gemini AI fallback classification

---

# 📊 Financial Analytics
Generates:
- Total Income
- Total Expenses
- Savings
- Highest Spending Category
- Merchant-wise Analysis
- Category-wise Expense Breakdown
- Spending Trends

---

# 🔁 Recurring Payment Detection
Detects:
- Netflix subscriptions
- SIP payments
- EMIs
- Rent
- Monthly recurring expenses

---

# 🚨 Unusual Transaction Detection
AI-based anomaly detection for:
- Unusual high spending
- Suspicious transactions
- Spending spikes

Uses:
- Isolation Forest Algorithm

---

# 🤖 AI Financial Insights
Generates intelligent insights like:

- "You spent 42% more on food this month."
- "Recurring Netflix subscription detected."
- "Weekend spending is significantly higher."

---

# 💬 Conversational AI Assistant (RAG)
Ask questions like:
- "How much did I spend on food?"
- "Where am I overspending?"
- "What subscriptions do I have?"
- "What was my highest transaction?"

Uses:
- LangChain
- FAISS Vector Database
- Gemini API
- Sentence Transformers

---

# 📈 Dashboard Features
- Income vs Expense Overview
- Expense Breakdown Charts
- Spending Trend Analysis
- Top Merchant Analysis
- Financial Health Score
- AI Insight Cards

---

# 🏗️ System Architecture

```text
Frontend (React)
        ↓
FastAPI Backend
        ↓
Upload Engine
        ↓
PDF/CSV Extraction
        ↓
Data Cleaning
        ↓
Categorization Engine
        ↓
Analytics Engine
        ↓
AI Insight Generator
        ↓
RAG Pipeline
        ↓
Gemini LLM
        ↓
Frontend Dashboard + Chatbot
```

---

# 🛠️ Tech Stack

# Frontend
- React + Vite
- Tailwind CSS
- Recharts
- Framer Motion

---

# Backend
- FastAPI
- Python

---

# AI / ML
- LangChain
- Gemini API
- FAISS
- Sentence Transformers
- Scikit-learn

---

# PDF Processing
- pdfplumber
- pandas

---

# Database
- SQLite

---

# 📁 Project Structure

```bash
backend/
│
├── app/
│
│   ├── main.py
│
│   ├── routes/
│   │   ├── upload.py
│   │   ├── dashboard.py
│   │   ├── chat.py
│   │   ├── insights.py
│
│   ├── services/
│   │   ├── pdf_parser.py
│   │   ├── csv_parser.py
│   │   ├── cleaner.py
│   │   ├── category_mapper.py
│   │   ├── analytics.py
│   │   ├── recurring_detector.py
│   │   ├── anomaly_detector.py
│
│   ├── ai/
│   │   ├── gemini_classifier.py
│   │   ├── insight_generator.py
│   │   ├── summary_generator.py
│
│   ├── rag/
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── chatbot.py
│
│   ├── database/
│   │   ├── db.py
│
│   ├── models/
│   │   ├── schemas.py
│
│   ├── utils/
│
├── uploads/
├── vector_store/
├── requirements.txt
├── .gitignore
├── README.md
```

---

# ⚙️ Installation

# 1️⃣ Clone Repository

```bash
git clone <your_repo_url>
cd cortex-finance-backend
```

---

# 2️⃣ Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Run Backend Server

```bash
python -m uvicorn app.main:app --reload
```

---

# 📄 Swagger API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 📌 API Endpoints

# Upload Bank Statement

```http
POST /upload
```

Uploads:
- PDF statement
- CSV statement

---

# Dashboard Analytics

```http
GET /dashboard
```

Returns:
- income
- expenses
- savings
- category breakdown
- financial score

---

# AI Insights

```http
GET /insights
```

Returns:
- AI-generated insights
- recommendations
- spending observations

---

# Conversational AI Chatbot

```http
POST /chat
```

Example:

```json
{
  "query": "How much did I spend on food?"
}
```

---

# 🧠 RAG Architecture

```text
Uploaded Statement
        ↓
Transaction Extraction
        ↓
Categorization
        ↓
Convert to Text Chunks
        ↓
Embeddings
        ↓
FAISS Vector Store
        ↓
Retriever
        ↓
Gemini LLM
        ↓
Financial AI Response
```

---

# 🧪 Testing

# Run Backend

```bash
python -m uvicorn app.main:app --reload
```

---

# Open Swagger Docs

```text
http://127.0.0.1:8000/docs
```

Test:
- `/upload`
- `/dashboard`
- `/chat`
- `/insights`

---

# 🚀 Deployment

# Frontend
- Vercel

# Backend
- Railway / Render

# Vector Database
- Local FAISS Storage

---

# 🔮 Future Improvements

- OCR Support
- Multi-bank compatibility
- Voice-based AI assistant
- Fraud Detection AI
- Multi-statement comparison
- Personalized budgeting AI
- Real-time financial monitoring

---

# 👨‍💻 Team

Built for Hackathon 🚀

---

# 🏆 Project Goal

To build an AI-powered financial intelligence platform that transforms raw bank statements into meaningful financial insights using modern AI and RAG architecture.

---