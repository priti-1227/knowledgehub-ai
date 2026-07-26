import { z } from "zod";

export const createDepartmentSchema = z.object({
    name: z
        .string()
        .trim()
        .min(2, "Department name must be at least 2 characters")
        .max(50, "Department name cannot exceed 50 characters"),

    description: z
        .string()
        .trim()
        .max(255, "Description cannot exceed 255 characters")
        .optional()
        .or(z.literal("")),
});

export type CreateDepartmentInput = z.infer<
    typeof createDepartmentSchema
>;