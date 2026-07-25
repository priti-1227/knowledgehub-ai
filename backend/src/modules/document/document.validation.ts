import { z } from "zod";

export const uploadDocumentSchema = z.object({
    title: z
        .string()
        .min(3, "Title must be at least 3 characters"),

    departmentId: z
        .string()
        .min(1, "Department is required"),
});

export type UploadDocumentInput =
    z.infer<typeof uploadDocumentSchema>;