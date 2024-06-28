from fastapi import FastAPI, HTTPException, UploadFile, File
from review import ReviewRequest, generate_review
from self_review import SelfReviewRequest, generate_self_review
from speech_to_text import convert_speech_to_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Performance Review API",
    description="An API for generating performance reviews and self-reviews, now with speech-to-text capabilities.",
    version="2.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_review", summary="Generate a performance review")
async def api_generate_review(request: ReviewRequest):
    """
    Generate a performance review based on the provided information.

    - **your_role**: Your role in the review process.
    - **candidate_role**: The role of the candidate being reviewed.
    - **perf_question**: The performance question to be addressed.
    - **your_review**: Your review text (optional if audio_review is provided).
    - **audio_review**: An audio file containing your spoken review (optional).
    - **llm_type**: The type of language model to use.
    - **user_api_key**: Your API key for the chosen language model.
    - **model_size**: The size of the language model to use (default: "medium").

    Returns the generated review.
    """
    try:
        if request.audio_review:
            audio_data = await request.audio_review.read()
            request.your_review = convert_speech_to_text(audio_data)

        review = generate_review(
            request.your_role,
            request.candidate_role,
            request.perf_question,
            request.your_review,
            request.llm_type,
            request.user_api_key,
            request.model_size
        )
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_self_review", summary="Generate a self-review")
async def api_generate_self_review(request: SelfReviewRequest):
    """
    Generate a self-review based on the provided information.

    - **text_dump**: A text dump containing information about your performance (optional if audio_dump is provided).
    - **audio_dump**: An audio file containing spoken information about your performance (optional).
    - **questions**: A list of questions to be addressed in the self-review.
    - **instructions**: Additional instructions for generating the self-review (optional).
    - **llm_type**: The type of language model to use.
    - **user_api_key**: Your API key for the chosen language model.
    - **model_size**: The size of the language model to use (default: "medium").

    Returns the generated self-review.
    """
    try:
        if request.audio_dump:
            audio_data = await request.audio_dump.read()
            request.text_dump = convert_speech_to_text(audio_data)

        review = generate_self_review(
            request.text_dump,
            request.questions,
            request.instructions,
            request.llm_type,
            request.user_api_key,
            request.model_size
        )
        return {"self_review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Performance Review API"}

@app.post("/speech_to_text", summary="Convert speech to text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Convert an uploaded audio file to text using speech recognition.

    - **audio_file**: An audio file containing speech to be converted to text.

    Returns the converted text.
    """
    try:
        audio_data = await audio_file.read()
        text = convert_speech_to_text(audio_data)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
