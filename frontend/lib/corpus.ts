import records from "../data/legal_documents.json";
import type { LegalDocumentMeta } from "./types";

export const legalDocuments = records as LegalDocumentMeta[];

const BY_ID = new Map(legalDocuments.map((document) => [document.document_id, document]));

export function getCorpusStats() {
  const federal = legalDocuments.filter((d) => d.jurisdiction === "Federal").length;
  const sindh = legalDocuments.filter((d) => d.jurisdiction === "Sindh").length;
  const punjab = legalDocuments.filter((d) => d.jurisdiction === "Punjab").length;
  const kp = legalDocuments.filter((d) => d.jurisdiction === "Khyber Pakhtunkhwa").length;
  const balochistan = legalDocuments.filter((d) => d.jurisdiction === "Balochistan").length;
  const placeholders = legalDocuments.filter((d) =>
    d.title.toLowerCase().includes("placeholder")
  ).length;

  return {
    total: legalDocuments.length,
    federal,
    sindh,
    punjab,
    kp,
    balochistan,
    placeholders,
    verifiedMetadata: legalDocuments.length - placeholders
  };
}

export function getDocumentsByIds(ids: string[]) {
  return ids.map((id) => BY_ID.get(id)).filter(Boolean) as LegalDocumentMeta[];
}

type TopicRule = {
  words: string[];
  ids: string[];
};

const topicRules: TopicRule[] = [
  {
    words: ["property", "land", "plot", "qabza", "possession", "inheritance", "inherited", "warasat", "registry", "title"],
    ids: ["PK-009", "PK-010", "PK-037", "PK-007", "PK-004", "PK-008"]
  },
  {
    words: ["land revenue", "mutation", "intiqal", "fard", "patwari", "girdawari"],
    ids: ["PB-002", "KP-003", "BL-002", "PK-010"]
  },
  {
    words: ["rent", "rented", "tenant", "landlord", "kiraya"],
    ids: ["SD-003", "PK-005", "PK-004"]
  },
  {
    words: ["crime", "fir", "police", "arrest", "bail", "criminal", "theft", "assault"],
    ids: ["PK-002", "PK-003", "PK-006"]
  },
  {
    words: ["divorce", "talaq", "khula", "maintenance", "nafqa", "custody", "guardianship", "dowry", "jahez", "nikah", "second marriage"],
    ids: ["PK-023", "PK-024", "PK-025", "PK-026"]
  },
  {
    words: ["cyber", "online", "hacking", "blackmail", "social media", "fake account", "fia"],
    ids: ["PK-021", "PK-018", "PK-002"]
  },
  {
    words: ["salary", "wages", "factory", "worker", "labour", "labor", "union", "eobi", "pension"],
    ids: ["PK-029", "PK-027", "PK-028", "PK-030", "PB-004"]
  },
  {
    words: ["tax", "fbr", "income tax", "sales tax", "customs"],
    ids: ["PK-034", "PK-033", "PK-032", "PK-035"]
  },
  {
    words: ["contract", "agreement", "payment", "vendor", "business", "company", "partnership"],
    ids: ["PK-005", "PK-012", "PK-013", "PK-011", "PK-014"]
  },
  {
    words: ["harassment", "workplace", "office", "employer"],
    ids: ["PK-017", "PK-006"]
  },
  {
    words: ["consumer", "shop", "service", "product", "refund"],
    ids: ["PB-001", "SD-006", "KP-001", "PK-022", "PK-013"]
  },
  {
    words: ["domestic violence", "abuse", "violence at home"],
    ids: ["SD-008", "PK-020"]
  },
  {
    words: ["child marriage", "minor marriage"],
    ids: ["SD-009", "PK-020"]
  },
  {
    words: ["money laundering", "aml", "suspicious transaction"],
    ids: ["PK-015"]
  },
  {
    words: ["terror", "terrorism"],
    ids: ["PK-016", "PK-003", "PK-006"]
  }
];

function termMatches(text: string, term: string) {
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`\\b${escaped}\\b`, "i").test(text);
}

export function findRelevantSourceIds(text: string, limit = 5) {
  const normalized = text.toLowerCase();
  const scores = new Map<string, number>();

  for (const rule of topicRules) {
    const hits = rule.words.filter((word) => termMatches(normalized, word)).length;
    if (!hits) continue;
    rule.ids.forEach((id, index) => {
      scores.set(id, (scores.get(id) ?? 0) + hits * (rule.ids.length - index));
    });
  }

  if (scores.size === 0) {
    ["PK-001", "PK-004", "PK-006", "PK-020"].forEach((id, index) => {
      scores.set(id, 10 - index);
    });
  }

  return [...scores.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([id]) => id);
}

export function isPlaceholderDocument(document: LegalDocumentMeta) {
  return document.title.toLowerCase().includes("placeholder");
}
