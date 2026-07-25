import bcrypt from "bcrypt";
import { prisma } from "@/lib/prisma.js";
import type { RegisterInput } from "./auth.validation.js";

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
        throw new Error(
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