import { useDepartments } from "../hooks/useDepartments";

export default function DepartmentTable() {
    const { data, isLoading, isError, error } = useDepartments();

    if (isLoading) {
        return <p className="text-slate-500 py-4">Loading departments...</p>;
    }

    if (isError) {
        return (
            <div className="rounded-lg bg-red-50 border border-red-200 p-4 text-red-600 text-sm">
                Failed to load departments: {error instanceof Error ? error.message : "Unknown error"}
            </div>
        );
    }

    const departments = data?.departments ?? [];

    if (departments.length === 0) {
        return (
            <div className="rounded-lg border p-8 text-center text-slate-500">
                No departments found. Click "Add Department" to create one.
            </div>
        );
    }

    return (
        <div className="overflow-x-auto rounded-lg border bg-white shadow-sm">
            <table className="w-full text-left text-sm text-slate-600">
                <thead className="bg-slate-50 text-xs uppercase text-slate-500 border-b">
                    <tr>
                        <th className="px-6 py-3">Name</th>
                        <th className="px-6 py-3">Description</th>
                        <th className="px-6 py-3 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y">
                    {departments.map((department) => (
                        <tr key={department.id} className="hover:bg-slate-50">
                            <td className="px-6 py-4 font-medium text-slate-900">
                                {department.name}
                            </td>
                            <td className="px-6 py-4 text-slate-500">
                                {department.description || "—"}
                            </td>
                            <td className="px-6 py-4 text-right space-x-2">
                                <button className="text-indigo-600 hover:text-indigo-900 font-medium">
                                    Edit
                                </button>
                                <button className="text-red-600 hover:text-red-900 font-medium">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}