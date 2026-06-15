# 🤖 AI Tutor Agent

An AI-powered educational assistant built using **Python, Streamlit, LangChain, and Groq LLMs** that generates personalized question papers, evaluates student answers, and provides detailed assessments and recommendations.

---

# 📚 Project Overview

AI Tutor Agent is a **Single-Agent Educational Assistant** designed to help students practice and improve their learning through:

* Personalized question generation
* Automated answer evaluation
* Detailed performance assessment
* Student progress tracking
* Downloadable question papers and reports

The application supports multiple boards, grades, subjects, and difficulty levels, making it suitable for a wide range of learners.

---

# ✨ Features

## 📝 Personalized Question Generation

* Generates age-appropriate questions

* Supports:

  * CBSE
  * ICSE
  * IB
  * IGCSE
  * State Boards
  * NIOS

* Supports various subjects:

  * Mathematics
  * Science
  * Physics
  * Chemistry
  * Biology
  * English
  * History
  * Geography
  * Computer Science
  * Economics

* Supports question types:

  * MCQ
  * Short Answer
  * Long Answer
  * Mixed

* Difficulty Levels:

  * Easy
  * Medium
  * Hard

---

## 📄 Question Paper Download

Students can download generated question papers as a text file for offline practice.

---

## 📤 Answer Sheet Upload

Students can upload answers in the following formats:

* PDF
* DOCX
* TXT

---

## 📊 Automated Assessment

The AI Tutor evaluates the uploaded answers and generates:

* Overall Score
* Grade
* Logical Thinking Score
* Conceptual Understanding Score
* Accuracy Score
* Application Skill Score
* Critical Analysis Score
* Expression and Clarity Score
* Question-wise Feedback
* Strengths
* Areas of Improvement
* Personalized Recommendations

---

## 🧠 Student Memory

The application maintains student assessment history, enabling future enhancements such as:

* Progress Tracking
* Weak Topic Identification
* Personalized Revision Tests
* Adaptive Learning Recommendations

---

# 🏗️ System Architecture

Student Details
↓
Question Generation
↓
Download Question Paper
↓
Upload Answer Sheet
↓
Answer Extraction
↓
AI Assessment
↓
Performance Report
↓
Student History Tracking

---

# 🤖 Agent Architecture

This project is implemented as a **Single-Agent AI Tutoring System**.

The AI Tutor Agent performs multiple tasks:

1. Question Generation
2. Answer Evaluation
3. Assessment Report Generation
4. Student Performance Tracking
5. Personalized Recommendations

---

# 🛠️ Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## AI/LLM Framework

* LangChain

## Large Language Model

* Groq
* Llama Models

## Document Processing

* PyPDF
* Python-Docx

## Environment Management

* Python-Dotenv

---

# 📂 Project Structure

```text
AI_Tutor_Agent/
│
├── app.py                 # Main Streamlit application
├── assess.py              # Assessment and document extraction logic
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── .gitignore             # Ignore sensitive files
└── .env                   # API Keys (not uploaded to GitHub)
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/ai-tutor-agent.git
cd ai-tutor-agent
```

---

## Create Virtual Environment

### Mac/Linux

```bash
python -m venv demo1_ai
source demo1_ai/bin/activate
```

### Windows

```bash
python -m venv demo1_ai
demo1_ai\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 📈 Future Enhancements

* Multi-Agent Architecture
* Database Integration
* User Authentication
* Progress Dashboard
* Weak Topic Analysis
* Adaptive Learning Paths
* Personalized Revision Plans
* Report Visualization
* Cloud Deployment
* Speech-to-Text Answer Upload
* Image-Based Answer Evaluation

---

# 🎯 Learning Outcomes

This project demonstrates:

* Prompt Engineering
* LangChain Pipelines
* LLM Integration
* Document Processing
* State Management in Streamlit
* Modular Python Design
* AI Application Architecture
* Educational AI Systems
* Agentic Workflow Design

---

# 👩‍💻 Author

**Divya T**

13+ years of experience in Enterprise Integration and currently transitioning into AI Engineering and AI Solution Architecture.

---

# 📜 License

This project is intended for educational and portfolio purposes.

Website: https://ai-tutor-assessment.streamlit.app/
