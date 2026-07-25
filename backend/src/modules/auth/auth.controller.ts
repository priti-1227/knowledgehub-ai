import type {
    Request,
    Response,
} from "express";

import { asyncHandler } from "@/utils/asyncHandler.js";
import { loginSchema, registerSchema } from "./auth.validation.js";
import { loginUser, registerUser } from "./auth.service.js";

export const register =
    asyncHandler(async (req: Request, res: Response) => {

        const data =
            registerSchema.parse(req.body);

        const user =
            await registerUser(data);

        res.status(201).json({
            success: true,
            user,
        });

    });

export const login =
    asyncHandler(async (req: Request, res: Response) => {

        const data = loginSchema.parse(req.body);

        const result =
            await loginUser(data);

        res.status(200).json({
            success: true,
            user: result.user,
            token: result.token,
        });

    });
