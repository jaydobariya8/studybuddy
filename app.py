"""StudyBuddy - a study-tutor chatbot built with Streamlit and Gemini.

Run with:  streamlit run app.py

The whole app is three boxes:
    UI (Streamlit)  ->  this file (prompt, key, chat history)  ->  Gemini API
"""

import logging
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

logging.getLogger("google_genai.models").setLevel(logging.ERROR)  # hide SDK chatter

load_dotenv()

MODEL = "gemini-2.5-flash"

# The system prompt: Role, Task, Context, Rules.
# This is what turns a generic assistant into StudyBuddy.
SYSTEM_PROMPT = """Role: You are StudyBuddy, a friendly and patient tutor.

Task: Explain concepts simply, with one real-world example, then check understanding.

Context: Your users are Indian college students preparing for exams. They may ask
about any subject - engineering, science, maths, programming, or general studies.

Rules:
- Keep answers under 150 words unless the student asks for more detail.
- Use simple English. Avoid jargon; if you must use a term, define it.
- Give exactly one example per concept.
- If you are not sure, say "I'm not sure" and suggest what to check.
- If the question is not about studies, politely bring the conversation back to learning.
- End every answer with one short question to check understanding.
"""

QUIZ_RULE = """
Quiz mode is ON: after explaining, ask three multiple-choice questions one at a time.
Wait for the student's answer before revealing whether it was correct and moving on.
"""


def build_system_prompt(quiz_mode: bool) -> str:
    """Return the system prompt, with the quiz rule appended when quiz mode is on."""
    return SYSTEM_PROMPT + QUIZ_RULE if quiz_mode else SYSTEM_PROMPT


def ask_gemini(client: genai.Client, history: list[dict[str, str]], quiz_mode: bool) -> str:
    """Send the full conversation to Gemini and return the reply text.

    Args:
        client: An initialised Gemini client.
        history: Every message so far, oldest first. Each item is
            {"role": "user" | "model", "text": "..."}. The model has no
            memory of its own, so the whole list is sent on every turn.
        quiz_mode: Whether to append the quiz rule to the system prompt.

    Returns:
        The model's reply as plain text.
    """
    contents = [
        types.Content(role=message["role"], parts=[types.Part(text=message["text"])])
        for message in history
    ]
    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=build_system_prompt(quiz_mode)),
    )
    return response.text or "I couldn't come up with an answer. Try asking another way."


def friendly_error(error: errors.APIError) -> str:
    """Translate a Gemini API error into a message a student can act on."""
    if error.code in (400, 401, 403):
        return "Gemini rejected the API key. Check GEMINI_API_KEY in your .env file."
    if error.code == 429:
        return "Too many requests - the free tier limit was hit. Wait a minute and try again."
    return f"Gemini returned an error ({error.code}). Try again in a moment."


# --- UI -----------------------------------------------------------------------

st.set_page_config(page_title="StudyBuddy", page_icon="📚")
st.title("📚 StudyBuddy")
st.caption("Ask me anything you're studying. I explain, then I check you got it.")

with st.sidebar:
    st.header("Settings")
    quiz_mode = st.toggle("Quiz mode", value=False, help="After explaining, StudyBuddy quizzes you.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("No API key found. Copy .env.example to .env and paste your key from aistudio.google.com.")
    st.stop()

client = genai.Client(api_key=api_key)

# Chat history lives in session_state so it survives Streamlit's re-runs.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay the conversation so far.
for message in st.session_state.messages:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["text"])

# New message from the student.
if question := st.chat_input("What are you studying today?"):
    st.session_state.messages.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = ask_gemini(client, st.session_state.messages, quiz_mode)
            except errors.APIError as error:
                answer = friendly_error(error)
        st.markdown(answer)

    st.session_state.messages.append({"role": "model", "text": answer})
