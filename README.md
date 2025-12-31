# 🚀 Finoplex

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-darkgreen?style=for-the-badge&logo=mongodb)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-JS-blue?style=for-the-badge&logo=react)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-cyan?style=for-the-badge&logo=tailwindcss)
![shadcn/ui](https://img.shields.io/badge/shadcn-ui-white?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange?style=for-the-badge&logo=google)

A **full-stack AI-powered personal finance operating system** that tracks expenses, generates financial intelligence, predicts future behavior, and explains insights using generative AI.

Built with **FastAPI, MongoDB, Next.js, Tailwind, shadcn/ui, and Google Gemini**.

---

## ✨ Key Capabilities

- Secure user authentication
- Expense tracking and management
- Financial intelligence & analytics
- Predictive financial forecasting
- AI-generated financial explanations
- Clean, production-grade UX

---

## 🧱 System Architecture — 4 Layers

### **Layer 1 — Data Layer**
Responsible for collecting and storing financial data.

**Backend**
- User authentication (register/login)
- Expense CRUD operations
- Indexed MongoDB collections

**Frontend**
- Expense input forms
- Expense listings
- Data validation & error handling

---

### **Layer 2 — Intelligence Layer**
Transforms raw data into meaningful financial metrics.

**Backend**
- Monthly summaries
- Spending breakdowns
- Fixed vs variable expense ratios
- Savings rate calculations

**Frontend**
- Analytics cards
- Trend indicators
- Financial health visuals

---

### **Layer 3 — Prediction Layer**
Forecasts future financial behavior.

**Backend**
- Next-month expense prediction
- Net balance projection
- Risk detection (overspending, savings decline)
- Confidence scoring based on data quality

**Frontend**
- Prediction dashboards
- Risk badges
- Confidence indicators

---

### **Layer 4 — AI Explanation Layer**
Converts numerical insights into **human-readable explanations**.

**Backend**
- Google Gemini integration
- Strict prompt control (no advice, no hallucinations)
- Clean, neutral financial summaries

**Frontend**
- AI explanation cards
- Typography-clean output
- Confidence-aware explanations

---

## ⚙️ Installation & Setup

### 🔧 Backend Setup

#### 1️⃣ Clone Backend Repository
```bash
git clone https://github.com/chiragRane-Projects/fintech_backend.git
cd fintech_backend

python -m venv env
source env/bin/activate   # Linux / macOS
env\Scripts\activate      # Windows

pip install -r requirements.txt

Create a .env file:
MONGODB_URL=your_mongodb_connection_string
MONGODB_DB_NAME=db_name
GEMINI_AI_API_KEY=your_gemini_api_key

Run backend server:
fastapi dev main.py --host 0.0.0.0 --port 8000

API documentation:
http://localhost:8000/docs
```

### 2️⃣ Clone frontend repository
```bash
git clone https://github.com/chiragRane-Projects/fintech_frontend.git
cd fintech_frontend

npm install

Create a .env file in frontend Repo:
NEXT_PUBLIC_API_URL=http://localhost:8000

Run server:
npm run dev

URL:
http://localhost:3000


---

## ✅ STATUS: COMPLETE
