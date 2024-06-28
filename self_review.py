from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict
import speech_recognition as sr
from io import BytesIO
from typing import List, Dict, Optional
import re
from llm import OpenAILLM, GoogleLLM, AnthropicLLM, GroqLLM

class SelfReviewRequest(BaseModel):
    text_dump: str
    questions: List[str]
    instructions: Optional[str] = None
    llm_type: str
    user_api_key: str
    model_size: str = "medium"
    audio_input: Optional[UploadFile] = None

    model_config = ConfigDict(protected_namespaces=())

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

def generate_self_review_prompt(text_dump: str, questions: List[str], instructions: Optional[str]) -> str:
    prompt = f"""
    You are an AI assistant tasked with helping write a performance self-review. Use the following information and instructions to generate a comprehensive self-review.

    Text Dump (containing various information about performance):
    {text_dump}

    Questions to Answer:
    {' '.join(f'{i+1}. {q}' for i, q in enumerate(questions))}

    Additional Instructions:
    {instructions or 'No additional instructions provided.'}

    Please provide your self-review in the following XML structure:
    <self-review>
    <question1>
    [Question 1 text]
    </question1>
    <answer1>
    [Your detailed answer for question 1]
    </answer1>
    <question2>
    [Question 2 text]
    </question2>
    <answer2>
    [Your detailed answer for question 2]
    </answer2>
    ...
    </self-review>

    Ensure that your answers are detailed, reflective, and based on the information provided in the text dump.
    """
    return prompt

def parse_self_review_response(response: str) -> List[Dict[str, str]]:
    review_match = re.search(r'<self-review>(.*?)</self-review>', response, re.DOTALL)
    if not review_match:
        raise ValueError("No <self-review> tags found in the response")
    
    review_content = review_match.group(1).strip()
    
    qa_pairs = re.findall(r'<question(\d+)>(.*?)</question\1>\s*<answer\1>(.*?)</answer\1>', review_content, re.DOTALL)
    
    result = [{"question": q.strip(), "answer": a.strip()} for _, q, a in qa_pairs]
    
    return result

def generate_self_review(text_dump: str, questions: List[str], instructions: Optional[str], llm_type: str, user_api_key: str, model_size: str, audio_input: Optional[UploadFile] = None) -> List[Dict[str, str]]:
    if audio_input:
        try:
            # Convert audio to text
            recognizer = sr.Recognizer()
            audio_data = audio_input.file.read()
            with sr.AudioFile(BytesIO(audio_data)) as source:
                audio = recognizer.record(source)
            text_dump = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            raise ValueError("Speech recognition could not understand the audio")
        except sr.RequestError as e:
            raise ValueError(f"Could not request results from speech recognition service; {str(e)}")
        except Exception as e:
            raise ValueError(f"An error occurred during speech-to-text conversion: {str(e)}")

    prompt = generate_self_review_prompt(text_dump, questions, instructions)
    llm = create_llm_instance(llm_type, user_api_key)
    response = llm.generate_text(prompt, model=model_size)
    return parse_self_review_response(response)