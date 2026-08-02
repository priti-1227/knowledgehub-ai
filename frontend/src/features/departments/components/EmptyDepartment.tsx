import { FolderOpen } from "lucide-react";

export default function EmptyDepartment() {
    return (
        <div className="py-16 flex flex-col items-center text-center">
            <FolderOpen className="h-12 w-12 text-muted-foreground" />

            <h2 className="mt-4 text-xl font-semibold">
                No Departments Found
            </h2>

            <p className="text-muted-foreground mt-2">
                Create your first department.
            </p>
        </div>
    );
}