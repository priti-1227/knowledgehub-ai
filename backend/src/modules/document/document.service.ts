import { prisma } from "../../lib/prisma.js";
import { UploadDocumentDTO } from "./document.types.js";

export async function uploadDocumentService(data: UploadDocumentDTO) {
    const { title, departmentId, uploadedById, file } = data;

    const document = await prisma.document.create({
        data: {
            title,
            originalName: file.originalname,
            fileName: file.filename,
            filePath: file.path,
            mimeType: file.mimetype,
            fileSize: file.size,
            departmentId,
            uploadedById,
        },
    });

    return document;
}
