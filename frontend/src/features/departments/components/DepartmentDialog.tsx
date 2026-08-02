import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

import {
    departmentSchema,
    type DepartmentFormData,
} from "../schemas/department.schema";

import { useCreateDepartment } from "../hooks/useCreateDepartment";
import type { Department } from "../types/department";
import { useUpdateDepartment } from "../hooks/useUpdateDepartment";

interface Props {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    department?: Department | null;
}

export default function DepartmentDialog({
    open,
    onOpenChange,
    department,
}: Props) {
    const createDepartment = useCreateDepartment();
    const updateDepartment = useUpdateDepartment();

    const isEdit = Boolean(department);
    const isPending = createDepartment.isPending || updateDepartment.isPending;

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<DepartmentFormData>({
        resolver: zodResolver(departmentSchema),
    });

    useEffect(() => {
        if (department) {
            reset({
                name: department.name,
                description: department.description ?? "",
            });
        } else {
            reset({
                name: "",
                description: "",
            });
        }
    }, [department, reset, open]);

    function onSubmit(data: DepartmentFormData) {
        if (isEdit && department) {
            updateDepartment.mutate(
                { id: department.id, ...data },
                {
                    onSuccess() {
                        reset();
                        onOpenChange(false);
                    },
                }
            );
        } else {
            createDepartment.mutate(data, {
                onSuccess() {
                    reset();
                    onOpenChange(false);
                },
            });
        }
    }
    useEffect(() => {
        reset({
            name: department?.name ?? "",
            description:
                department?.description ?? "",
        });
    }, [department]);
    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>
                        {isEdit ? "Edit Department" : "Add Department"}
                    </DialogTitle>
                </DialogHeader>

                <form
                    onSubmit={handleSubmit(onSubmit)}
                    className="space-y-4"
                >
                    <div>
                        <Input
                            placeholder="Department Name"
                            {...register("name")}
                        />

                        {errors.name && (
                            <p className="text-sm text-red-500 mt-1">
                                {errors.name.message}
                            </p>
                        )}
                    </div>

                    <div>
                        <Textarea
                            placeholder="Description"
                            rows={4}
                            {...register("description")}
                        />
                    </div>

                    <DialogFooter>
                        <Button
                            variant="outline"
                            type="button"
                            onClick={() => onOpenChange(false)}
                        >
                            Cancel
                        </Button>

                        <Button
                            type="submit"
                            disabled={isPending}
                        >
                            {isPending
                                ? isEdit
                                    ? "Updating..."
                                    : "Creating..."
                                : isEdit
                                    ? "Save Changes"
                                    : "Create Department"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}