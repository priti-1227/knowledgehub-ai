export interface Department {
    id: string;
    name: string;
}

export interface UploadedBy {
    id: string;
    fullName: string;
    email: string;
}

export interface Document {
    id: string;
    title: string;

    originalName: string;
    fileName: string;
    filePath: string;

    mimeType: string;
    fileSize: number;

    version: number;
    isProcessed: boolean;

    createdAt: string;

    department: Department;
    uploadedBy: UploadedBy;
}

export interface DocumentsResponse {
    success: boolean;
    documents: Document[];
}