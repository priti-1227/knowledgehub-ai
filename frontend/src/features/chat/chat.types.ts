export type AnswerStatus =
    | "answered"
    | "answered_with_conflict"
    | "conflict"
    | "not_found";

export interface ConflictInfo {
    has_conflict: boolean;
    level: "none" | "partial" | "full";
    reason: string;
}

export interface ChatSource {
    chunk_id: string | number;
    document_id: string;
    document_version_id: string;
    document_name: string;
    page_number: number | null;
    score: number;
}

export interface ChatApiResponse {
    answer: string;
    grounded: boolean;

    answer_status: AnswerStatus;

    conflict?: ConflictInfo;

    grounding_reason?: string;

    best_score?: number | null;

    model?: string | null;
    provider?: string | null;

    sources: ChatSource[];
}

export interface ChatMessage {
    id: string;

    role: "user" | "assistant";

    content: string;

    status?: AnswerStatus;

    grounded?: boolean;

    conflict?: ConflictInfo;

    sources?: ChatSource[];
}