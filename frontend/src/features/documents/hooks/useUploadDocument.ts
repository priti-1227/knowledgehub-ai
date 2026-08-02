import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { documentApi } from "../api/document.api";

export function useUploadDocument() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: documentApi.upload,

        onSuccess() {

            toast.success(
                "Document uploaded successfully"
            );

            queryClient.invalidateQueries({
                queryKey: ["documents"],
            });

        },

        onError(error: Error) {

            toast.error(error.message);

        },

    });

}