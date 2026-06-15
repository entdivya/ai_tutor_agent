import os
from io import StringIO
from datetime import datetime

from pypdf import PdfReader
from docx import Document

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Load LLM
# --------------------------------------------------
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=groq_api_key
)

parser = StrOutputParser()


# --------------------------------------------------
# Extract Text
# --------------------------------------------------
def extract_text(uploaded_file):

    text = ""

    if uploaded_file is None:
        return text

    file_extension = (
        uploaded_file.name
        .split(".")[-1]
        .lower()
    )

    if file_extension == "pdf":

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    elif file_extension == "docx":

        document = Document(uploaded_file)

        for para in document.paragraphs:
            text += para.text + "\n"

    elif file_extension == "txt":

        string_data = StringIO(
            uploaded_file.getvalue()
            .decode("utf-8")
        )

        text = string_data.read()

    return text


# --------------------------------------------------
# Assessment Prompt
# --------------------------------------------------
assessment_prompt = ChatPromptTemplate.from_template(
    """
You are an expert teacher.

Evaluate the student's answers.

Student Name:
{student_name}

Board:
{board}

Grade:
{grade}

Subject:
{subject}

Topic:
{topic}

Generated Questions:
{questions}

Student Answers:
{answers}

Evaluate the student and provide:

1. Overall Score out of 100
2. Grade
3. Logical Thinking Score
4. Conceptual Understanding Score
5. Accuracy Score
6. Application Skill Score
7. Critical Analysis Score
8. Expression and Clarity Score

For each question provide:

- Correct / Partially Correct / Incorrect
- Marks out of 10
- Feedback

Finally provide:

Strengths
Areas of Improvement
Personalized Recommendations.

Return the report in a clean, well-structured format.
"""
)


assessment_chain = (
        assessment_prompt
        | llm
        | parser
)


# --------------------------------------------------
# Generate Assessment
# --------------------------------------------------
def generate_assessment(
        student_name,
        board,
        grade,
        subject,
        topic,
        questions,
        answers
):

    report = assessment_chain.invoke(
        {
            "student_name": student_name,
            "board": board,
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "questions": questions,
            "answers": answers
        }
    )

    return report


# --------------------------------------------------
# Save Student History
# --------------------------------------------------
def create_student_record(
        student_name,
        board,
        grade,
        subject,
        topic,
        questions,
        answers,
        assessment_report
):

    record = {
        "date":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),
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
        "questions":
            questions,
        "answers":
            answers,
        "assessment":
            assessment_report
    }

    return record