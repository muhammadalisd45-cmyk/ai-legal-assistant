"use client";

import { useVoiceInput } from "@/lib/voice-input";
import type { Language } from "@/lib/types";
import { Icon } from "./icons";

const LABELS: Record<Language, { start: string; stop: string; hint: string }> = {
  en: { start: "Speak instead", stop: "Stop listening", hint: "Listening — speak in English" },
  "roman-ur": { start: "Bol kar likhwayein (Urdu)", stop: "Rokein", hint: "Sun rahe hain — Urdu mein bolein. Text Urdu script mein likha jayega." },
  ur: { start: "بول کر لکھوائیں", stop: "روکیں", hint: "سن رہے ہیں — اردو میں بولیں" }
};

/** Mic button that dictates into a text field. Hidden in browsers without speech recognition (e.g. Firefox). */
export function VoiceButton({ language, onText, compact = false }: { language: Language; onText: (text: string) => void; compact?: boolean }) {
  const voice = useVoiceInput(language, onText);
  const label = LABELS[language];
  if (!voice.supported) return null;
  const listening = voice.status === "listening";

  return (
    <div className={compact ? "voice-input compact" : "voice-input"}>
      <button
        type="button"
        className={listening ? "voice-button listening" : "voice-button"}
        onClick={listening ? voice.stop : voice.start}
        aria-pressed={listening}
        aria-label={listening ? label.stop : label.start}
      >
        <Icon name="mic" size={compact ? 16 : 18} />
        {!compact && <span>{listening ? label.stop : label.start}</span>}
        {listening && <i className="voice-pulse" aria-hidden="true" />}
      </button>
      <div className="voice-status" aria-live="polite">
        {listening && <span>{voice.interim || label.hint}</span>}
        {voice.status === "error" && <span className="voice-error" role="alert">{voice.error}</span>}
      </div>
    </div>
  );
}
