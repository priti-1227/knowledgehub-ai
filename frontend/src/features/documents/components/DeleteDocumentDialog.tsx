import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

import { useDeleteDocument } from "../hooks/useDeleteDocument";

import type { Document } from "../types/document";

interface Props {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    document: Document | null;
}

export default function DeleteDocumentDialog({
    open,
    onOpenChange,
    document,
}: Props) {
    const { mutateAsync: deleteDocument, isPending } = useDeleteDocument();

    async function confirmDelete() {
        if (!document) return;

        await deleteDocument(document.id);
        onOpenChange(false);
    }

    return (
        <Dialog
            open={open}
            onOpenChange={onOpenChange}
        >
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Delete Document</DialogTitle>
                    <DialogDescription>
                        Are you sure you want to delete "{document?.title}"?
                    </DialogDescription>
                </DialogHeader>

                <DialogFooter>
                    <Button
                        variant="outline"
                        onClick={() => onOpenChange(false)}
                    >
                        Cancel
                    </Button>

                    <Button
                        variant="destructive"
                        onClick={confirmDelete}
                        disabled={isPending}
                    >
                        {isPending ? "Deleting..." : "Delete"}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
