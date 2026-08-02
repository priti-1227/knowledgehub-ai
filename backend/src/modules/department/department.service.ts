import { prisma } from "@/lib/prisma.js";
import { ApiError } from "@/utils/ApiError.js";

import type { CreateDepartmentDTO, UpdateDepartmentDTO } from "./department.types.js";

export async function createDepartmentService(
    data: CreateDepartmentDTO
) {
    const existingDepartment =
        await prisma.department.findUnique({
            where: {
                name: data.name,
            },
        });

    if (existingDepartment) {
        throw new ApiError(
            409,
            "Department already exists."
        );
    }

    const department =
        await prisma.department.create({
            data: {
                name: data.name,
                description: data.description || null,
            },
        });

    return department;
}
export async function getDepartmentsService() {

    return prisma.department.findMany({

        orderBy: {

            name: "asc",

        },

    });

}

export async function updateDepartmentService(
    id: string,
    data: UpdateDepartmentDTO
) {
    return prisma.department.update({
        where: {
            id,
        },
        data: {
            name: data.name,
            description: data.description,
        },
    });
}

export async function deleteDepartmentService(id: string) {
    return prisma.department.delete({
        where: {
            id,
        },
    });
}