import { prisma } from "@/lib/prisma.js";
import type { UploadDocumentDTO } from "./document.types.js";

export async function createDocument(data: UploadDocumentDTO) {
    return prisma.document.create({
        data: {
            title: data.title,

            originalName: data.file.originalname,
            fileName: data.file.filename,
            filePath: data.file.path,

            mimeType: data.file.mimetype,
            fileSize: data.file.size,

            departmentId: data.departmentId,
            uploadedById: data.uploadedById,
        },
    });
}

export async function getAllDocuments() {
    return prisma.document.findMany({
        include: {
            department: {
                select: {
                    id: true,
                    name: true,
                },
            },
            uploadedBy: {
                select: {
                    id: true,
                    fullName: true,
                    email: true,
                },
            },
        },
        orderBy: {
            createdAt: "desc",
        },
    });
}

export async function getDocumentById(id: string) {
    return prisma.document.findUnique({
        where: { id },
        include: {
            department: true,
            uploadedBy: true,
        },
    });
}

export async function deleteDocument(id: string) {
    return prisma.document.delete({
        where: {
            id,
        },
    });
}