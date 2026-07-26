import { useState } from "react";

import DepartmentTable
    from "../components/DepartmentTable";

import DepartmentDialog
    from "../components/DepartmentDialog";

export default function DepartmentsPage() {

    const [

        open,

        setOpen,

    ] = useState(false);

    return (

        <div className="space-y-6">

            <div className="flex justify-between">

                <div>

                    <h1
                        className="text-3xl font-bold"
                    >
                        Departments
                    </h1>

                    <p
                        className="text-slate-500"
                    >
                        Manage company departments.
                    </p>

                </div>

                <button

                    onClick={() =>
                        setOpen(true)
                    }

                    className="
                    rounded-lg
                    bg-indigo-600
                    px-4
                    py-2
                    text-white
                    "

                >

                    Add Department

                </button>

            </div>

            <DepartmentTable />

            {open && (

                <DepartmentDialog

                    onClose={() =>
                        setOpen(false)
                    }

                />

            )}

        </div>

    );

}