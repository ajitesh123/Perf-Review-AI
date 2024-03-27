import os
import openai
from dotenv import load_dotenv, dotenv_values
import streamlit as st

load_dotenv()

#API_KEY = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, API_KEY, model="gpt-4"):
    client = openai.OpenAI(api_key=API_KEY)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def generate_review(your_role, candidate_role, your_review, user_questions, your_openai_key):
    prompt = generate_prompt(your_role, candidate_role, your_review)
    response = get_completion(prompt, your_openai_key)
    return response

def generate_prompt(your_role, candidate_role, your_review, user_questions):
    delimiter = "####"
    prompt = f"""
    I’m {your_role}. You’re an expert at writing performance reviews. On my behalf, help answer the question for performance reviews below.

    {delimiter} Instructions {delimiter}:
    - Use the context below to understand my perspective of working with him
    - Keep the role of person I’m review {candidate_role} in mind when writing the review
    - Use simple language and keep it to the point
    - Strictly answer the question mentioned in “question for performance”

    <context>
    {your_review}
    </context>

    <question for performance>
    " + '\n'.join(user_questions) + "
    </question for performance>

    {delimiter} Output in markdown format in following structure:{delimiter}
    - Q1: Describe example(s) of the topics selected. What was the context? What actions did they take?
    Your answer
    - Q2: In your opinion, what impact did their actions have?
    Your answer
    - Q3: What recommendations do you have for their growth and development? Your feedback can be about any area of their work.
    Your answer

    Answer: """
    return prompt

# Streamlit UI
st.title("Write Performance Review in a Minute")

your_openai_key = st.text_input('Your OpenAI key')
your_role = st.text_input('Your Role')
candidate_role = st.text_input('Candidate Role')
your_review = st.text_area('Briefly describe your experience of working with the candidate including project, responsibility of candidate, unique things they did etc., in free flow writing')

if st.button('Write Review'):
    review = generate_review(your_role, candidate_role, your_review, ['Sample question 1', 'Sample question 2'], your_openai_key)
    st.markdown(review)
2