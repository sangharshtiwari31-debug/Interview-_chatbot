import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import matplotlib.pyplot as plt
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Interview Chatbot",
    page_icon="💼",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 18px;
    background-color: #4CAF50;
    color: white;
}
.score-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #e8f5e9;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("💼 AI Interview Chatbot")
st.write("Practice your interview skills with smart evaluation and feedback.")

# ---------------- SESSION STATE ----------------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.total_score = 0
    st.session_state.history = []
    st.session_state.submitted = False
    st.session_state.start_time = time.time()

# ---------------- QUESTIONS ----------------
questions = [
    {
        "question": "Tell me about yourself",
        "ideal": "I am a motivated student with strong technical skills and passion for learning.",
        "keywords": ["student", "skills", "learning", "technical"]
    },
    {
        "question": "What are your strengths?",
        "ideal": "My strengths are teamwork, adaptability, and problem solving.",
        "keywords": ["teamwork", "adaptability", "problem"]
    },
    {
        "question": "What are your weaknesses?",
        "ideal": "I focus too much on details but improve using time management.",
        "keywords": ["improve", "time", "management"]
    },
    {
        "question": "Why should we hire you?",
        "ideal": "I can contribute skills, dedication, and willingness to learn.",
        "keywords": ["skills", "dedication", "learn"]
    },
    {
        "question": "Where do you see yourself in 5 years?",
        "ideal": "I see myself growing professionally and taking responsibilities.",
        "keywords": ["growth", "career", "responsibility"]
    }
]

# ---------------- FUNCTIONS ----------------

def similarity_score(user, ideal):
    return SequenceMatcher(None, user.lower(), ideal.lower()).ratio() * 5


def keyword_score(user, keywords):
    score = 0
    for word in keywords:
        if word.lower() in user.lower():
            score += 1
    return score


def structure_score(user):
    words = len(user.split())

    if words > 60:
        return 3
    elif words > 30:
        return 2
    elif words > 15:
        return 1
    return 0


def confidence_score(user):
    confident_words = [
        "confident", "definitely", "sure",
        "can", "will", "strong", "capable"
    ]

    score = 0
    for word in confident_words:
        if word in user.lower():
            score += 0.5

    return min(score, 2)


def grammar_bonus(user):
    sentences = user.split(".")
    if len(sentences) >= 2:
        return 1
    return 0


def performance_label(score):
    if score >= 12:
        return "🔥 Excellent"
    elif score >= 8:
        return "👍 Good"
    else:
        return "📌 Needs Improvement"


def generate_feedback(sim, key, struct, conf):
    feedback = []

    if sim > 3:
        feedback.append("✅ Your answer matches expected concepts.")
    else:
        feedback.append("⚠️ Try improving answer relevance.")

    if key >= 2:
        feedback.append("✅ Good keyword usage.")
    else:
        feedback.append("💡 Add more important keywords.")

    if struct >= 2:
        feedback.append("✅ Your answer is well structured.")
    else:
        feedback.append("📌 Add more explanation and details.")

    if conf >= 1:
        feedback.append("💪 Confident tone detected.")
    else:
        feedback.append("🔊 Use confident words like 'I can' or 'I will'.")

    return feedback

# ---------------- MAIN INTERVIEW ----------------

if st.session_state.q_index < len(questions):

    q = questions[st.session_state.q_index]

    # Progress bar
    progress = (st.session_state.q_index + 1) / len(questions)
    st.progress(progress)

    st.subheader(
        f"Question {st.session_state.q_index + 1} / {len(questions)}"
    )

    st.write(f"### ❓ {q['question']}")

    # Timer
    elapsed = int(time.time() - st.session_state.start_time)
    st.info(f"⏱ Time Spent: {elapsed} sec")

    user_answer = st.text_area(
        "✍️ Your Answer",
        height=180,
        placeholder="Type your answer here..."
    )

    if st.button("Submit Answer"):

        if user_answer.strip() == "":
            st.warning("Please write your answer.")
        else:

            # Scoring
            sim = similarity_score(user_answer, q["ideal"])
            key = keyword_score(user_answer, q["keywords"])
            struct = structure_score(user_answer)
            conf = confidence_score(user_answer)
            grammar = grammar_bonus(user_answer)

            total = round(sim + key + struct + conf + grammar, 2)

            st.session_state.total_score += total

            # Save history
            st.session_state.history.append({
                "Question": q["question"],
                "Score": total
            })

            # Score Card
            st.markdown(
                f"""
                <div class="score-box">
                <h3>📊 Total Score: {total}/15</h3>
                <h4>{performance_label(total)}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Breakdown
            st.write("## 📈 Score Breakdown")
            st.write(f"Similarity Score: {round(sim,2)} / 5")
            st.write(f"Keyword Score: {key} / 4")
            st.write(f"Structure Score: {struct} / 3")
            st.write(f"Confidence Score: {conf} / 2")
            st.write(f"Grammar Bonus: {grammar} / 1")

            # Suggested Answer
            st.write("## 🤖 Suggested Answer")
            st.success(q["ideal"])

            # Feedback
            st.write("## 💬 Feedback")
            for item in generate_feedback(sim, key, struct, conf):
                st.write(item)

            # Motivational line
            st.info("🚀 Great effort! Keep improving your communication skills.")

            # Wait
            with st.spinner("Moving to next question..."):
                time.sleep(3)

            st.session_state.q_index += 1
            st.session_state.start_time = time.time()
            st.rerun()

# ---------------- FINAL RESULT ----------------

else:

    st.balloons()

    st.title("🎉 Interview Completed")

    final_score = round(st.session_state.total_score, 2)

    st.success(f"🏆 Final Score: {final_score}")

    # Overall Result
    if final_score > 55:
        st.success("🔥 Excellent Performance!")
    elif final_score > 35:
        st.info("👍 Good Job! Keep Practicing.")
    else:
        st.warning("📌 Practice More To Improve.")

    # Table Summary
    st.write("## 📋 Performance Summary")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    # Chart
    st.write("## 📊 Score Analysis")

    fig, ax = plt.subplots()

    ax.pie(
        df["Score"],
        labels=df["Question"],
        autopct='%1.1f%%'
    )

    st.pyplot(fig)

    # Download Report
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="interview_report.csv",
        mime="text/csv"
    )

    # Restart
    if st.button("🔄 Restart Interview"):

        st.session_state.q_index = 0
        st.session_state.total_score = 0
        st.session_state.history = []
        st.session_state.submitted = False
        st.session_state.start_time = time.time()

        st.rerun()