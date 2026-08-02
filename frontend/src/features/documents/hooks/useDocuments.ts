import { useQuery } from "@tanstack/react-query";
import { documentApi } from "../api/document.api";

export function useDocuments() {
    return useQuery({
        queryKey: ["documents"],
        queryFn: documentApi.getAll,
    });
}