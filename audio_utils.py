import speech_recognition as sr

class AudioTranscriptionError(Exception):
    """Custom exception for audio transcription errors."""
    pass

def transcribe_audio(audio_file):
    """
    Transcribe the given audio file to text.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        str: Transcribed text.

    Raises:
        AudioTranscriptionError: If transcription fails.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        raise AudioTranscriptionError("Speech recognition could not understand the audio")
    except sr.RequestError as e:
        raise AudioTranscriptionError(f"Could not request results from speech recognition service; {str(e)}")
    except Exception as e:
        raise AudioTranscriptionError(f"An error occurred during audio transcription: {str(e)}")

def validate_audio_file(file):
    """
    Validate the uploaded audio file.

    Args:
        file (UploadedFile): The uploaded audio file.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    allowed_extensions = ['.wav', '.mp3', '.ogg']
    max_file_size = 10 * 1024 * 1024  # 10 MB

    if not file.name.lower().endswith(tuple(allowed_extensions)):
        return False

    if file.size > max_file_size:
        return False

    return True
