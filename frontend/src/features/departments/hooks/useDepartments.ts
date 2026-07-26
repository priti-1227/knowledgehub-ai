import { useQuery } from "@tanstack/react-query";

import { departmentApi } from "../api/department.api";

export function useDepartments() {
    return useQuery({
        queryKey: ["departments"],
        queryFn: departmentApi.getAll,
    });
}