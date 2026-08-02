import { ApiError } from "@/utils/ApiError.js";
import fs from "fs/promises";

import { createDocument, getAllDocuments, getDocumentById, deleteDocument } from "./document.repository.js";
import type { UploadDocumentDTO } from "./document.types.js";

export async function uploadDocumentService(
    data: UploadDocumentDTO
) {
    if (!data.file) {
        throw new ApiError(400, "File is required");
    }

    if (!data.title) {
        throw new ApiError(400, "Title is required");
    }

    if (!data.departmentId) {
        throw new ApiError(
            400,
            "Department is required"
        );
    }

    return createDocument(data);
}

export async function getDocumentsService() {
    return getAllDocuments();
}

export async function getDocumentService(id: string) {
    const document = await getDocumentById(id);

    if (!document) {
        throw new ApiError(404, "Document not found");
    }

    return document;
}

export async function deleteDocumentService(id: string) {
    const document = await getDocumentById(id);

    if (!document) {
        throw new ApiError(404, "Document not found");
    }

    try {
        await fs.unlink(document.filePath);
    } catch {
        // Ignore if file doesn't exist
    }

    return deleteDocument(id);
}