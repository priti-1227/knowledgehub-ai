import { Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";

import type { Department } from "../types/department";

interface Props {
    department: Department;
    onEdit: (department: Department) => void;
    onDelete: (department: Department) => void;
}

export default function DepartmentActions({
    department,
    onEdit,
    onDelete,
}: Props) {
    return (
        <div className="flex gap-2">
            <Button
                size="icon"
                variant="ghost"
                onClick={() => onEdit(department)}
            >
                <Pencil className="h-4 w-4" />
            </Button>

            <Button
                size="icon"
                variant="ghost"
                className="text-red-600"
                onClick={() => onDelete(department)}
            >
                <Trash2 className="h-4 w-4" />
            </Button>
        </div>
    );
}