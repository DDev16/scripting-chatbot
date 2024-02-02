import { useState, useEffect } from 'react';
import RecordIcon from './RecordIcon';

type Props = {
  handleStop: (blobUrl: string) => void;
};

function RecordMessage({ handleStop }: Props) {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  useEffect(() => {
    // Request permissions and create media recorder instance
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const newMediaRecorder = new MediaRecorder(stream);
        setMediaRecorder(newMediaRecorder);

        const chunks: BlobPart[] = [];
        newMediaRecorder.ondataavailable = event => {
          chunks.push(event.data);
        };

        newMediaRecorder.onstop = () => {
          const blob = new Blob(chunks, { type: 'audio/mpeg' });
          const blobUrl = URL.createObjectURL(blob);
          handleStop(blobUrl);
          setIsRecording(false); // Reset recording state
        };
      })
      .catch(err => console.error("Error accessing media devices:", err));
  }, [handleStop]);

  const startRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'inactive') {
      mediaRecorder.start();
      setIsRecording(true);
      console.log("Start recording");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      console.log("Stop recording");
      // Do not reset isRecording here since onstop handler will handle it
    }
  };

  // Combine mouse and touch events to handle interaction
  const handleInteractionStart = () => {
    if (!isRecording) {
      startRecording();
    }
  };

  const handleInteractionEnd = () => {
    if (isRecording) {
      stopRecording();
    }
  };

  return (
    <div className="mt-2">
      <button
        onMouseDown={handleInteractionStart}
        onMouseUp={handleInteractionEnd}
        onTouchStart={handleInteractionStart}
        onTouchEnd={handleInteractionEnd}
        className={`bg-white p-4 rounded-full ${isRecording ? "cursor-not-allowed" : ""}`}
      >
        <RecordIcon
          classText={
            isRecording
              ? "animate-pulse text-red-500"
              : "text-sky-500"
          }
        />
      </button>
      <p className="mt-2 text-white font-light">{isRecording ? 'Recording' : 'Not Recording'}</p>
    </div>
  );
  
}

export default RecordMessage;
