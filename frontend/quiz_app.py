import streamlit as st
import requests

BACKEND_URL = "http://capitals-quiz-backend-service" 

st.title("World Capitals Quiz")

# --- Session state init ---
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "user_path" not in st.session_state:
    st.session_state.user_path = None

def log_in_user():
    user_id_input = st.text_input("Enter your user ID")
    if st.button("Start"):
        st.session_state.user_id = user_id_input
        st.rerun()

# --- User ID entry ---
if st.session_state.user_id is None:
    log_in_user()
else:
    st.write(f"Logged in as user: {st.session_state.user_id}")

    # --- Fetch a question ---
    if st.session_state.current_question is None:
        if st.button("Get Question"):
            response = requests.post(
                f"{BACKEND_URL}/question",
                json={"user_id": st.session_state.user_id}
            )
            st.session_state.current_question = response.json()
            st.rerun()
    else:
        st.subheader(f"What is the capital of {st.session_state.current_question}?")
        answer = st.text_input("Your answer")

        if st.button("Submit"):
            response = requests.post(
                f"{BACKEND_URL}/answer",
                json={
                    "user_id": st.session_state.user_id,
                    "question_value": st.session_state.current_question,
                    "answer_value": answer
                }
            )
            answer_result = response.json()
            st.session_state.user_path = answer_result["user_path"]
            st.session_state.feedback = "Correct!" if answer_result["correct"] else "Incorrect. Click 'Get Question' to try another."
            st.session_state.current_question = None
            st.rerun()

    if st.session_state.feedback:
        st.write(st.session_state.feedback)
        st.session_state.feedback = None

    # --- Reset ---
    if st.button("Reset my progress"):
        requests.post(
            f"{BACKEND_URL}/user_reset",
            json={"user_path": st.session_state.user_path}
        )
        st.write("Progress reset!")
        st.session_state.current_question = None
        st.session_state.feedback = None
        st.rerun()

    if st.button("Logout user"):
        st.session_state.user_id = None
        log_in_user()
