import { Router } from "express";
import { upload } from "@/config/multer.js";
import { deleteDocumentController, downloadDocumentController, getDocumentController, getDocumentsController, uploadDocumentController, viewDocumentController } from "./document.controller.js";
import { authenticate } from "@/middleware/authenticate.js";
import { authorize } from "@/middleware/authorize.js";

const router = Router();

/**
 * @swagger
 * /api/documents/upload:
 *   post:
 *     summary: Upload a new document
 *     tags:
 *       - Documents
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         multipart/form-data:
 *           schema:
 *             type: object
 *             required:
 *               - file
 *               - title
 *               - departmentId
 *             properties:
 *               file:
 *                 type: string
 *                 format: binary
 *                 description: Document file (PDF, DOCX, TXT)
 *               title:
 *                 type: string
 *                 description: Document title
 *                 example: Employee Handbook 2026
 *               departmentId:
 *                 type: string
 *                 description: Department ID
 *                 example: cm123abc456def
 *     responses:
 *       201:
 *         description: Document uploaded successfully
 *       400:
 *         description: Bad request (Missing file, title, or departmentId)
 *       401:
 *         description: Unauthorized
 *       403:
 *         description: Forbidden (Only Admin can upload documents)
 */
router.post(
    "/upload",
    authenticate,
    authorize("ADMIN"),
    upload.single("file"),
    uploadDocumentController
);
/**
 * @swagger
 * /api/documents/upload:
 *   post:
 *     summary: Upload a new document
 *     tags:
 *       - Documents
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         multipart/form-data:
 *           schema:
 *             type: object
 *             required:
 *               - file
 *               - title
 *               - departmentId
 *             properties:
 *               file:
 *                 type: string
 *                 format: binary
 *                 description: Document file (PDF, DOCX, TXT)
 *               title:
 *                 type: string
 *                 description: Document title
 *                 example: Employee Handbook 2026
 *               departmentId:
 *                 type: string
 *                 description: Department ID
 *                 example: cm123abc456def
 *     responses:
 *       201:
 *         description: Document uploaded successfully
 *       400:
 *         description: Bad request (Missing file, title, or departmentId)
 *       401:
 *         description: Unauthorized
 *       403:
 *         description: Forbidden (Only Admin can upload documents)
 */
router.get(
    "/",
    authenticate,
    getDocumentsController
);
/**
 * @swagger
 * /api/documents/{id}:
 *   get:
 *     summary: Get document by ID
 *     tags:
 *       - Documents
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Document ID
 *         example: cm123abc456def
 *     responses:
 *       200:
 *         description: Document found
 *       401:
 *         description: Unauthorized
 *       404:
 *         description: Document not found
 */
router.get(
    "/:id",
    authenticate,
    getDocumentController
);

/**
 * @swagger
 * /api/documents/{id}:
 *   delete:
 *     summary: Delete document by ID
 *     tags:
 *       - Documents
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Document ID
 *         example: cm123abc456def
 *     responses:
 *       200:
 *         description: Document deleted successfully
 *       401:
 *         description: Unauthorized
 *       404:
 *         description: Document not found
 *       403:
 *         description: Forbidden (Only Admin can delete documents)
 */
router.delete(
    "/:id",
    authenticate,
    authorize("ADMIN"),
    deleteDocumentController
);
/**
 * @swagger
 * /api/documents/{id}/view:
 *   get:
 *     summary: View document content
 *     tags:
 *       - Documents
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Document ID
 *         example: cm123abc456def
 *     responses:
 *       200:
 *         description: Document content returned successfully
 *       401:
 *         description: Unauthorized
 *       404:
 *         description: Document not found
 */
router.get(
    "/:id/view",
    authenticate,
    viewDocumentController
);
/**
 * @swagger
 * /api/documents/{id}/download:
 *   get:
 *     summary: Download document
 *     tags:
 *       - Documents
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Document ID
 *         example: cm123abc456def
 *     responses:
 *       200:
 *         description: Document downloaded successfully
 *       401:
 *         description: Unauthorized
 *       404:
 *         description: Document not found
 */
router.get(
    "/:id/download",
    authenticate,
    downloadDocumentController
);

export default router;