import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { departmentApi } from "../api/department.api";

export function useUpdateDepartment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({
            id,
            ...data
        }: any) =>
            departmentApi.update(id, data),

        onSuccess() {
            toast.success("Department updated");

            queryClient.invalidateQueries({
                queryKey: ["departments"],
            });
        },
    });
}