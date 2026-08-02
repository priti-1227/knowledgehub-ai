import { Request, Response } from "express";

import { createDepartmentSchema } from "./department.validation.js";
import {
    createDepartmentService,
    getDepartmentsService,
    updateDepartmentService,
    deleteDepartmentService,
} from "./department.service.js";

export async function createDepartment(
    req: Request,
    res: Response
) {
    const validatedData =
        createDepartmentSchema.parse(req.body);

    const department =
        await createDepartmentService(validatedData);

    return res.status(201).json({
        success: true,
        message: "Department created successfully.",
        department,
    });
}
export async function getDepartments(
    req: Request,
    res: Response
) {

    const departments =
        await getDepartmentsService();

    return res.json({

        success: true,

        departments,

    });

}
export async function updateDepartmentController(
    req: Request<{ id: string }>,
    res: Response
) {
    const department =
        await updateDepartmentService(
            req.params.id,
            req.body
        );

    res.json({
        success: true,
        department,
    });
}

export async function deleteDepartmentController(
    req: Request<{ id: string }>,
    res: Response
) {
    await deleteDepartmentService(req.params.id);

    res.json({
        success: true,
        message: "Department deleted successfully.",
    });
}