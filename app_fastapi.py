from fastapi import FastAPI, HTTPException, File, UploadFile
from review import ReviewRequest, generate_review
from self_review import SelfReviewRequest, generate_self_review
import speech_recognition as sr
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_review")
async def api_generate_review(request: ReviewRequest):
    try:
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

@app.post("/generate_review_voice")
async def api_generate_review_voice(
    audio_file: UploadFile = File(...),
    your_role: str = "",
    candidate_role: str = "",
    perf_question: str = "",
    llm_type: str = "openai",
    user_api_key: str = None,
    model_size: str = "large"
):
    try:
        audio_content = await audio_file.read()
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(audio_content)) as source:
            audio_data = recognizer.record(source)
            your_review = recognizer.recognize_google(audio_data)

        review = generate_review(
            your_role, candidate_role, perf_question, your_review,
            llm_type, user_api_key, model_size, input_type="voice"
        )
        return {"review": review, "transcription": your_review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_self_review")
async def api_generate_self_review(request: SelfReviewRequest):
    try:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)