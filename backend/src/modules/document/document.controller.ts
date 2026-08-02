import { Request, Response } from "express";
import path from "path";
import { deleteDocumentService, getDocumentService, getDocumentsService, uploadDocumentService } from "./document.service.js";

export async function uploadDocumentController(
    req: Request,
    res: Response
) {
    const document =
        await uploadDocumentService({
            title: req.body.title,
            departmentId: req.body.departmentId,
            uploadedById: req.user!.id,
            file: req.file!,
        });

    res.status(201).json({
        success: true,
        message: "Document uploaded successfully",
        document,
    });
}
export async function getDocumentsController(
    req: Request,
    res: Response
) {
    const documents = await getDocumentsService();

    res.json({
        success: true,
        documents,
    });
}

export async function getDocumentController(
    req: Request,
    res: Response
) {
    const id = req.params.id as string;
    const document = await getDocumentService(id);

    res.json({
        success: true,
        document,
    });
}

export async function deleteDocumentController(
    req: Request,
    res: Response
) {
    const id = req.params.id as string;
    await deleteDocumentService(id);

    res.json({
        success: true,
        message: "Document deleted successfully",
    });
}
export async function viewDocumentController(
    req: Request,
    res: Response
) {
    const id = req.params.id as string;
    const document = await getDocumentService(id);

    res.sendFile(path.resolve(document.filePath));
}
export async function downloadDocumentController(
    req: Request,
    res: Response
) {
    const id = req.params.id as string;
    const document = await getDocumentService(id);

    res.download(
        path.resolve(document.filePath),
        document.originalName
    );
}