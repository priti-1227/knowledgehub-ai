import type { ColumnDef } from "@tanstack/react-table";

import type { Document } from "./types/document";
import DocumentActions from "./components/DocumentActions";

// import { DocumentActions } from "./components/DocumentActions";

export function documentColumns(
    onDelete: (document: Document) => void
): ColumnDef<Document>[] {

    return [

        {
            accessorKey: "title",
            header: "Title",
        },

        {
            accessorKey: "department.name",
            header: "Department",
            cell: ({ row }) =>
                row.original.department.name,
        },

        {
            accessorKey: "uploadedBy.fullName",
            header: "Uploaded By",
            cell: ({ row }) =>
                row.original.uploadedBy.fullName,
        },

        {
            accessorKey: "createdAt",
            header: "Uploaded",
            cell: ({ row }) =>
                new Date(
                    row.original.createdAt
                ).toLocaleDateString(),
        },

        {
            id: "actions",
            cell: ({ row }) => (
                <DocumentActions
                    document={row.original}
                    onDelete={onDelete}
                />
            ),
        },

    ];
}