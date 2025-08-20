import streamlit as st
from openai import OpenAI

# Initialize OpenAI client (make sure OPENAI_API_KEY is in your env)
client = OpenAI()

st.set_page_config(page_title="Reverse Search Agent", page_icon="🔄")

st.title("🔄 Reverse Search Agent")
st.write("Give me an **answer**, I'll guess the **questions** that could lead to it!")

# User input
answer = st.text_input("Enter an answer:", "")

def reverse_search(answer: str, n: int = 5):
    # Step 1: Generate candidate questions
    prompt = f"""
    You are an AI that generates possible questions for a given answer.
    Answer: "{answer}"
    Generate {n} different questions that could logically have this as the answer.
    """

    gen_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    questions = gen_resp.choices[0].message.content.strip().split("\n")
    questions = [q.strip("-•1234567890. ") for q in questions if q.strip()]

    # Step 2: Validate / filter questions
    validated = []
    for q in questions:
        check_prompt = f"""
        Question: "{q}"
        Proposed Answer: "{answer}"
        Does this question correctly map to the answer? 
        Reply only 'Yes' or 'No'.
        """
        check_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": check_prompt}],
        )
        verdict = check_resp.choices[0].message.content.strip()
        if verdict.lower().startswith("yes"):
            validated.append(q)

    return validated

if answer:
    with st.spinner("Thinking... 🤔"):
        questions = reverse_search(answer, n=7)

    if questions:
        st.subheader("Possible Questions:")
        for q in questions:
            st.write(f"• {q}")
    else:
        st.warning("Couldn't come up with valid questions for that answer 😅")
