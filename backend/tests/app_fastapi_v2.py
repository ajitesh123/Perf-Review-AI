from loguru import logger
import json
import urllib.request
import urllib.error
import io
import os 
import sys
import requests
project_root = os.getcwd()  # Get the current working directory
sys.path.append(project_root)


# Base URL for the FastAPI server
BASE_URL = "http://localhost:8003/v2"

"""
Refresh this token everytime to run the test
TODO: Automate generation of this token
"""
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM0OjFjOmM5OjVlOjJlOmNmOmE4OmYzOmI3Ojg5OjBmOmY0OjA1OjI2OjkxOjE2IiwidHlwIjoiSldUIn0.eyJhdWQiOltdLCJhenAiOiI5ZDY3Yjg3ODBkNWU0NTJkODM0MDc5N2YyZDJlYThjMyIsImV4cCI6MTcyOTI5NTM2NiwiaWF0IjoxNzI4NDMxMzY2LCJpc3MiOiJodHRwczovL2FyY2hpZWFpLmtpbmRlLmNvbSIsImp0aSI6IjgwMDVhNDc2LWY1MGYtNDI5Yy05NzhhLWE4ZTE3M2E3MWJiZSIsIm9yZ19jb2RlIjoib3JnX2UyZWI2NzE1MzE5IiwicGVybWlzc2lvbnMiOltdLCJzY3AiOltdLCJzdWIiOiJrcF9kOGE5NzYwODFlNTk0ZTRjOGVmYTNkMDZkYWZmMzk0ZiJ9.hJd7N4s1jWFfD-6Ha9FV_8F1aLJWCge4OpxPdB5DAaXU_VxI4s7uFtSkMlXFAiSKAdX1FJkaxQtLUNRPGrXgJkrdBKB67Q22ngumjSXdPg-OwVW63Nfgqgaif0AoDwSTafOIYWxLzEQAmIcWqM563Nt45UaIeavJXsUzxMV8L9sLzmjzm6A8_25vHiaGAImQY_72_GrxHmC25AMs4EDRAShx7_427Ap5pVLp3P7VoiUUSISS40b9F4sR_7DkkWcDr6tXJlTkZnBGK7YjBkgHfzBiIF1acIKoy3Ph-Uc_ixIBzy3frFLP1OMrQ6gvT86fPESLVF2UmjLUzLPaFgsMvw"

def test_server_home():
    """Test the /ping endpoint."""
    response = requests.get(f"{BASE_URL}")
    logger.info(f"Response: {response.json()}")
    assert response.status_code == 200, "Expected status code 200, but got {response.status_code}"
    assert response.json()["message"] == "Welcome to the Performance Review API v2"

def test_generate_review():
    """Test the /generate_review endpoint."""
    logger.info("Testing /generate_review endpoint")
    url = f"{BASE_URL}/generate_review"
    logger.info(f"URL: {url}")
    payload = {
        "your_role": "PM",
        "candidate_role": "software developer",
        "your_review": "test - But please generate a detailed OUTPUT FOR TESTING",
        "is_paid":True
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    logger.info(f"Status Code: {response.status_code}")
    response_json = response.json()
    logger.info(json.dumps(response_json, indent=2))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert "review" in response_json, "Response does not contain 'review' key"
    assert len(response_json["review"]) > 0, "Review list is empty"

def test_generate_self_review():
    """Test the /generate_self_review endpoint."""
    logger.info("Testing /generate_self_review endpoint")
    url = f"{BASE_URL}/generate_self_review"
    payload = {
        "text_dump": "this is test but please generate all the text",
        "questions": [
            "How i did this cycle?", "How can I improve"
        ],
        "instructions": "string",
        "is_paid": True
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    logger.info(f"Status Code: {response.status_code}")
    response_json = response.json()
    logger.info(json.dumps(response_json, indent=2))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert "self_review" in response_json, "Response does not contain 'self_review' key"
    assert len(response_json["self_review"]) == 2, "Expected 2 self-review items"

def test_transcribe_audio():
    """Test the /transcribe_audio endpoint."""
    logger.info("Testing /transcribe_audio endpoint")
    url = f"{BASE_URL}/transcribe_audio"
    
    # Path to the audio file
    audio_file_path = "backend/tests/test_data/file_example_MP3_700KB.mp3"
    
    # Prepare the files for the request
    with open(audio_file_path, 'rb') as audio_file:
        files = {
            'file': ('file_example_MP3_700KB.mp3', audio_file, 'audio/mpeg')
        }
        
        params = {
            'is_paid': 'true'
        }
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }

        response = requests.post(url, headers=headers, files=files, params=params)
        logger.info(f"Status Code: {response.status_code}")
        response_json = response.json()
        logger.info(json.dumps(response_json, indent=2))

        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert "transcribed_text" in response_json, "Response does not contain 'transcribed_text' key"
        assert len(response_json["transcribed_text"]) > 0, "Transcribed text is empty"

if __name__ == "__main__":
    test_server_home()
    test_generate_review()
    # print("\n" + "-"*50 + "\n")
    test_generate_self_review()
    # print("\n" + "-"*50 + "\n")
    test_transcribe_audio()

#path: backend/tests/app_fastapi_v2.py