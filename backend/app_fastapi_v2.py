from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from backend.llm import GroqLLM
from backend.orchestrator import generate_review, generate_self_review, transcribe_audio
from backend.kindle_auth import kinde_client, CONFIG, kinde_configuration

v2 = FastAPI()

class ReviewRequestV2(BaseModel):
    your_role: str
    candidate_role: str
    perf_question: Optional[str] = None
    your_review: str
    is_paid: bool

class SelfReviewRequestV2(BaseModel):
    text_dump: str
    questions: List[str] 
    instructions: Optional[str] = None
    is_paid: bool

# OAuth2 scheme for FastAPI
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{CONFIG['kinde']['domain']}/oauth2/auth",
    tokenUrl=f"{CONFIG['kinde']['domain']}/oauth2/token",
)

# Dependency to check if user is authenticated
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not kinde_client.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return kinde_client.get_user_details()

@v2.get("/")
async def root():
    return {"message": "Welcome to the Performance Review API v2"}

@v2.get("/ping")
async def ping():
    return {"status": "pong"}

@v2.post("/generate_review")
async def api_generate_review(request: ReviewRequestV2, current_user: dict = Depends(get_current_user)):
    try:
        review = generate_review(**request.model_dump())
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@v2.post("/generate_self_review")
async def api_generate_self_review(request: SelfReviewRequestV2, current_user: dict = Depends(get_current_user)):
    try:
        self_review = generate_self_review(**request.model_dump())
        return {"self_review": self_review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@v2.post("/transcribe_audio")
async def api_transcribe_audio(file: UploadFile = File(...), is_paid: bool = False, current_user: dict = Depends(get_current_user)):
    try:
        audio_bytes = await file.read()
        transcribed_text = transcribe_audio(is_paid, audio_bytes)
        return {"transcribed_text": transcribed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@v2.get("/login")
async def login():
    login_url = kinde_client.get_login_url()
    return {"login_url": login_url}

@v2.get("/register")
async def register():
    register_url = kinde_client.get_register_url()
    return {"register_url": register_url}

@v2.get("/callback")
async def callback(code: str, state: str):
    try:
        kinde_client.fetch_token(authorization_response=f"{CONFIG['kinde']['callback_url']}?code={code}&state={state}")
        # Redirect to a success page or dashboard
        print(f"Access token: {kinde_configuration.access_token}")  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@v2.get("/logout")
async def logout():
    logout_url = kinde_client.logout(redirect_to=CONFIG['kinde']['logout_url'])
    return {"logout_url": logout_url}

@v2.get("/user")
async def get_user(current_user: dict = Depends(get_current_user)):
    return current_user

@v2.get("/is_authenticated")
async def is_authenticated():
    return {"is_authenticated": kinde_client.is_authenticated()}