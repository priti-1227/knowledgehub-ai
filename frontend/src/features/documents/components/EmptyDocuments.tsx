import { FileText } from "lucide-react";

export default function EmptyDocuments() {
    return (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-20">

            <FileText className="h-12 w-12 text-muted-foreground" />

            <h2 className="mt-4 text-xl font-semibold">
                No Documents
            </h2>

            <p className="mt-2 text-sm text-muted-foreground">
                Upload your first document.
            </p>

        </div>
    );
}