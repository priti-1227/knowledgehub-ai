import path from "path";
import { prisma } from "../../lib/prisma.js";
import { aiService } from "./ai.service.js";


export class AIIndexingService {
    async indexDocument(
        documentId: string
    ) {
        const document =
            await prisma.document.findUnique({
                where: {
                    id: documentId,
                },
                include: {
                    department: true,
                },
            });

        if (!document) {
            throw new Error(
                `Document not found: ${documentId}`
            );
        }
        const MAX_RETRIES = 5;

        if (document.aiIndexStatus === "AI_PROCESSING") {
            throw new Error(
                "Document is already being indexed."
            );
        }

        if (document.aiIndexStatus === "AI_READY") {
            return {
                status: "already_ready",
            };
        }

        if (document.aiRetryCount >= MAX_RETRIES) {
            throw new Error(
                "Maximum AI indexing retries exceeded."
            );
        }

        // -----------------------------------------
        // Mark PROCESSING
        // -----------------------------------------

        await prisma.document.update({
            where: {
                id: documentId,
            },

            data: {
                aiIndexStatus: "AI_PROCESSING",
                aiIndexError: null,
            },
        });

        try {
            // Ensure absolute file path so external AI service can read the file correctly
            const absoluteFilePath = path.isAbsolute(document.filePath)
                ? document.filePath
                : path.resolve(process.cwd(), document.filePath);

            const result =
                await aiService.ingestDocument({
                    file_path: absoluteFilePath,
                    document_name: document.title,
                    department:
                        document.department?.name ?? null,
                });

            // ---------------------------------------
            // Mark READY & set isProcessed
            // ---------------------------------------

            await prisma.document.update({
                where: {
                    id: documentId,
                },

                data: {
                    aiIndexStatus: "AI_READY",

                    aiIndexedAt: new Date(),

                    aiIndexError: null,

                    isProcessed: true,
                },
            });

            return result;
        } catch (error) {
            const message =
                error instanceof Error
                    ? error.message
                    : "Unknown AI indexing error";

            console.error(
                `AI Indexing failed for document ID [${documentId}]:`,
                error
            );

            // ---------------------------------------
            // Mark FAILED
            // ---------------------------------------

            await prisma.document.update({
                where: {
                    id: documentId,
                },

                data: {
                    aiIndexStatus: "AI_FAILED",

                    aiIndexError: message,

                    isProcessed: false,

                    aiRetryCount: {
                        increment: 1,
                    },
                },
            });

            throw error;
        }
    }
}


export const aiIndexingService =
    new AIIndexingService();