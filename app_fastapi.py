from fastapi import FastAPI, HTTPException
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

@app.post("/generate_review")
async def api_generate_review(request: ReviewRequest):
    try:
        review = generate_review(
            request.your_role,
            request.candidate_role,
            request.perf_question,
            request.your_review,
            request.audio_review,
            request.llm_type,
            request.user_api_key,
            request.model_size
        )
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_self_review")
async def api_generate_self_review(request: SelfReviewRequest):
    try:
        review = generate_self_review(
            request.text_dump,
            request.audio_review,
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