# AI Performance Review Generator
Generate performance reviews in minutes using LLM, supporting both text and audio input.


## Setup
1. Clone this repository
pip install -r requirements.txt
```

## Usage
1. Enter the employee's name
2. Enter the employee's job title
3. Choose input method:
   - Text: Provide a summary of the employee's performance in the text area
   - Audio: Upload an audio file (.wav, .mp3, or .ogg format, max 10MB) containing the performance summary
4. If using audio input, wait for the transcription to complete
5. Click "Generate Review" to get an AI-generated performance review

This will start the Streamlit app, and you will be able to interact with the chatbot in your web browser.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
4. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
## Audio Input Feature
- Supported audio formats: WAV, MP3, OGG
- Maximum file size: 10MB
- The audio will be transcribed using Google's Speech Recognition API
- Transcribed text will be displayed before generating the review

Note: Internet connection is required for audio transcription and review generation.

This will start the Streamlit app, and you will be able to interact with it in your web browser.
