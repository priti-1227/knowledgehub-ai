import type { Table } from "@tanstack/react-table";

import { Input } from "@/components/ui/input";

interface Props<TData> {
    table: Table<TData>;
    searchColumn?: string;
}

export function DataTableToolbar<TData>({
    table,
    searchColumn,
}: Props<TData>) {
    if (!searchColumn) return null;

    return (
        <Input
            placeholder="Search..."
            value={
                (table
                    .getColumn(searchColumn)
                    ?.getFilterValue() as string) ?? ""
            }
            onChange={(e) =>
                table
                    .getColumn(searchColumn)
                    ?.setFilterValue(e.target.value)
            }
            className="max-w-sm"
        />
    );
}