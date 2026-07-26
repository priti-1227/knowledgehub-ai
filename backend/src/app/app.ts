import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import authRoutes from "@/modules/auth/auth.routes.js";
import { errorMiddleware } from "@/middleware/error.middleware.js";
import documentRoutes from "@/modules/document/document.routes.js";
import departmentRoutes from "@/modules/department/department.routes.js";
import { setupSwagger } from "@/config/swagger.js";


const app = express();

app.use(cors());
app.use(helmet());
app.use(morgan("dev"));
app.use(express.json());

app.get("/api/health", (_, res) => {
    res.json({
        success: true,
        message: "KnowledgeHub API is running 🚀",
    });
});
app.use("/api/auth", authRoutes);
app.use("/api/documents", documentRoutes);
app.use("/api/departments", departmentRoutes);
app.use(errorMiddleware);
setupSwagger(app);
export default app;