import speech_recognition as sr
import io

def convert_speech_to_text(audio_data: bytes) -> str:
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        raise ValueError("Speech recognition could not understand the audio")
    except sr.RequestError as e:
        raise RuntimeError(f"Could not request results from speech recognition service; {str(e)}")

