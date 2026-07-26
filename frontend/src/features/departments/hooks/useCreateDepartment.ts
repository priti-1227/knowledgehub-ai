import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { departmentApi } from "../api/department.api";

export function useCreateDepartment() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: departmentApi.create,

        onSuccess: () => {

            toast.success("Department created.");

            queryClient.invalidateQueries({

                queryKey: ["departments"],

            });

        },

        onError: (error: Error) => {

            toast.error(error.message);

        },

    });

}