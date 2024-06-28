from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from fastapi import UploadFile
import re
from llm import OpenAILLM, GoogleLLM, AnthropicLLM, GroqLLM

DEFAULT_QUESTIONS = """
- Describe example(s) of the topics selected. What was the context? What actions did they take?
- In your opinion, what impact did their actions have?
- What recommendations do you have for their growth and development? Your feedback can be about any area of their work.
"""

class ReviewRequest(BaseModel):
    your_role: str
    candidate_role: str
    perf_question: str
    your_review: Optional[str] = None
    audio_review: Optional[UploadFile] = None
    llm_type: str
    user_api_key: str
    model_size: str = "medium"

    model_config = ConfigDict(arbitrary_types_allowed=True)

def get_completion(prompt, llm, model_size):
    response = llm.generate_text(prompt, model=model_size)
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
    <output>
    <question>
    {{Mention the first question in question for performance}}
    </question>
    <answer>
    {{Your answer come here}}
    </answer>
    <question>
    {{Mention the second question in question for performance}}
    </question>
    <answer>
    {{Your answer for second question come here}}
    </answer>
    ...
    </output>
    """
    return prompt

def parse_llm_response(response: str) -> List[Dict[str, str]]:
    output_match = re.search(r'<output>(.*?)</output>', response, re.DOTALL)
    if not output_match:
        raise ValueError("No <output> tags found in the response")
    
    output_content = output_match.group(1).strip()
    
    qa_pairs = re.findall(r'<question>(.*?)</question>\s*<answer>(.*?)</answer>', output_content, re.DOTALL)
    
    result = [{"question": q.strip(), "answer": a.strip()} for q, a in qa_pairs]
    
    return result

def generate_review(your_role, candidate_role, perf_question, your_review, llm_type, user_api_key, model_size):
    perf_question = perf_question or DEFAULT_QUESTIONS
    prompt = generate_prompt(your_role, candidate_role, perf_question, your_review)
    llm = create_llm_instance(llm_type, user_api_key)
    response = get_completion(prompt, llm, model_size)
    return parse_llm_response(response)