import jwt from "jsonwebtoken";

interface JwtPayload {
    id: string;
    email: string;
    role: string;
}

export function generateToken(
    payload: JwtPayload
) {
    return jwt.sign(
        payload,
        process.env.JWT_SECRET! as string,
        {
            expiresIn: process.env.JWT_EXPIRES_IN as string,
        } as any
    );
}