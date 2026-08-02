import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { documentApi } from "../api/document.api";

export function useDeleteDocument() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: documentApi.delete,

        onSuccess() {

            toast.success("Document deleted");

            queryClient.invalidateQueries({
                queryKey: ["documents"],
            });

        },

        onError(error: Error) {

            toast.error(error.message);

        },

    });

}