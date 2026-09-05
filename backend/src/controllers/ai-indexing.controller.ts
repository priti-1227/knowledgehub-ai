import { aiIndexingService } from "../services/ai/ai-indexing.service.js";
import {
    Request,
    Response,
    NextFunction,
} from "express";

import { prisma } from "../lib/prisma.js";

export const getAIIndexStatus = async (
    req: Request,
    res: Response,
    next: NextFunction
) => {
    try {
        const { documentId } = req.params;

        if (!documentId || typeof documentId !== "string") {
            return res.status(400).json({
                success: false,
                message: "Invalid document ID.",
            });
        }

        const document = await prisma.document.findUnique({
            where: {
                id: documentId,
            },

            select: {
                id: true,
                aiIndexStatus: true,
                aiIndexError: true,
                aiIndexedAt: true,
                aiRetryCount: true,
            },
        });

        if (!document) {
            return res.status(404).json({
                success: false,
                message: "Document not found.",
            });
        }

        return res.status(200).json({
            success: true,
            data: document,
        });
    } catch (error) {
        next(error);
    }
};
export const retryAIIndexing = async (
    req: Request,
    res: Response,
    next: NextFunction
) => {
    try {
        const { documentId } = req.params;

        if (!documentId || typeof documentId !== "string") {
            return res.status(400).json({
                success: false,
                message: "Invalid document ID.",
            });
        }

        const result =
            await aiIndexingService.indexDocument(
                documentId
            );

        return res.status(200).json({
            success: true,
            message:
                "AI indexing completed successfully.",
            data: result,
        });
    } catch (error) {
        next(error);
    }
};