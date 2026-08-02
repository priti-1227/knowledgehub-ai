import multer from "multer";
import path from "path";
import fs from "fs";

const uploadPath = "uploads";

if (!fs.existsSync(uploadPath)) {
    fs.mkdirSync(uploadPath, { recursive: true });
}

const storage = multer.diskStorage({
    destination(_, __, cb) {
        cb(null, uploadPath);
    },

    filename(_, file, cb) {
        const unique =
            Date.now() +
            "-" +
            Math.round(Math.random() * 1e9);

        cb(
            null,
            unique + path.extname(file.originalname)
        );
    },
});

export const upload = multer({
    storage,

    limits: {
        fileSize: 20 * 1024 * 1024, //20MB
    },

    fileFilter(_, file, cb) {
        const allowed = [
            "application/pdf",

            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

            "text/plain",
        ];

        if (allowed.includes(file.mimetype)) {
            return cb(null, true);
        }

        cb(new Error("Unsupported file"));
    },
});