import {
    FileText,
    FileSpreadsheet,
    FileImage,
} from "lucide-react";

interface Props {
    mimeType: string;
}

export default function FileIcon({
    mimeType,
}: Props) {
    if (mimeType.includes("pdf")) {
        return (
            <FileText className="text-red-500 h-5 w-5" />
        );
    }

    if (
        mimeType.includes("word") ||
        mimeType.includes("document")
    ) {
        return (
            <FileText className="text-blue-500 h-5 w-5" />
        );
    }

    if (mimeType.includes("image")) {
        return (
            <FileImage className="text-green-500 h-5 w-5" />
        );
    }

    return <FileSpreadsheet className="h-5 w-5" />;
}