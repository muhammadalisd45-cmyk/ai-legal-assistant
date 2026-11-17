"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { Language } from "./types";

// Minimal Web Speech API typings — TypeScript's DOM lib ships the result types but not the recognizer itself.
type RecognitionEvent = { resultIndex: number; results: SpeechRecognitionResultList };
type RecognitionErrorEvent = { error: string };
type Recognition = {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  onresult: ((event: RecognitionEvent) => void) | null;
  onerror: ((event: RecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
  abort(): void;
};
type RecognitionConstructor = new () => Recognition;

function recognitionConstructor(): RecognitionConstructor | null {
  if (typeof window === "undefined") return null;
  const w = window as unknown as { SpeechRecognition?: RecognitionConstructor; webkitSpeechRecognition?: RecognitionConstructor };
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null;
}

/**
 * Speech language per intake language. Speech engines cannot write Roman Urdu, so spoken Urdu is transcribed in
 * Urdu script for both Urdu modes — the triage service understands Urdu script and still replies in the chosen language.
 */
export function speechLanguage(language: Language): string {
  return language === "en" ? "en-PK" : "ur-PK";
}

export type VoiceStatus = "checking" | "idle" | "listening" | "unsupported" | "error";

const ERROR_MESSAGES: Record<string, string> = {
  "not-allowed": "Microphone access was blocked. Allow the microphone for this site in your browser settings, then try again.",
  "service-not-allowed": "Microphone access was blocked. Allow the microphone for this site in your browser settings, then try again.",
  "audio-capture": "No microphone was found. Check that one is connected.",
  network: "Voice typing needs an internet connection. Check your connection and try again.",
  "language-not-supported": "This browser cannot transcribe this language. Try Chrome or Edge, or type instead."
};

/**
 * Browser speech-to-text. `onText` receives each finished phrase; `interim` holds the phrase still being spoken.
 * Nothing is recorded or uploaded by this app — the browser's own speech service does the transcription.
 */
export function useVoiceInput(language: Language, onText: (text: string) => void) {
  const [status, setStatus] = useState<VoiceStatus>("checking");
  const [interim, setInterim] = useState("");
  const [error, setError] = useState("");
  const recognition = useRef<Recognition | null>(null);
  const onTextRef = useRef(onText);
  useEffect(() => {
    onTextRef.current = onText;
  }, [onText]);

  useEffect(() => {
    // Checked after mount so the server render and first client render match.
    setStatus(recognitionConstructor() ? "idle" : "unsupported");
    return () => recognition.current?.abort();
  }, []);

  const stop = useCallback(() => {
    recognition.current?.stop();
  }, []);

  const start = useCallback(() => {
    const Ctor = recognitionConstructor();
    if (!Ctor) {
      setStatus("unsupported");
      return;
    }
    recognition.current?.abort();
    const rec = new Ctor();
    rec.lang = speechLanguage(language);
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;
    rec.onresult = (event) => {
      let pending = "";
      for (let i = event.resultIndex; i < event.results.length; i += 1) {
        const result = event.results[i];
        const text = result[0]?.transcript ?? "";
        if (result.isFinal) {
          if (text.trim()) onTextRef.current(text.trim());
        } else {
          pending += text;
        }
      }
      setInterim(pending.trim());
    };
    rec.onerror = (event) => {
      // "no-speech" and "aborted" are normal (silence, or the user pressed stop).
      if (event.error === "no-speech" || event.error === "aborted") return;
      setError(ERROR_MESSAGES[event.error] ?? "Voice typing stopped unexpectedly. You can try again or type instead.");
      setStatus("error");
    };
    rec.onend = () => {
      setInterim("");
      setStatus((current) => (current === "listening" ? "idle" : current));
      if (recognition.current === rec) recognition.current = null;
    };
    recognition.current = rec;
    setError("");
    setInterim("");
    try {
      rec.start();
      setStatus("listening");
    } catch {
      setError("Voice typing could not start. Try again in a moment.");
      setStatus("error");
    }
  }, [language]);

  // Switching language mid-dictation would keep transcribing in the old one.
  useEffect(() => {
    recognition.current?.stop();
  }, [language]);

  return { status, interim, error, start, stop, supported: status !== "unsupported" && status !== "checking" };
}

/** Joins a dictated phrase onto existing text with a sensible separator. */
export function appendDictation(existing: string, phrase: string): string {
  if (!existing.trim()) return phrase;
  const sep = /[\s\n]$/.test(existing) ? "" : " ";
  return `${existing}${sep}${phrase}`;
}
