import { Request, Response } from "express";

import {
    uploadDocumentSchema,
} from "./document.validation.js";

import {
    uploadDocumentService,
} from "./document.service.js";

export async function uploadDocument(
    req: Request,
    res: Response
) {

    if (!req.file) {
        return res.status(400).json({
            success: false,
            message: "PDF file is required",
        });
    }

    const validated =
        uploadDocumentSchema.parse(req.body);

    // JWT middleware should attach the user
    const user = req.user as any;

    const document =
        await uploadDocumentService({

            ...validated,

            uploadedById: user.id,

            file: req.file,

        });

    return res.status(201).json({

        success: true,

        message: "Document uploaded successfully.",

        document,

    });

}