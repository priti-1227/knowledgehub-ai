import jwt from "jsonwebtoken";

export interface JwtPayload {
    id: string;
    email: string;
    role: string;
}

export function generateToken(payload: JwtPayload): string {
    return jwt.sign(
        payload,
        process.env.JWT_SECRET! as string,
        {
            expiresIn: process.env.JWT_EXPIRES_IN as string,
        } as any
    );
}

export function verifyToken(token: string): JwtPayload {
    return jwt.verify(
        token,
        process.env.JWT_SECRET! as string
    ) as JwtPayload;
}