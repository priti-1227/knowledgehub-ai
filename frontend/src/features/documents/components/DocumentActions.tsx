import {
    Download,
    Eye,
    Trash2,
} from "lucide-react";

import { Button } from "@/components/ui/button";

import type { Document } from "../types/document";
import { documentApi } from "../api/document.api";

interface Props {
    document: Document;
    onDelete: (doc: Document) => void;
}

export default function DocumentActions({
    document,
    onDelete,
}: Props) {
    return (
        <div className="flex gap-1">

            <Button
                variant="ghost"
                size="icon"
                onClick={() =>
                    documentApi.view(document.id)
                }
            >
                <Eye className="h-4 w-4" />
            </Button>

            <Button
                variant="ghost"
                size="icon"
                onClick={() =>
                    documentApi.download(document.id, document.originalName || document.title)
                }
            >
                <Download className="h-4 w-4" />
            </Button>

            <Button
                variant="ghost"
                size="icon"
                className="text-red-600"
                onClick={() =>
                    onDelete(document)
                }
            >
                <Trash2 className="h-4 w-4" />
            </Button>

        </div>
    );
}