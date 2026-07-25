export interface UploadDocumentDTO {
    title: string;
    departmentId: string;
    uploadedById: string;
    file: Express.Multer.File;
}