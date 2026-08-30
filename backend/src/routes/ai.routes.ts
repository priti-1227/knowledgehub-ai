import { Router } from "express";

import {
    askKnowledgeHub,
} from "../controllers/ai.controller.js";


// Replace this with your actual auth middleware.
import {
    authenticate,
} from "../middleware/auth.middleware.js";


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


export default router;