"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useLanguage } from "@/i18n";

interface VoiceInputProps {
  onTranscript: (text: string) => void;
  onError?: (error: string) => void;
  className?: string;
  disabled?: boolean;
}

// Type declarations for Web Speech API
interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onstart: ((this: SpeechRecognition, ev: Event) => void) | null;
  onend: ((this: SpeechRecognition, ev: Event) => void) | null;
  onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => void) | null;
  onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

export default function VoiceInput({
  onTranscript,
  onError,
  className = "",
  disabled = false,
}: VoiceInputProps) {
  const { t, language } = useLanguage();
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [interimText, setInterimText] = useState("");
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Check for browser support
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    setIsSupported(!!SpeechRecognition);
  }, []);

  // Initialize speech recognition
  const initRecognition = useCallback(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) return null;

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    // Set language based on current UI language
    recognition.lang = language === "ur" ? "ur-PK" : "en-US";

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);
      setInterimText("");
    };

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      let finalTranscript = "";
      let interimTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      setInterimText(interimTranscript);

      if (finalTranscript) {
        onTranscript(finalTranscript.trim());
        setInterimText("");
      }
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      console.error("Speech recognition error:", event.error);
      setIsListening(false);
      setInterimText("");

      if (onError) {
        let errorMessage = t.error;
        switch (event.error) {
          case "network":
            errorMessage = t.errorNetwork;
            break;
          case "not-allowed":
            errorMessage = language === "ur"
              ? "مائیکروفون کی اجازت درکار ہے"
              : "Microphone permission required";
            break;
          case "no-speech":
            errorMessage = language === "ur"
              ? "کوئی آواز نہیں سنی گئی"
              : "No speech detected";
            break;
          default:
            errorMessage = event.message || t.error;
        }
        onError(errorMessage);
      }
    };

    return recognition;
  }, [language, onTranscript, onError, t]);

  // Update recognition language when UI language changes
  useEffect(() => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current = initRecognition();
    }
  }, [language, initRecognition, isListening]);

  const startListening = useCallback(() => {
    if (!isSupported || disabled) return;

    if (!recognitionRef.current) {
      recognitionRef.current = initRecognition();
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error("Failed to start recognition:", error);
      }
    }
  }, [isSupported, disabled, initRecognition]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  }, []);

  const toggleListening = useCallback(() => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  }, [isListening, startListening, stopListening]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, []);

  if (!isSupported) {
    return (
      <button
        disabled
        className={`opacity-50 cursor-not-allowed ${className}`}
        title={language === "ur" ? "آواز کی پہچان دستیاب نہیں" : "Voice input not supported"}
      >
        <MicrophoneOffIcon />
      </button>
    );
  }

  return (
    <div className="relative">
      <button
        onClick={toggleListening}
        disabled={disabled}
        className={`
          p-2 rounded-full transition-all duration-200
          ${isListening
            ? "bg-red-500 text-white animate-pulse"
            : "bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
          }
          ${disabled ? "opacity-50 cursor-not-allowed" : ""}
          ${className}
        `}
        title={isListening ? t.voiceStop : t.voiceStart}
        aria-label={isListening ? t.voiceStop : t.voiceStart}
      >
        {isListening ? <MicrophoneActiveIcon /> : <MicrophoneIcon />}
      </button>

      {/* Interim text display */}
      {interimText && (
        <div className="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 bg-black/80 text-white text-sm px-3 py-1 rounded-lg whitespace-nowrap max-w-xs truncate">
          {interimText}
        </div>
      )}

      {/* Listening indicator */}
      {isListening && (
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
        </span>
      )}
    </div>
  );
}

// Microphone Icons
function MicrophoneIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
      />
    </svg>
  );
}

function MicrophoneActiveIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-5 w-5"
      fill="currentColor"
      viewBox="0 0 24 24"
    >
      <path d="M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3z" />
      <path d="M19 11a1 1 0 10-2 0 5 5 0 01-10 0 1 1 0 10-2 0 7 7 0 006 6.92V20H8a1 1 0 100 2h8a1 1 0 100-2h-3v-2.08A7 7 0 0019 11z" />
    </svg>
  );
}

function MicrophoneOffIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4M12 14a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
      />
      <line x1="2" y1="2" x2="22" y2="22" stroke="currentColor" strokeWidth="2" />
    </svg>
  );
}
