import { z } from "zod";

export const departmentSchema = z.object({
    name: z
        .string()
        .trim()
        .min(2, "Department name is required")
        .max(50),

    description: z
        .string()
        .trim()
        .max(255)
        .optional(),
});

export type DepartmentFormData =
    z.infer<typeof departmentSchema>;