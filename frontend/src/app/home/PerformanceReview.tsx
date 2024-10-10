import { useState } from 'react';
import { generateReview } from '@services/review';
import AudioInput from './AudioInput';
import { isBlankObject } from '@utils/object';
import { TextButton } from '@components/ui/button';

const PerformanceReview = ({
  paramsWhenKeysNeeded,
  onReviewResultsReceived,
}: any) => {
  const [yourRole, setYourRole] = useState('');
  const [candidateRole, setCandidateRole] = useState('');
  const [perfQuestion, setPerfQuestion] = useState('');
  const [yourReview, setYourReview] = useState('');
  const [transcription, setTranscription] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerateReview = async () => {
    setIsLoading(true);
    if (
      !isBlankObject(paramsWhenKeysNeeded) &&
      !paramsWhenKeysNeeded?.userApiKey
    ) {
      setIsLoading(false);
      alert('Please enter your API key.');
      return;
    }

    if (!yourRole || !candidateRole) {
      setIsLoading(false);
      alert('Please fill in all required fields.');
      return;
    }

    if (!yourReview && !transcription) {
      setIsLoading(false);
      alert('Please provide either a your review dump or audio input.');
      return;
    }

    try {
      const requestData = {
        your_role: yourRole,
        candidate_role: candidateRole,
        perf_question: perfQuestion,
        your_review: `${yourReview} ${transcription}`,
        is_paid: false,
        ...paramsWhenKeysNeeded,
      };

      const response = (await generateReview(requestData)) as {
        review: Array<{ question: string; answer: string }>;
      };
      onReviewResultsReceived(response.review);
    } catch (error) {
      console.error('Error generating review:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="relative isolate px-6 py-4 lg:py-8 lg:px-8 widget-animate animate in-view">
      <div className="flex flex-col mx-auto max-w-5xl justify-between gap-8 border-secondary items-center rounded-xl border bg-zinc-800 p-6 sm:p-12 sm:px-12  dark:bg-zinc-900">
        <div className="w-full">
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
        <div className="w-full">
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
        <div className="w-full">
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
        <div className="w-full">
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
        <div className="w-full">
          <AudioInput
            paramsWhenKeysNeeded={paramsWhenKeysNeeded}
            onTranscriptionReceived={setTranscription}
          />
        </div>
        <TextButton
          onClick={handleGenerateReview}
          variant={`primary-perf-review`}
          disabled={isLoading}
        >
          {isLoading ? 'Generating...' : 'Generate Performance Review'}
        </TextButton>
      </div>
    </section>
  );
};

export default PerformanceReview;
