import { Router } from "express";
import { createDepartment, getDepartments } from "./department.controller.js";
import { authorize } from "@/middleware/authorize.js";
import { authenticate } from "@/middleware/authenticate.js";

/**
 * @swagger
 * /api/departments:
 *   post:
 *     summary: Create a new department
 *     tags:
 *       - Departments
 *
 *     security:
 *       - bearerAuth: []
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
 *               - name
 *
 *             properties:
 *
 *               name:
 *                 type: string
 *                 example: Warehouse
 *
 *               description:
 *                 type: string
 *                 example: Warehouse Operations Department
 *
 *     responses:
 *
 *       201:
 *         description: Department created successfully
 *
 *       401:
 *         description: Unauthorized
 *
 *       403:
 *         description: Only Admin can create departments
 */

const router = Router();

router.post(
    "/",
    authenticate,
    authorize("ADMIN"),
    createDepartment
);

/**
 * @swagger
 * /api/departments:
 *   get:
 *     summary: Get all departments
 *     tags:
 *       - Departments
 *
 *     security:
 *       - bearerAuth: []
 *
 *     responses:
 *
 *       200:
 *         description: List of departments
 *
 *       401:
 *         description: Unauthorized
 */
router.get(

    "/",

    authenticate,

    getDepartments

);

export default router;