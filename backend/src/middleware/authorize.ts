import { Request, Response, NextFunction } from "express";
import { ApiError } from "@/utils/ApiError.js";
import { Role } from "@prisma/client";

export function authorize(...allowedRoles: Role[]) {
    return (req: Request, res: Response, next: NextFunction) => {
        if (!req.user) {
            throw new ApiError(401, "Unauthorized");
        }

        if (!allowedRoles.includes(req.user.role as Role)) {
            throw new ApiError(
                403,
                "Access denied. You do not have permission to access this resource."
            );
        }

        next();
    };
}
