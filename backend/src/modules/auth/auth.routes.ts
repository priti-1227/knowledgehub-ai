import { Router } from "express";
import { register } from "./auth.controller.js";
import { login } from "./auth.controller.js";

const router = Router();
/**
 * @swagger
 * /api/auth/login:
 *   post:
 *     summary: Login user
 *     tags:
 *       - Authentication
 *
 *     requestBody:
 *       required: true
 *
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *
 *             required:
 *               - email
 *               - password
 *
 *             properties:
 *
 *               email:
 *                 type: string
 *                 example: admin@knowledgehub.com
 *
 *               password:
 *                 type: string
 *                 example: Password@123
 *
 *     responses:
 *
 *       200:
 *         description: Login successful
 *
 *       401:
 *         description: Invalid credentials
 */

router.post("/login", login);
/**
 * @swagger
 * /api/auth/register:
 *   post:
 *     summary: Register a new user
 *     tags:
 *       - Authentication
 *
 *     requestBody:
 *       required: true
 *
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *
 *             required:
 *               - fullName
 *               - email
 *               - password
 *
 *             properties:
 *
 *               fullName:
 *                 type: string
 *                 example: Priti Rathore
 *
 *               email:
 *                 type: string
 *                 example: priti@gmail.com
 *
 *               password:
 *                 type: string
 *                 example: Password@123
 *
 *               role:
 *                 type: string
 *                 example: ADMIN
 *
 *     responses:
 *
 *       201:
 *         description: User registered successfully
 *
 *       400:
 *         description: Validation failed
 *
 *       409:
 *         description: User already exists
 */
router.post("/register", register);
export default router;