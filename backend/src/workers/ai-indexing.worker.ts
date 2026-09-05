import {
    Job,
    Worker,
} from "bullmq";

import {
    AI_INDEXING_QUEUE,
} from "../queues/ai-indexing.queue.js";

import {
    redisConnection,
} from "../config/redis.js";

import {
    aiIndexingService,
} from "../services/ai/ai-indexing.service.js";


interface AIIndexingJob {
    documentId: string;
}


export const aiIndexingWorker =
    new Worker<AIIndexingJob>(
        AI_INDEXING_QUEUE,

        async (
            job: Job<AIIndexingJob>
        ) => {
            const {
                documentId,
            } = job.data;

            console.log(
                `Starting AI indexing job ${job.id} for document ${documentId}`
            );

            const result =
                await aiIndexingService.indexDocument(
                    documentId
                );

            console.log(
                `AI indexing completed for document ${documentId}`
            );

            return result;
        },

        {
            connection: redisConnection,

            concurrency: 2,
        }
    );


aiIndexingWorker.on(
    "completed",
    (job) => {
        console.log(
            `AI indexing job ${job.id} completed`
        );
    }
);


aiIndexingWorker.on(
    "failed",
    (job, error) => {
        console.error(
            `AI indexing job ${job?.id} failed:`,
            error.message
        );
    }
);