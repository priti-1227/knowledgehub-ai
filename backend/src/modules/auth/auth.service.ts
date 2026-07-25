import bcrypt from "bcrypt";
import { prisma } from "@/lib/prisma.js";
import type { LoginInput, RegisterInput } from "./auth.validation.js";
import { ApiError } from "@/utils/ApiError.js";
import { generateToken } from "@/utils/jwt.js";

export async function registerUser(
    data: RegisterInput
) {
    const existingUser =
        await prisma.user.findUnique({
            where: {
                email: data.email,
            },
        });

    if (existingUser) {
        throw new ApiError(
            409,
            "Email already registered."
        );
    }

    const hashedPassword =
        await bcrypt.hash(data.password, 10);

    const user = await prisma.user.create({
        data: {
            fullName: data.fullName,
            email: data.email,
            password: hashedPassword,
        },
    });

    return user;
}
export async function loginUser(
    data: LoginInput
) {
    const user =
        await prisma.user.findUnique({
            where: {
                email: data.email
            }
        });
    if (!user) {
        throw new ApiError(
            401,
            "Invalid credentials"
        );
    }
    const isPasswordValid =
        await bcrypt.compare(
            data.password,
            user.password
        );
    if (!isPasswordValid) {
        throw new ApiError(
            401,
            "Invalid credentials"
        );
    }
    const token = generateToken({
        id: user.id,
        email: user.email,
        role: user.role,
    });
    return {
        user,
        token,
    };
}