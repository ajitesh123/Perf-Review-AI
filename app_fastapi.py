from fastapi import FastAPI, HTTPException, File, UploadFile
import speech_recognition as sr
from io import BytesIO

from review import ReviewRequest, generate_review
from self_review import SelfReviewRequest, generate_self_review
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_review")
async def api_generate_review(request: ReviewRequest):
    """
    Generate a performance review based on the provided input.

    Parameters:
    - request: A ReviewRequest object containing the necessary information for generating the review.
      It now includes an optional 'audio_input' field for speech input.

    Returns:
    - A JSON object containing the generated review.

    Raises:
    - HTTPException: If there's an error during review generation or speech-to-text conversion.
    """
    try:
        review = generate_review(
            request.your_role, request.candidate_role, request.perf_question,
            request.your_review,
            request.llm_type,
            request.user_api_key,
            request.model_size,
            request.audio_input
        )
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_self_review")
async def api_generate_self_review(request: SelfReviewRequest):
    """
    Generate a self-review based on the provided input.

    Parameters:
    - request: A SelfReviewRequest object containing the necessary information for generating the self-review.
      It now includes an optional 'audio_input' field for speech input.

    Returns:
    - A JSON object containing the generated self-review.

    Raises:
    - HTTPException: If there's an error during self-review generation or speech-to-text conversion.
    """
    try:
        review = generate_self_review(
            request.text_dump, request.questions, request.instructions,
            request.llm_type,
            request.user_api_key,
            request.model_size,
            request.audio_input
        )
        return {"self_review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speech_to_text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Convert speech to text.

    Parameters:
    - audio_file: An audio file containing speech to be converted to text.

    Returns:
    - A JSON object containing the converted text.

    Raises:
    - HTTPException: If there's an error during speech-to-text conversion.
    """
    try:
        audio_data = await audio_file.read()
        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(audio_data)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return {"text": text}
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Speech recognition could not understand the audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Could not request results from speech recognition service; {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during speech-to-text conversion: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Performance Review API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)