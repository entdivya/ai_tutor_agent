# ---------------------------------------------------
# Imports
# ---------------------------------------------------
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import functions from assess.py
from asses import (
    extract_text,
    generate_assessment,
    create_student_record
)


# ---------------------------------------------------
# Page Configuration
# Must be the first Streamlit command
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Tutor Agent",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()


# ---------------------------------------------------
# Session State Initialization
# Session state keeps data during reruns
# ---------------------------------------------------
if "questions" not in st.session_state:
    st.session_state.questions = ""

if "assessment_report" not in st.session_state:
    st.session_state.assessment_report = None

if "answer_text" not in st.session_state:
    st.session_state.answer_text = ""

if "student_history" not in st.session_state:
    st.session_state.student_history = []


# ---------------------------------------------------
# Initialize LLM
# Used only for Question Generation
# Assessment LLM is in assess.py
# ---------------------------------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=groq_api_key
)


# ---------------------------------------------------
# Prompt Template for Question Generation
# ---------------------------------------------------
question_prompt = ChatPromptTemplate.from_template(
    """
You are an expert tutor.

Generate exactly {num_questions}
age-appropriate questions.

Student Name: {student_name}
Board: {board}
Grade: {grade}
Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}
Question Type: {question_type}

Instructions:

1. Questions must match the {board} curriculum.
2. Questions must suit Grade {grade}.
3. Questions should cover the topic '{topic}'.
4. Follow the selected difficulty level.
5. Number all questions properly.
6. Do NOT provide answers.
7. Do NOT provide explanations.

Question Type Rules:

- MCQ only → Generate only MCQs with 4 options.
- Short answer → Generate only short-answer questions.
- Long answer → Generate only long-answer questions.
- Mixed → Generate a combination of question types.
"""
)


# ---------------------------------------------------
# Create LangChain Pipeline
# Prompt → LLM → String Output
# ---------------------------------------------------
parser = StrOutputParser()

question_chain = (
        question_prompt
        | llm
        | parser
)


# ---------------------------------------------------
# UI
# ---------------------------------------------------
st.title("📄 AI Tutor")
st.write(
    "Generate personalized question papers "
    "and assess student answers."
)

st.header("Enter Student Details")


# ---------------------------------------------------
# Student Inputs
# ---------------------------------------------------
student_name = st.text_input(
    "Student Name"
)

board = st.selectbox(
    "Board",
    [
        "CBSE",
        "ICSE",
        "IB",
        "IGCSE",
        "State Board",
        "NIOS",
        "Other"
    ]
)

grade = st.selectbox(
    "Grade",
    [6, 7, 8, 9, 10, 11, 12]
)

subject = st.selectbox(
    "Subject",
    [
        "Maths",
        "Science",
        "Physics",
        "Chemistry",
        "Biology",
        "English",
        "History",
        "Geography",
        "Computer Science",
        "Economics"
    ]
)

topic = st.text_input(
    "Topic / Chapter"
)

num_questions = st.selectbox(
    "Number of Questions",
    [3, 5, 7, 10]
)

difficulty = st.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

question_type = st.selectbox(
    "Question Type",
    [
        "Mixed",
        "MCQ only",
        "Short answer",
        "Long answer"
    ]
)


# ---------------------------------------------------
# Generate Questions Button
# ---------------------------------------------------
generate_btn = st.button(
    "Generate Questions"
)


# ---------------------------------------------------
# Generate Questions
# ---------------------------------------------------
if generate_btn:

    if not student_name.strip():

        st.error(
            "Please enter Student Name."
        )

    elif not topic.strip():

        st.error(
            "Please enter Topic."
        )

    else:

        with st.spinner(
            "Generating questions..."
        ):

            questions = question_chain.invoke(
                {
                    "student_name":
                        student_name,
                    "board":
                        board,
                    "grade":
                        grade,
                    "subject":
                        subject,
                    "topic":
                        topic,
                    "difficulty":
                        difficulty,
                    "question_type":
                        question_type,
                    "num_questions":
                        num_questions
                }
            )

            st.session_state.questions = (
                questions
            )

        st.success(
            "Questions generated successfully!"
        )


