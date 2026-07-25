import { Request, Response, NextFunction } from "express";
import { JwtPayload, verifyToken } from "@/utils/jwt.js";
import { ApiError } from "@/utils/ApiError.js";

export function authenticate(
    req: Request,
    res: Response,
    next: NextFunction
) {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        throw new ApiError(401, "Authentication token is required");
    }

    const token = authHeader.split(" ")[1];

    try {
        const decoded = verifyToken(token) as JwtPayload;
        req.user = decoded;
        next();
    } catch (error) {
        throw new ApiError(401, "Invalid or expired token");
    }
}
