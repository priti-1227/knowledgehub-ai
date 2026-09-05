import { Router } from "express";

import {
    askKnowledgeHub,
} from "../controllers/ai.controller.js";


// Replace this with your actual auth middleware.
import {
    authenticate,
} from "../middleware/auth.middleware.js";

import {
    getAIIndexStatus,
    retryAIIndexing,
} from "../controllers/ai-indexing.controller.js";

const router = Router();

/**
 * @swagger
 * /api/v1/chat:
 *   post:
 *     summary: Ask a question to KnowledgeHub.
 *     description: Sends a question to the RAG system for answering.
 *     tags:
 *       - AI
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: "#/components/schemas/ChatRequest"
 *     responses:
 *       200:
 *         description: Successful response containing the answer.
 *         content:
 *           application/json:
 *             schema:
 *               $ref: "#/components/schemas/ChatResponse"
 *       400:
 *         description: Invalid request.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error: { type: string }
 *       401:
 *         description: Unauthorized.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error: { type: string }
 *       500:
 *         description: Internal server error.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error: { type: string }
 */
router.post(
    "/chat",
    authenticate,
    askKnowledgeHub
);
/**
 * @swagger
 * /api/v1/documents/{documentId}/ai-status:
 *   get:
 *     summary: Get AI indexing status for a document.
 *     description: Retrieves the current AI indexing status of a specific document, including status, error messages, and retry counts.
 *     tags:
 *       - AI / Indexing
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: documentId
 *         schema:
 *           type: string
 *           format: uuid
 *         required: true
 *         description: The ID of the document to check.
 *     responses:
 *       200:
 *         description: AI indexing status retrieved successfully.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success: { type: boolean }
 *                 data: 
 *                   type: object
 *                   properties:
 *                     id: { type: string, format: uuid }
 *                     aiIndexStatus: { type: string, enum: ["NOT_STARTED", "AI_PROCESSING", "AI_READY", "AI_FAILED"] }
 *                     aiIndexError: { type: [string, null] }
 *                     aiIndexedAt: { type: [string, null], format: date-time }
 *                     aiRetryCount: { type: number }
 *       400:
 *         description: Invalid document ID format.
 *       404:
 *         description: Document not found.
 *       500:
 *         description: Internal server error.
 */
router.get(
    "/documents/:documentId/ai-status",
    authenticate,
    getAIIndexStatus
);

/**
 * @swagger
 * /api/v1/documents/{documentId}/retry-ai-indexing:
 *   post:
 *     summary: Retry AI indexing for a document.
 *     description: Manually triggers AI indexing for a document that previously failed or needs to be re-indexed. Automatically increments retry count.
 *     tags:
 *       - AI / Indexing
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: documentId
 *         schema:
 *           type: string
 *           format: uuid
 *         required: true
 *         description: The ID of the document to retry indexing for.
 *     responses:
 *       200:
 *         description: AI indexing completed successfully.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success: { type: boolean }
 *                 message: { type: string }
 *                 data: { type: object }
 *       400:
 *         description: Invalid document ID format or document already being indexed.
 *       404:
 *         description: Document not found.
 *       500:
 *         description: Internal server error.
 */
router.post(
    "/documents/:documentId/retry-ai-indexing",
    authenticate,
    retryAIIndexing
);


export default router;