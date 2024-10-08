'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Sidebar from './home/Sidebar';
import { generateReview, generateSelfReview } from '@services/review';
import { transcribeAudioBlob } from '@services/audio';

// Dynamically import ReactMediaRecorder to avoid server-side rendering issues
const DynamicMediaRecorder = dynamic(
  () => import('react-media-recorder').then((mod) => mod.ReactMediaRecorder),
  { ssr: false }
);

interface ReviewItem {
  question: string;
  answer: string;
}

export default function Home() {
  const [reviewType, setReviewType] = useState('Performance Review');
  const [llmType, setLlmType] = useState('openai');
  const [modelSize, setModelSize] = useState('small');
  const [userApiKey, setUserApiKey] = useState('');
  const [groqApiKey, setGroqApiKey] = useState<string>('');
  const [yourRole, setYourRole] = useState('');
  const [candidateRole, setCandidateRole] = useState('');
  const [perfQuestion, setPerfQuestion] = useState('');
  const [yourReview, setYourReview] = useState('');
  const [textDump, setTextDump] = useState('');
  const [questions, setQuestions] = useState('');
  const [instructions, setInstructions] = useState('');
  const [review, setReview] = useState<ReviewItem[]>([]);
  const [transcription, setTranscription] = useState<string>(''); // New state for transcription
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);

  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const transcribeAudio = async () => {
    if (!audioBlob || !groqApiKey) {
      alert('Please provide an audio recording and Groq API key.');
      return '';
    }

    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');
    formData.append('groq_api_key', groqApiKey);

    try {
      const response = (await transcribeAudioBlob(formData)) as {
        transcribed_text: string;
      };
      console.log('Transcription response:', response);
      setTranscription(response.transcribed_text); // Set transcription state
      return response.transcribed_text;
    } catch (error: unknown) {
      console.error('Error transcribing audio:', error);

      // Check if error is an object and has a 'response' property
      if (
        error &&
        typeof error === 'object' &&
        'response' in error &&
        (error as any).response
      ) {
        console.error('Server response:', (error as any).response.data);
      } else {
        console.error('Unexpected error:', error);
      }

      return '';
    }
  };

  const handleGenerateReview = async () => {
    if (!userApiKey) {
      alert('Please enter your API key.');
      return;
    }

    let transcribedText = '';
    if (audioBlob) {
      transcribedText = await transcribeAudio();
    }

    try {
      const requestData = {
        your_role: yourRole,
        candidate_role: candidateRole,
        perf_question: perfQuestion,
        your_review: yourReview + transcribedText,
        llm_type: llmType,
        user_api_key: userApiKey,
        model_size: modelSize,
      };

      const response = (await generateReview(requestData)) as {
        review: Array<{ question: string; answer: string }>;
      };
      setReview(response.review);
    } catch (error) {
      console.error('Error generating review:', error);
    }
  };

  const handleGenerateSelfReview = async () => {
    if (!userApiKey) {
      alert('Please enter your API key.');
      return;
    }

    let transcribedText = '';
    if (audioBlob) {
      transcribedText = await transcribeAudio();
    }

    try {
      const requestData = {
        text_dump: textDump + transcribedText,
        questions: questions
          .split('\n')
          .map((q) => q.trim())
          .filter(Boolean),
        instructions: instructions || null,
        llm_type: llmType,
        user_api_key: userApiKey,
        model_size: modelSize,
      };

      const response = (await generateSelfReview(requestData)) as {
        self_review: Array<{ question: string; answer: string }>;
      };
      setReview(response.self_review);
    } catch (error) {
      console.error('Error generating self-review:', error);
    }
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <Sidebar
        onReviewTypeChange={(value: string) => setReviewType(value)}
        onLlmTypeChange={(value: string) => setLlmType(value)}
        onModelSizeChange={(value: string) => setModelSize(value)}
        onUserApiKeyChange={(value: string) => setUserApiKey(value)}
        onGroqApiKeyChange={(value: string) => setGroqApiKey(value)}
      />

      {/* Main content */}
      <div className="flex-1 p-8">
        <h1 className="text-4xl font-bold mb-8">
          Performance Review Assistant
        </h1>
        <div className="bg-white p-8 rounded-lg shadow-md">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Record Audio Review (optional)
            </label>
            {isClient && (
              <DynamicMediaRecorder
                audio
                onStop={async (blobUrl, blob) => {
                  setAudioBlob(blob);
                  await transcribeAudio(); // Transcribe audio on stop
                }}
                render={({
                  status,
                  startRecording,
                  stopRecording,
                  mediaBlobUrl,
                }) => (
                  <div>
                    <p>{status}</p>
                    <button
                      onClick={startRecording}
                      className="mr-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700"
                    >
                      Start Recording
                    </button>
                    <button
                      onClick={stopRecording}
                      className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-700"
                    >
                      Stop Recording
                    </button>
                    {mediaBlobUrl && (
                      <audio src={mediaBlobUrl} controls className="mt-2" />
                    )}
                  </div>
                )}
              />
            )}
          </div>

          {/* Display Transcribed Text */}
          {transcription && (
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Transcribed Text
              </label>
              <textarea
                value={transcription}
                readOnly
                className="w-full px-3 py-2 border rounded bg-gray-50"
                rows={4}
              />
            </div>
          )}

          {reviewType === 'Performance Review' ? (
            <>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Your Role
                </label>
                <input
                  type="text"
                  value={yourRole}
                  onChange={(e) => setYourRole(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Candidate Role
                </label>
                <input
                  type="text"
                  value={candidateRole}
                  onChange={(e) => setCandidateRole(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Performance Review Questions (one per line)
                </label>
                <textarea
                  value={perfQuestion}
                  onChange={(e) => setPerfQuestion(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                  rows={4}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Your Review
                </label>
                <textarea
                  value={yourReview}
                  onChange={(e) => setYourReview(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                  rows={4}
                />
              </div>
              <button
                onClick={handleGenerateReview}
                className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-700"
              >
                Generate Performance Review
              </button>
            </>
          ) : (
            <>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Text Dump (information about your performance)
                </label>
                <textarea
                  value={textDump}
                  onChange={(e) => setTextDump(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                  rows={4}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Questions to Answer in Self-Review (one per line)
                </label>
                <textarea
                  value={questions}
                  onChange={(e) => setQuestions(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                  rows={4}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Additional Instructions (optional)
                </label>
                <textarea
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                  rows={4}
                />
              </div>
              <button
                onClick={handleGenerateSelfReview}
                className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-700"
              >
                Generate Self-Review
              </button>
            </>
          )}
        </div>
        {review.length > 0 && (
          <div className="bg-white p-8 rounded-lg shadow-md mt-8">
            <h2 className="text-2xl font-bold mb-4">Generated Review</h2>
            {review.map((item: ReviewItem, index) => (
              <div key={index} className="mb-4">
                <h3 className="text-lg font-semibold">{item.question}</h3>
                <p>{item.answer}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
