from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, status, Response
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from backend.llm import GroqLLM
from backend.orchestrator import generate_review, generate_self_review, transcribe_audio
from backend.kindle_auth import kinde_client, CONFIG, kinde_configuration
from loguru import logger

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
        logger.info(f"Callback called with code: {code} and state: {state}")
        kinde_client.fetch_token(authorization_response=f"{CONFIG['kinde']['callback_url']}?code={code}&state={state}")
        # Redirect to a success page or dashboard
        logger.info(f"Access token: {kinde_configuration.access_token}")
        logger.info(f"User details: {kinde_client.get_user_details()}")
        # logger.info("Now redirecting to /dashboard")
        # return RedirectResponse(url="/v2/dashboard")
        return {"message": "Callback successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")
    
@v2.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": "Dashboard", "user": current_user}

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


"""
Some other useful settings from Kindle Dashboard:
- To use own signup/login screen: go to "Details" and select "user your own signup/login screen"
- Make sure prod callback urls and logout urls are set in Details
- To not use email and code: we can switch off from "Authentication" tab

TODO: 
- Integerate with Supabase to store # of use of API per users and whether paid or not
- Figure out what API to called to put user details from Kindle to Supabase
- Integeration with Stripe - should we handle in backend or frontend?


To test the API:
1. Test the root endpoint:
curl http://localhost:8003/v2/
{"message":"Welcome to the Performance Review API v2"}

2. curl http://localhost:8003/v2/ping
{"status":"pong"}

3. curl http://localhost:8003/v2/login
{"login_url":"https://archieai.kinde.com/oauth2/auth?response_type=code&client_id=9d67b8780d5e452d8340797f2d2ea8c3&redirect_uri=http%3A%2F%2Flocalhost%3A8003%2Fcallback&scope=openid+profile+email+offline&state=MVEKXbieIS5lOXyU3BliQq3Q776DJU"}%
"""