# ---------------------------------------------------
# Display Questions
# ---------------------------------------------------
if st.session_state.questions:

    st.subheader(
        "Generated Questions"
    )

    st.write(
        st.session_state.questions
    )

    # --------------------------------------------
    # Create Answer Section
    # --------------------------------------------
    answer_section = (
        "\n------------------------------------\n"
        "ANSWERS\n"
        "------------------------------------\n"
    )

    for i in range(
            1,
            num_questions + 1
    ):

        answer_section += (
            f"\nQ{i}:\n\n"
        )

    # --------------------------------------------
    # Create Question Paper
    # --------------------------------------------
    question_file_content = f"""
AI Tutor - Question Paper
Generated On:
{datetime.now().strftime('%d-%m-%Y %H:%M')}

Student Name: {student_name}
Board: {board}
Grade: {grade}
Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}
Question Type: {question_type}

------------------------------------
QUESTIONS
------------------------------------

{st.session_state.questions}

{answer_section}
"""

    safe_name = (
        student_name
        .replace(" ", "_")
    )

    st.download_button(
        label="⬇️ Download Question Paper",
        data=question_file_content,
        file_name=
        f"{safe_name}_{subject}_questions.txt",
        mime="text/plain"
    )

    # --------------------------------------------
    # Upload Answer Sheet
    # --------------------------------------------
    st.divider()

    st.subheader(
        "Upload Answer Sheet for analysis"
    )

    uploaded_answers = (
        st.file_uploader(
            "Upload Answers",
            type=[
                "pdf",
                "docx",
                "txt"
            ]
        )
    )

    # --------------------------------------------
    # Extract Uploaded Answers
    # --------------------------------------------
    if uploaded_answers:

        answer_text = extract_text(
            uploaded_answers
        )

        st.session_state.answer_text = (
            answer_text
        )

        st.subheader(
            "Extracted Answers"
        )

        st.text_area(
            "Answer Sheet Content",
            answer_text,
            height=250
        )

    # --------------------------------------------
    # Analyse Button
    # --------------------------------------------
    analyse_btn = st.button(
        "Analyse Answer Sheet"
    )

    # --------------------------------------------
    # Generate Assessment
    # --------------------------------------------
    if analyse_btn:

        if not uploaded_answers:

            st.error(
                "Please upload an answer sheet."
            )

        else:

            with st.spinner(
                "Evaluating answers..."
            ):

                report = (
                    generate_assessment(
                        student_name,
                        board,
                        grade,
                        subject,
                        topic,
                        st.session_state.questions,
                        st.session_state.answer_text
                    )
                )

                st.session_state.assessment_report = (
                    report
                )

                # Save history
                student_record = (
                    create_student_record(
                        student_name,
                        board,
                        grade,
                        subject,
                        topic,
                        st.session_state.questions,
                        st.session_state.answer_text,
                        report
                    )
                )

                st.session_state.student_history.append(
                    student_record
                )

            st.success(
                "Assessment completed successfully!"
            )


# ---------------------------------------------------
# Display Assessment Report
# ---------------------------------------------------
if st.session_state.assessment_report:

    st.subheader(
        "Assessment Report"
    )

    st.write(
        st.session_state.assessment_report
    )

    report_content = f"""
AI Tutor Assessment Report
Generated On:
{datetime.now().strftime('%d-%m-%Y %H:%M')}

Student Name: {student_name}
Board: {board}
Grade: {grade}
Subject: {subject}
Topic: {topic}

------------------------------------
ASSESSMENT REPORT
------------------------------------

{st.session_state.assessment_report}
"""

    safe_name = (
        student_name
        .replace(" ", "_")
    )

    st.download_button(
        label="⬇️ Download Assessment Report",
        data=report_content,
        file_name=
        f"{safe_name}_{subject}_assessment.txt",
        mime="text/plain"
    )