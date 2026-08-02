import { useMutation, useQueryClient } from "@tanstack/react-query";

import { toast } from "sonner";

import { departmentApi } from "../api/department.api";

export function useDeleteDepartment() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: departmentApi.delete,

        onSuccess() {

            toast.success("Department deleted");

            queryClient.invalidateQueries({

                queryKey: ["departments"],

            });

        },

    });

}