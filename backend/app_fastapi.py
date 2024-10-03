from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app_fastapi_v1 import v1
from backend.app_fastapi_v2 import v2

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/v1", v1)
app.mount("/v2", v2)

@app.get("/")
async def root():
    return {"message": "Welcome to the Performance Review API"}

# To run this server, use the following command in the terminal:
# uvicorn backend.app_fastapi:app --host 0.0.0.0 --port 8000