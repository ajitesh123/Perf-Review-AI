import { useCallback, useRef, useState } from 'react';
import { transcribeAudioBlob } from '@services/audio';
import { isBlankObject, isObject } from '@utils/object';
import { ShimmerText } from 'shimmer-effects-react';
import { useWavesurfer } from '@wavesurfer/react';
// import Timeline from 'wavesurfer.js/dist/plugins/timeline.esm.js';
import tailwindConfig from '../../../tailwind.config';
import { useAppContext } from '@contexts/AppContext';
import { ReviewType } from '@constants/common';
import  { MediaRecorder } from '@constants/media';
// import Audio from './Audio';
import { TextButton } from '@components/ui/button';
import { useReactMediaRecorder } from "react-media-recorder";

const getColor = (reviewType: string, colorType: string) => {
  if(reviewType === ReviewType.perfReview) {
    return tailwindConfig.theme.extend.colors.perfReview[colorType === 'wave' ? 500: 600];
  }
  return tailwindConfig.theme.extend.colors.selfReview[colorType === 'wave' ? 500: 600];
}

const isAudioRecording = (status: string) => {
  return status === MediaRecorder.RECORDING;
}

const AudioInput = ({ paramsWhenKeysNeeded, onTranscriptionReceived }: any) => {
  const { reviewType } = useAppContext();
  const [transcription, setTranscription] = useState<string>(''); // New state for transcription
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [isInitiated, setIsInitiated] = useState(false);
  const [blobUrl, setBlobUrl] = useState('');

  const containerRef = useRef(null);

  const { wavesurfer, isPlaying, currentTime } = useWavesurfer({
    container: containerRef,
    height: 30,
    barHeight: 10,
    barWidth: 1,
    waveColor: getColor(reviewType, 'wave'),
    progressColor: getColor(reviewType, 'progress'),
    url: blobUrl,
    // plugins: useMemo(() => [Timeline.create()], []),
  })

  const onPlayPause = useCallback(() => {
    wavesurfer && wavesurfer.playPause()
  }, [wavesurfer])

  const transcribeAudio = useCallback(
    async (audioBlob: Blob) => {
      if (!audioBlob) {
        alert('Please provide an audio recording.');
        return '';
      }
      if (
        !isBlankObject(paramsWhenKeysNeeded) &&
        !paramsWhenKeysNeeded?.groqApiKey
      ) {
        alert('Please provide Groq API key.');
        return '';
      }

      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.wav');
      if (!isBlankObject(paramsWhenKeysNeeded)) {
        formData.append('groq_api_key', paramsWhenKeysNeeded?.groqApiKey);
      } else {
        formData.append('is_paid', 'false');
      }

      try {
        setIsInitiated(true);
        setIsLoading(true);
        const response = (await transcribeAudioBlob(formData)) as {
          transcribed_text: string;
        };
        console.log('Transcription response:', response);
        const transcribedText = response.transcribed_text;
        setIsError(false);
        // Set transcription state
        setTranscription(transcribedText);
        onTranscriptionReceived(transcribedText);
      } catch (error: unknown) {
        setIsError(true);
        console.error('Error transcribing audio:', error);
        // Check if error is an object and has a 'response' property
        if (
          error &&
          isObject(error) &&
          'response' in error &&
          (error as any).response
        ) {
          console.error('Server response:', (error as any).response.data);
        } else {
          console.error('Unexpected error:', error);
        }
        setTranscription('Unable to transcribe text');
      } finally {
        setIsLoading(false);
      }
    },
    [paramsWhenKeysNeeded, onTranscriptionReceived]
  );

  const { status, startRecording, stopRecording, mediaBlobUrl,  } = useReactMediaRecorder({
    video: false,
    audio: true,
    async onStop(blobUrl, blob) {
      setBlobUrl(blobUrl);
      await transcribeAudio(blob); // Transcribe audio on stop
    },
  });

  const isRecording = isAudioRecording(status);

  const handleStartRecording = useCallback(() => {
    startRecording();
    setBlobUrl('');
  }, [setBlobUrl, startRecording]);

  return (
    <>
      <div className="mb-8">
        <label className="block text-milk text-sm font-bold mb-6">
          Record Audio Review (optional)
        </label>
        <div  className='mb-8 flex justify-center items-center gap-4'>
          <TextButton
            variant='secondary'
            onClick={isRecording ? stopRecording : handleStartRecording}
            className={`${isRecording ? 'bg-red-500 hover:bg-red-500 text-milk' : ''}`}
            disabled={isRecording}
          >
            {isRecording ? 'Recording...' : 'Record'}
          </TextButton>

          {isRecording && (
             <TextButton
              variant='secondary'
              onClick={stopRecording}
            >
              {'Stop Recording'}
            </TextButton>
          )}

          {blobUrl && (
            <div className='flex flex-1 items-center gap-4'>
              <TextButton
                variant='secondary'
                onClick={onPlayPause}
              >
                {isPlaying ? 'Pause' : 'Play'}
              </TextButton>
              <div ref={containerRef} className='w-full' />
            </div>
          )}
        </div>
      </div>

      {/* <Audio /> */}

      {/* Display Transcribed Text */}
      {isInitiated && (
        <div className="mb-4 mt-8">
          <label className="block text-milk text-sm font-medium mb-2">
            {isLoading ? 'Transcribing...' : 'Transcribed Text'}
          </label>
          <div className="w-full md-4 px-3 py-2  border rounded bg-background">
            {isLoading ? (
              <ShimmerText className="m-4" mode="dark" line={3} gap={20} />
            ) : (
              <p className={`${isError ? 'text-red-400' : ''}`}>
                {transcription}
              </p>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default AudioInput;
