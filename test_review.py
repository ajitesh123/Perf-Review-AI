import pytest
from review import generate_review
from unittest.mock import patch, MagicMock

def test_generate_review():
    with patch("review.create_llm_instance") as mock_create_llm:
        mock_llm = MagicMock()
        mock_llm.generate_text.return_value = "<review>Generated review</review>"
        mock_create_llm.return_value = mock_llm

        result = generate_review(
            your_role="Manager",
            candidate_role="Employee",
            perf_question="How was the performance?",
            your_review="Good performance",
            llm_type="openai",
            user_api_key="test_key",
            model_size="medium"
        )

    assert "Generated review" in result
    mock_llm.generate_text.assert_called_once()

@pytest.fixture
def mock_speech_recognition():
    with patch("speech_recognition.Recognizer") as mock_recognizer:
        yield mock_recognizer

def test_generate_review_with_audio_input(mock_speech_recognition):
    mock_recognizer = MagicMock()
    mock_recognizer.recognize_google.return_value = "This is an audio review"
    mock_speech_recognition.return_value = mock_recognizer

    mock_audio_file = MagicMock()
    mock_audio_file.file.read.return_value = b"mock audio data"

    with patch("review.create_llm_instance") as mock_create_llm:
        mock_llm = MagicMock()
        mock_llm.generate_text.return_value = "<review>Generated review from audio</review>"
        mock_create_llm.return_value = mock_llm

        result = generate_review(
            your_role="Manager",
            candidate_role="Employee",
            perf_question="How was the performance?",
            your_review="",
            llm_type="openai",
            user_api_key="test_key",
            model_size="medium",
            audio_input=mock_audio_file
        )

    assert "Generated review from audio" in result
    mock_recognizer.recognize_google.assert_called_once()
    mock_llm.generate_text.assert_called_once()
