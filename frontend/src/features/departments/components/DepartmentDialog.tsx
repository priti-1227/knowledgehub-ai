import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
    departmentSchema,
    type DepartmentFormData,
} from "../schemas/department.schema";

import { useCreateDepartment } from "../hooks/useCreateDepartment";

interface Props {
    onClose: () => void;
}

export default function DepartmentDialog({

    onClose,

}: Props) {

    const mutation =
        useCreateDepartment();

    const {

        register,

        handleSubmit,

        formState: { errors },

    } = useForm<DepartmentFormData>({

        resolver:
            zodResolver(departmentSchema),

    });

    function onSubmit(
        data: DepartmentFormData
    ) {

        mutation.mutate(data, {

            onSuccess() {

                onClose();

            },

        });

    }

    return (

        <div>

            {/* Dialog UI */}test

            {/* We'll improve UI in next sprint */}

        </div>

    );

}