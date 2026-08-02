import { Plus } from "lucide-react";
import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { DataTable } from "@/components/shared/DataTable/DataTable";

import { useDocuments } from "../hooks/useDocuments";
import { documentColumns } from "../columns";

import UploadDocumentDialog from "../components/UploadDocumentDialog";
import DeleteDocumentDialog from "../components/DeleteDocumentDialog";
import EmptyDocuments from "../components/EmptyDocuments";

import type { Document } from "../types/document";

export default function DocumentsPage() {
    const [uploadOpen, setUploadOpen] = useState(false);
    const [deleteOpen, setDeleteOpen] = useState(false);

    const [selectedDocument, setSelectedDocument] =
        useState<Document | null>(null);

    const { data, isLoading } = useDocuments();

    function handleUpload() {
        setSelectedDocument(null);
        setUploadOpen(true);
    }

    function handleDelete(document: Document) {
        setSelectedDocument(document);
        setDeleteOpen(true);
    }

    const columns = useMemo(
        () => documentColumns(handleDelete),
        []
    );

    if (isLoading) {
        return (
            <div className="space-y-3">
                {Array.from({ length: 8 }).map((_, index) => (
                    <Skeleton
                        key={index}
                        className="h-12 w-full"
                    />
                ))}
            </div>
        );
    }

    const documents = data?.documents ?? [];

    return (
        <div className="space-y-6">

            <div className="flex items-center justify-between">

                <div>

                    <h1 className="text-3xl font-bold">
                        Documents
                    </h1>

                    <p className="text-muted-foreground">
                        Upload and manage organization documents.
                    </p>

                </div>

                <Button onClick={handleUpload}>
                    <Plus className="mr-2 h-4 w-4" />
                    Upload Document
                </Button>

            </div>

            {documents.length === 0 ? (
                <EmptyDocuments />
            ) : (
                <DataTable
                    columns={columns}
                    data={documents}
                    searchColumn="title"
                />
            )}

            <UploadDocumentDialog
                open={uploadOpen}
                onOpenChange={setUploadOpen}
            />

            <DeleteDocumentDialog
                open={deleteOpen}
                onOpenChange={setDeleteOpen}
                document={selectedDocument}
            />

        </div>
    );
}