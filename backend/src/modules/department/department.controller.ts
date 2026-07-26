import { Request, Response } from "express";

import { createDepartmentSchema } from "./department.validation.js";
import { createDepartmentService } from "./department.service.js";
import { getDepartmentsService } from "./department.service.js";

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