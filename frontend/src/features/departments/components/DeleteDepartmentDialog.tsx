import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";

import type { Department } from "../types/department";
import { useDeleteDepartment } from "../hooks/useDeleteDepartment";

interface Props {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    department: Department | null;
}

export default function DeleteDepartmentDialog({
    open,
    onOpenChange,
    department,
}: Props) {
    const deleteDepartment = useDeleteDepartment();

    if (!department) return null;

    function handleDelete() {
        deleteDepartment.mutate(department.id, {
            onSuccess() {
                onOpenChange(false);
            },
        });
    }

    return (
        <AlertDialog open={open} onOpenChange={onOpenChange}>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>
                        Delete Department
                    </AlertDialogTitle>

                    <AlertDialogDescription>
                        Are you sure you want to delete{" "}
                        <strong>{department.name}</strong> ?
                        This action cannot be undone.
                    </AlertDialogDescription>
                </AlertDialogHeader>

                <AlertDialogFooter>
                    <AlertDialogCancel>
                        Cancel
                    </AlertDialogCancel>

                    <AlertDialogAction
                        onClick={handleDelete}
                        className="bg-red-600 hover:bg-red-700"
                    >
                        Delete
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
}