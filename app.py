import streamlit as st
from openai import OpenAI

# Initialize OpenAI client (make sure OPENAI_API_KEY is set in your env)
client = OpenAI()

st.set_page_config(page_title="Reverse Search Agent", page_icon="🔄", layout="centered")

st.title("🔄 Reverse Search Agent")
st.write("Give me an **answer**, I'll guess the **questions** that could lead to it!")

# --- User Inputs ---
answer = st.text_input("Enter an answer:", "")

domain = st.selectbox(
    "Choose a domain:",
    ["General Knowledge", "Math", "History", "Science", "Coding / Debugging"]
)

num_qs = st.slider("How many questions to generate?", min_value=3, max_value=10, value=5)

# --- Helper Function ---
def reverse_search(answer: str, domain: str, n: int = 5):
    # Tailor the prompt based on domain
    domain_instruction = {
        "General Knowledge": "Think broadly, including trivia, everyday facts, or general reasoning.",
        "Math": "Focus on mathematical problems, equations, and number logic.",
        "History": "Focus on historical events, people, and dates.",
        "Science": "Focus on biology, chemistry, physics, or general scientific concepts.",
        "Coding / Debugging": "Focus on programming, software errors, or debugging contexts."
    }

    prompt = f"""
    You are an AI that generates possible questions for a given answer.
    Domain: {domain}
    Instruction: {domain_instruction[domain]}
    Answer: "{answer}"
    Generate {n} different questions that could logically have this as the answer.
    """

    gen_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    questions = gen_resp.choices[0].message.content.strip().split("\n")
    questions = [q.strip("-•1234567890. ") for q in questions if q.strip()]

    # Validation step
    validated = []
    for q in questions:
        check_prompt = f"""
        Domain: {domain}
        Question: "{q}"
        Proposed Answer: "{answer}"
        Does this question correctly map to the answer? Reply only 'Yes' or 'No'.
        """
        check_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": check_prompt}],
        )
        verdict = check_resp.choices[0].message.content.strip()
        if verdict.lower().startswith("yes"):
            validated.append(q)

    return validated

# --- Run Agent ---
if answer:
    with st.spinner("Generating possible questions... 🤔"):
        questions = reverse_search(answer, domain, num_qs)

    if questions:
        st.subheader(f"Possible Questions ({domain}):")
        for q in questions:
            st.write(f"• {q}")
    else:
        st.warning("Couldn't come up with valid questions for that answer 😅")
