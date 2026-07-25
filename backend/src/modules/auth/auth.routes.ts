import { Router } from "express";
import { register } from "./auth.controller.js";
import { login } from "./auth.controller.js";

const router = Router();

router.post(
    "/register",
    register
);
router.post("/login", login);


export default router;