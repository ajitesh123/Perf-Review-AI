import pytest
from self_review import generate_self_review
from unittest.mock import patch, MagicMock

def test_generate_self_review():
    with patch("self_review.create_llm_instance") as mock_create_llm:
        mock_llm = MagicMock()
        mock_llm.generate_text.return_value = "<self-review><question1>Q1</question1><answer1>A1</answer1></self-review>"
        mock_create_llm.return_value = mock_llm

        result = generate_self_review(
            text_dump="Sample text dump",
            questions=["Q1"],
            instructions="Test instructions",
            llm_type="openai",
            user_api_key="test_key",
            model_size="medium"
        )

    assert len(result) == 1
    assert result[0]["question"] == "Q1"
    assert result[0]["answer"] == "A1"
    mock_llm.generate_text.assert_called_once()

@pytest.fixture
def mock_speech_recognition():
    with patch("speech_recognition.Recognizer") as mock_recognizer:
        yield mock_recognizer

def test_generate_self_review_with_audio_input(mock_speech_recognition):
    mock_recognizer = MagicMock()
    mock_recognizer.recognize_google.return_value = "This is an audio self-review"
    mock_speech_recognition.return_value = mock_recognizer

    mock_audio_file = MagicMock()
    mock_audio_file.file.read.return_value = b"mock audio data"

    with patch("self_review.create_llm_instance") as mock_create_llm:
        mock_llm = MagicMock()
        mock_llm.generate_text.return_value = "<self-review><question1>Q1</question1><answer1>A1 from audio</answer1></self-review>"
        mock_create_llm.return_value = mock_llm

        result = generate_self_review(
            text_dump="",
            questions=["Q1"],
            instructions="Test instructions",
            llm_type="openai",
            user_api_key="test_key",
            model_size="medium",
            audio_input=mock_audio_file
        )

    assert len(result) == 1
    assert result[0]["question"] == "Q1"
    assert result[0]["answer"] == "A1 from audio"
    mock_recognizer.recognize_google.assert_called_once()
    mock_llm.generate_text.assert_called_once()
