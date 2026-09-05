import { Queue } from "bullmq";

import { redisConnection } from "../config/redis.js";


export const AI_INDEXING_QUEUE =
    "ai-document-indexing";


export const aiIndexingQueue =
    new Queue(
        AI_INDEXING_QUEUE,
        {
            connection: redisConnection,

            defaultJobOptions: {
                attempts: 5,

                backoff: {
                    type: "exponential",
                    delay: 2000,
                },

                removeOnComplete: 100,

                removeOnFail: 500,
            },
        }
    );
export async function queueDocumentForIndexing(
    documentId: string
) {
    return aiIndexingQueue.add(
        "index-document",

        {
            documentId,
        },

        {
            jobId: `document-${documentId}`,
        }
    );
}