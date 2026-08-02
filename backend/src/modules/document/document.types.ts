import type { Request } from "express";

export interface UploadDocumentDTO {
    title: string;
    departmentId: string;
    uploadedById: string;
    file: Express.Multer.File;
}

export interface UploadDocumentRequest extends Request {
    file: Express.Multer.File;
}