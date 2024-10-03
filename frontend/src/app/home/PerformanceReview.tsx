import { useState } from 'react';
import AudioInput from './AudioInput';
import { generateReview } from '@services/review';

const PerformanceReview = ({ userApiKey, groqApiKey }: any) => {
  const [yourRole, setYourRole] = useState('');
  const [candidateRole, setCandidateRole] = useState('');
  const [perfQuestion, setPerfQuestion] = useState('');
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [yourReview, setYourReview] = useState('');
  const [llmType, setLlmType] = useState('openai');
  const [modelSize, setModelSize] = useState('small');

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

  return (
    <section className="relative isolate px-6 py-4 lg:py-8 lg:px-8">
      <div className="flex flex-col mx-auto max-w-5xl justify-between gap-10">
        <div className="h-full w-full widget-animate animate">
          <div className="border-secondary grid max-w-full gap-8 rounded-xl border bg-zinc-800 p-6 sm:p-12 sm:px-12 sm:text-base dark:bg-zinc-900">
            <div>
              <div className="mb-6">
                <label className="block text-milk text-sm font-medium mb-2">
                  Your Role
                </label>
                <input
                  type="text"
                  value={yourRole}
                  onChange={(e) => setYourRole(e.target.value)}
                  placeholder="Please enter your role"
                  className="w-full px-3 py-2 border rounded
                    bg-background border-gray-700 text-gray-300
                    placeholder:text-gray-600 hover:bg-neutral-800"
                />
              </div>
              <div className="mb-6">
                <label className="block text-milk text-sm font-medium mb-2">
                  Candidate Role
                </label>
                <input
                  type="text"
                  value={candidateRole}
                  onChange={(e) => setCandidateRole(e.target.value)}
                  placeholder="Please enter candidate role"
                  className="w-full px-3 py-2 border rounded
                    bg-background border-gray-700 text-gray-300
                    placeholder:text-gray-600 hover:bg-neutral-800"
                />
              </div>
              <div className="mb-6">
                <label className="block text-milk text-sm font-medium mb-2">
                  Performance Review Questions (one per line)
                </label>
                <textarea
                  value={perfQuestion}
                  onChange={(e) => setPerfQuestion(e.target.value)}
                  placeholder="Please enter questions..."
                  className="w-full px-3 py-2 border rounded
                    bg-background border-gray-700 text-gray-300
                    placeholder:text-gray-600 hover:bg-neutral-800"
                  rows={4}
                />
              </div>
              <div className="mb-6">
                <label className="block text-milk text-sm font-medium mb-2">
                  Your Review
                </label>
                <textarea
                  value={yourReview}
                  onChange={(e) => setYourReview(e.target.value)}
                  placeholder="Please enter your review..."
                  className="w-full px-3 py-2 border rounded
                    bg-background border-gray-700 text-gray-300
                    placeholder:text-gray-600 hover:bg-neutral-800"
                  rows={4}
                />
              </div>
              <AudioInput groqApiKey={groqApiKey} />
              <button
                onClick={handleGenerateReview}
                className="w-full bg-violet-500 text-white py-2 rounded hover:bg-violet-600"
              >
                Generate Performance Review
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PerformanceReview;