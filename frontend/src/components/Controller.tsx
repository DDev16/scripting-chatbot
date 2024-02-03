import { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

type Message = {
  sender: string,
  blobUrl?: string,
  text?: string, // Added to handle text messages
};

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  const createBlobUrl = (data: ArrayBuffer) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    return window.URL.createObjectURL(blob);
  };

  const handleStop = async (blobUrl: string) => {
    if (isLoading) return; // Prevent double submission
    setIsLoading(true);

    try {
      const response = await fetch(blobUrl);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append("file", blob, "myFile.wav");

      // First, post the audio and get the text response
      const textRes = await axios.post("http://localhost:8000/post-audio/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { chat_response, decoded_message } = textRes.data;

      // Add decoded message and chat response to messages
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "me", text: decoded_message },
        { sender: "Chatbot", text: chat_response },
      ]);

      // Then, fetch the audio response from a new endpoint
      const audioRes = await axios.get("http://localhost:8000/get-audio-response/", {
        responseType: "blob",
      });

      const audioUrl = createBlobUrl(audioRes.data);

      // Add the audio response to messages for playback
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "Chatbot", blobUrl: audioUrl },
      ]);

      const audio = new Audio(audioUrl);
      audio.play();
    } catch (error) {
      console.error("Error processing audio:", error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        {/* Conversation */}
        <div className="mt-5 px-5">
          {messages.map((message, index) => {
            return (
              <div
                key={index + message.sender}
                className={`flex flex-col ${message.sender === "rachel" ? "items-end" : ""}`}
              >
                <div className="mt-4">
                  <p className={message.sender === "rachel" ? "text-right mr-2 italic text-green-500" : "ml-2 italic text-blue-500"}>
                    {message.sender}
                  </p>
                  {message.text && (
                    <p className="text-sm bg-gray-100 rounded p-2">{message.text}</p> // Display text message
                  )}
                  {message.blobUrl && (
                    <audio src={message.blobUrl} controls /> // Display audio message
                  )}
                </div>
              </div>
            );
          })}

          {messages.length === 0 && !isLoading && (
            <div className="text-center font-light italic mt-10">
              Send Chatbot a message...
            </div>
          )}

          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Give me a few seconds...
            </div>
          )}
        </div>

        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <RecordMessage handleStop={handleStop} />
          </div>
        </div>
      </div>
    </div>
  );
  
}

export default Controller;
