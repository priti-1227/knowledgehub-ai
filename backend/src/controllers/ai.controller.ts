import type {
    Request,
    Response,
    NextFunction,
} from "express";

import { aiService } from "../services/ai/ai.service.js";
import { prisma } from "@/lib/prisma.js";


export const askKnowledgeHub = async (
    req: Request,
    res: Response,
    next: NextFunction,
) => {
    try {
        const {
            question,
            top_k,
            similarity_threshold,
        } = req.body;

        // ------------------------------------------------
        // 1. Validate question
        // ------------------------------------------------

        if (
            !question ||
            typeof question !== "string" ||
            !question.trim()
        ) {
            return res.status(400).json({
                success: false,
                message: "Question is required.",
            });
        }

        // ------------------------------------------------
        // 2. Make sure authenticated user exists
        // ------------------------------------------------

        if (!req.user) {
            return res.status(401).json({
                success: false,
                message: "Unauthorized.",
            });
        }

        // ------------------------------------------------
        // 3. Load trusted user information
        // ------------------------------------------------

        const user = await prisma.user.findUnique({
            where: {
                id: req.user.id,
            },

            select: {
                id: true,
                role: true,
                departmentId: true,
            },
        });

        if (!user) {
            return res.status(401).json({
                success: false,
                message: "User not found.",
            });
        }

        // ------------------------------------------------
        // 4. Resolve user's department
        // ------------------------------------------------

        let departmentName: string | null = null;

        if (user.departmentId) {
            const department =
                await prisma.department.findUnique({
                    where: {
                        id: user.departmentId,
                    },

                    select: {
                        name: true,
                    },
                });

            departmentName =
                department?.name ?? null;
        }

        // ------------------------------------------------
        // 5. Build trusted AI access context
        // ------------------------------------------------

        const isAdmin =
            user.role === "ADMIN";

        const roles = [
            user.role,
        ];

        console.log(
            "AI ACCESS CONTEXT:",
            {
                userId: user.id,
                role: user.role,
                department:
                    departmentName,
                isAdmin,
            },
        );

        // ------------------------------------------------
        // 6. Call AI service
        // ------------------------------------------------

        const result =
            await aiService.chat({

                question:
                    question.trim(),

                user_id:
                    user.id,

                department:
                    departmentName,

                roles,

                is_admin:
                    isAdmin,

                top_k:
                    top_k ?? 5,

                similarity_threshold:
                    similarity_threshold ?? 0.5,
            });

        // ------------------------------------------------
        // 7. Return response
        // ------------------------------------------------

        return res.status(200).json({
            success: true,
            data: result,
        });

    } catch (error) {
        next(error);
    }
};