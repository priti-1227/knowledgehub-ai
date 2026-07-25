import { z } from "zod";

export const registerSchema = z
    .object({
        fullName: z.string().min(3),
        email: z.email(),
        password: z.string().min(8),
        confirmPassword: z.string(),
    })
    .refine(
        (data) => data.password === data.confirmPassword,
        {
            path: ["confirmPassword"],
            message: "Passwords do not match",
        }
    );

export type RegisterInput = z.infer<
    typeof registerSchema
>;