import {
    Request,
    Response,
    NextFunction,
} from "express";

import { aiService } from "../services/ai/ai.service.js";


export const askKnowledgeHub = async (
    req: Request,
    res: Response,
    next: NextFunction
) => {
    try {
        const {
            question,
            top_k,
            similarity_threshold,
        } = req.body;

        /*
         * IMPORTANT:
         *
         * In production these values should come
         * from your authenticated backend user,
         * NOT from req.body.
         */

        const user = (req as any).user;

        const result = await aiService.chat({
            question,

            user_id: user.id,

            department:
                user.department ?? null,

            roles:
                user.roles ?? [],

            is_admin:
                user.isAdmin ?? false,

            top_k:
                top_k ?? 5,

            similarity_threshold:
                similarity_threshold ?? 0.5,
        });

        return res.status(200).json({
            success: true,
            data: result,
        });
    } catch (error) {
        next(error);
    }
};