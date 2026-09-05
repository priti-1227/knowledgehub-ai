export interface AIChatRequest {
    question: string;
    user_id: number;
    department?: string | null;
    roles: string[];
    is_admin: boolean;
    top_k?: number;
    similarity_threshold?: number;
}

export interface AISource {
    chunk_id: number;
    document_id: number;
    document_version_id: number;
    document_name: string;
    page_number: number | null;
    score: number;
}

export interface AIChatResponse {
    answer: string;
    grounded: boolean;
    grounding_reason: string;
    best_score: number | null;
    model: string | null;
    provider: string | null;
    sources: AISource[];
}


export interface AIIngestRequest {
    file_path: string;
    document_name: string;
    department?: string | null;
}

export interface AIIngestResponse {
    status: string;
    document_id?: number | null;
    version_id?: number | null;
    version_number?: number | null;
    chunks: number;
}
export interface RetryAIIndexingResponse {
    status: string;
    document_id?: number | null;
    version_id?: number | null;
    version_number?: number | null;
    chunks: number;
}
