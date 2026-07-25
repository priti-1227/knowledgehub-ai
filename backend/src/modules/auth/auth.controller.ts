import type {
    Request,
    Response,
} from "express";

import { registerSchema } from "./auth.validation.js";
import { registerUser } from "./auth.service.js";

export async function register(
    req: Request,
    res: Response
) {
    try {
        const data =
            registerSchema.parse(req.body);

        const user =
            await registerUser(data);

        res.status(201).json({
            success: true,
            user,
        });
    } catch (error: any) {
        res.status(400).json({
            success: false,
            message: error.message,
        });
    }
}