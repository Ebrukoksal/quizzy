import streamlit as st
import json
import random

st.title("QUIZZY")

st.write("This is a quiz app where you can choose different quizzes about different topics.")

# Load questions
with open("data/questions.json", "r") as file:
    data = json.load(file)
    questions = data["questions"]

# Topic mapping
topic_mapping = {
    "Math": "mathematics",
    "Science": "science",
    "History": "history",
    "Geography": "geography",
    "Art": "art",
    "Music": "music"
}

# Display available topics
st.write("You can choose from the following topics:")
for topic in topic_mapping.keys():
    st.write(f"- {topic}")

# Topic selection
selected_topics = st.multiselect(
    "Select the topics you want to take the quiz on:",
    list(topic_mapping.keys())
)

# Initialize session state for quiz
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

# Start quiz button
if st.button("Start Quiz") and selected_topics:
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    
    # Filter questions based on selected topics
    selected_ids = [topic_mapping[topic] for topic in selected_topics]
    filtered_questions = [q for q in questions if q["id"] in selected_ids]
    
    # Randomly select 5 questions from the filtered questions
    st.session_state.quiz_questions = random.sample(filtered_questions, min(5, len(filtered_questions)))
    st.rerun()

# Quiz interface
if st.session_state.quiz_started and st.session_state.quiz_questions:
    current_q = st.session_state.quiz_questions[st.session_state.current_question]
    
    st.write(f"Question {st.session_state.current_question + 1} of {len(st.session_state.quiz_questions)}")
    st.write(f"Score: {st.session_state.score}")
    
    st.write(f"Question: {current_q['question']}")
    
    user_answer = st.text_input("Your answer:").strip().lower()
    
    if st.button("Submit Answer"):
        if user_answer == current_q['answer'].lower():
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! The correct answer was: {current_q['answer']}")
        
        # Move to next question or end quiz
        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
            st.session_state.current_question += 1
            st.rerun()
        else:
            st.balloons()
            st.write(f"Quiz completed! Your final score: {st.session_state.score}/{len(st.session_state.quiz_questions)}")
            st.session_state.quiz_started = False
            st.session_state.quiz_questions = []
 





