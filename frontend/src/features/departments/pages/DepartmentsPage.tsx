import { Plus } from "lucide-react";
import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { DataTable } from "@/components/shared/DataTable/DataTable";

import DepartmentDialog from "../components/DepartmentDialog";
import DeleteDepartmentDialog from "../components/DeleteDepartmentDialog";
import EmptyDepartment from "../components/EmptyDepartment";

import { useDepartments } from "../hooks/useDepartments";

import { departmentColumns } from "../column";

import type { Department } from "../types/department";

export default function DepartmentsPage() {
    const [dialogOpen, setDialogOpen] = useState(false);
    const [deleteOpen, setDeleteOpen] = useState(false);

    const [selectedDepartment, setSelectedDepartment] =
        useState<Department | null>(null);

    const { data, isLoading } = useDepartments();

    function handleAdd() {
        setSelectedDepartment(null);
        setDialogOpen(true);
    }

    function handleEdit(department: Department) {
        setSelectedDepartment(department);
        setDialogOpen(true);
    }

    function handleDelete(department: Department) {
        setSelectedDepartment(department);
        setDeleteOpen(true);
    }

    const columns = useMemo(
        () => departmentColumns(handleEdit, handleDelete),
        []
    );

    if (isLoading) {
        return (
            <div className="space-y-3">
                {Array.from({ length: 6 }).map((_, index) => (
                    <Skeleton
                        key={index}
                        className="h-12 w-full rounded-lg"
                    />
                ))}
            </div>
        );
    }

    const departments = data?.departments ?? [];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold">
                        Departments
                    </h1>

                    <p className="text-muted-foreground">
                        Manage organization departments.
                    </p>
                </div>

                <Button onClick={handleAdd}>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Department
                </Button>
            </div>

            {departments.length === 0 ? (
                <EmptyDepartment />
            ) : (
                <DataTable
                    columns={columns}
                    data={departments}
                    searchColumn="name"
                />
            )}

            <DepartmentDialog
                open={dialogOpen}
                onOpenChange={setDialogOpen}
                department={selectedDepartment}
            />

            <DeleteDepartmentDialog
                open={deleteOpen}
                onOpenChange={setDeleteOpen}
                department={selectedDepartment}
            />
        </div>
    );
}