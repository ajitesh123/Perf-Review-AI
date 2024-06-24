import os
import streamlit as st
from llm import OpenAILLM, GoogleLLM, AnthropicLLM, GroqLLM

DEFAULT_QUESTIONS = """
- Describe example(s) of the topics selected. What was the context? What actions did they take?
- In your opinion, what impact did their actions have?
- What recommendations do you have for their growth and development? Your feedback can be about any area of their work.
"""

def get_completion(prompt, llm, model_size, input_type="text"):
    if input_type == "voice":
        # For voice input, the prompt is already processed and converted to text
        # in the api_generate_review_voice function
        pass
    return response

def create_llm_instance(llm_type, user_api_key):
    llm_classes = {
        "openai": OpenAILLM,
        "google": GoogleLLM,
        "anthropic": AnthropicLLM,
        "groq": GroqLLM
    }
    
    llm_class = llm_classes.get(llm_type)
    if not llm_class:
        raise ValueError(f"Invalid LLM type: {llm_type}")
    
    return llm_class(api_key=user_api_key)

def generate_prompt(your_role, candidate_role, perf_question, your_review):
    delimiter = "####"
    prompt = f"""
    I'm {your_role}. You're an expert at writing performance reviews. On my behalf, help answer the question for performance reviews below.

    {delimiter} Instructions {delimiter}:
    - Use the context below to understand my perspective of working with them
    - Keep the role of the person I'm reviewing, {candidate_role}, in mind when writing the review
    - Use simple language and keep it to the point
    - Strictly answer the questions mentioned in "question for performance"

    <context>
    {your_review}
    </context>

    <question for performance>
    {perf_question}
    </question for performance>

    {delimiter} Output in markdown format in the following structure:{delimiter}
    - Q1: Mention the first question in question for performance 
    Your answer
    - Q2: Mention the second question in question for performance
    Your answer
    - Q3: Mention the third question in question for performance
    Your answer

    Answer: """
    return prompt

def generate_review(your_role, candidate_role, perf_question, your_review, llm_type, user_api_key, model_size, input_type="text"):
    perf_question = perf_question or DEFAULT_QUESTIONS
    prompt = generate_prompt(your_role, candidate_role, perf_question, your_review)
    llm = create_llm_instance(llm_type, user_api_key)
    response = get_completion(prompt, llm, model_size, input_type)
    return response

# Streamlit UI
st.title("Write Performance Review in a Minute")

st.text("""If no question is passed, following are considered:
        1. Describe example(s) of the topics selected. What was the context? What actions did they take?
        2. In your opinion, what impact did their actions have?
        3. What recommendations do you have for their growth and development? Your feedback can be about any area of their work.
        """)

# Sidebar for LLM and model size selection, and API key input
with st.sidebar:
    llm_type = st.selectbox('Select LLM Type', ['openai', 'google', 'anthropic', 'groq'])
    model_size = st.selectbox('Select Model Size', ['small', 'medium', 'large'])
    user_api_key = st.text_input('Your API Key')

your_role = st.text_input('Your Role')
candidate_role = st.text_input('Candidate Role')
perf_question = st.text_input('Performance Review Questions')
your_review = st.text_area('Briefly describe your experience of working with the candidate including project, responsibility of candidate, unique things they did etc., in free flow writing')

if st.button('Write Review'):
    review = generate_review(your_role, candidate_role, perf_question, your_review, llm_type, user_api_key, model_size="small")
    st.markdown(review)
