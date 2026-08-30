import { aiConfig } from "../../config/ai.config.js";

import {
    AIChatRequest,
    AIChatResponse,
    AIIngestRequest,
    AIIngestResponse,
} from "./ai.types.js";


export class AIService {
    private async request<T>(
        endpoint: string,
        options: RequestInit
    ): Promise<T> {
        const controller = new AbortController();

        const timeout = setTimeout(
            () => controller.abort(),
            aiConfig.timeoutMs
        );

        try {
            const response = await fetch(
                `${aiConfig.baseUrl}${endpoint}`,
                {
                    ...options,
                    signal: controller.signal,
                    headers: {
                        "Content-Type": "application/json",
                        ...options.headers,
                    },
                }
            );

            if (!response.ok) {
                const errorBody = await response.text();

                throw new Error(
                    `AI service error ${response.status}: ${errorBody}`
                );
            }

            return (await response.json()) as T;
        } catch (error) {
            if (
                error instanceof Error &&
                error.name === "AbortError"
            ) {
                throw new Error(
                    "AI service request timed out."
                );
            }

            throw error;
        } finally {
            clearTimeout(timeout);
        }
    }


    async chat(
        payload: AIChatRequest
    ): Promise<AIChatResponse> {
        return this.request<AIChatResponse>(
            "/api/v1/chat",
            {
                method: "POST",
                body: JSON.stringify(payload),
            }
        );
    }


    async ingestDocument(
        payload: AIIngestRequest
    ): Promise<AIIngestResponse> {
        return this.request<AIIngestResponse>(
            "/api/v1/documents/ingest",
            {
                method: "POST",
                body: JSON.stringify(payload),
            }
        );
    }


    async healthCheck(): Promise<boolean> {
        try {
            await this.request(
                "/api/v1/health",
                {
                    method: "GET",
                }
            );

            return true;
        } catch {
            return false;
        }
    }
}


export const aiService = new AIService();