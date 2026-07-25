import { Router } from "express";
import { upload } from "../../config/multer.js";
import { uploadDocument } from "./document.controller.js";
import { authenticate } from "../../middleware/authenticate.js";
import { authorize } from "../../middleware/authorize.js";

const router = Router();

router.post(
    "/upload",
    authenticate,
    authorize("ADMIN"),
    upload.single("document"),
    uploadDocument
);

export default router;