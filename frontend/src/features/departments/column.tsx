import type { ColumnDef } from "@tanstack/react-table";
import type { Department } from "./types/department";

import DepartmentActions from "./components/DepartmentActions";

export function departmentColumns(
    onEdit: (department: Department) => void,
    onDelete: (department: Department) => void
): ColumnDef<Department>[] {
    return [
        {
            accessorKey: "name",
            header: "Department",
        },
        {
            accessorKey: "description",
            header: "Description",
            cell: ({ row }) =>
                row.original.description ?? "-",
        },
        {
            accessorKey: "createdAt",
            header: "Created",
            cell: ({ row }) =>
                new Date(
                    row.original.createdAt
                ).toLocaleDateString(),
        },
        {
            id: "actions",
            header: "",
            cell: ({ row }) => (
                <DepartmentActions
                    department={row.original}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ),
        },
    ];
}