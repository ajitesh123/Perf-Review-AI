import unittest
import os
from unittest.mock import patch, MagicMock
import speech_recognition as sr
from audio_utils import transcribe_audio, validate_audio_file, AudioTranscriptionError

class TestAudioUtils(unittest.TestCase):
    def test_transcribe_audio_success(self):
        with patch('speech_recognition.Recognizer.recognize_google') as mock_recognize:
            mock_recognize.return_value = "This is a test transcription"
            result = transcribe_audio("test_audio.wav")
            self.assertEqual(result, "This is a test transcription")

    def test_transcribe_audio_unknown_value_error(self):
        with patch('speech_recognition.Recognizer.recognize_google') as mock_recognize:
            mock_recognize.side_effect = sr.UnknownValueError()
            with self.assertRaises(AudioTranscriptionError):
                transcribe_audio("test_audio.wav")

    def test_transcribe_audio_request_error(self):
        with patch('speech_recognition.Recognizer.recognize_google') as mock_recognize:
            mock_recognize.side_effect = sr.RequestError("Test error")
            with self.assertRaises(AudioTranscriptionError):
                transcribe_audio("test_audio.wav")


if __name__ == '__main__':
    unittest.main()
