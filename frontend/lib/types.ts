export type Language = "en" | "roman-ur" | "ur";

export type LegalDocumentMeta = {
  document_id: string;
  title: string;
  document_type: string;
  jurisdiction: string;
  authority: string;
  source_name: string;
  source_url: string;
  priority: string;
};

export type FollowUpQuestion = {
  id: string;
  prompt: string;
  type: "text" | "yes_no" | "date";
};

export type ClarificationAnswer = { id: string; question: string; answer: string };

export type TriagePathway = { title: string; description: string; caution?: string };

export type TriageResult = {
  mode: "demo" | "backend" | "backend-fallback";
  category: string;
  summary: string;
  urgency: "low" | "medium" | "high" | "critical" | "unknown";
  facts: string[];
  legalIssues: string[];
  missingInformation: string[];
  suggestedDocuments: string[];
  followUpQuestions: FollowUpQuestion[];
  /** Practical next steps proposed by triage (absent on cases saved before this field existed). */
  pathways?: TriagePathway[];
  sourceIds: string[];
  guardrail: string;
  notice?: string;
};

export type CaseDocument = {
  name: string;
  size: number;
  type: string;
  status: "selected" | "uploaded" | "processing" | "analyzed" | "failed";
};

export type CaseDraft = {
  caseId: string;
  language: Language;
  description: string;
  answers: Record<string, string>;
  /** Answers with the question they answer, so the brief can show both (older cases only have `answers`). */
  clarifications?: ClarificationAnswer[];
  documents: CaseDocument[];
  triage: TriageResult;
  consentAcknowledged: boolean;
  createdAt: string;
  updatedAt: string;
};

export type IntakeDraft = {
  version: 2;
  language: Language;
  step: number;
  description: string;
  answers: Record<string, string>;
  documents: CaseDocument[];
  triage: TriageResult | null;
  /** Triage re-run with the clarification answers; `triage` keeps the original question list. */
  refinedTriage?: TriageResult | null;
  updatedAt: string;
};
