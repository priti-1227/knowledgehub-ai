import { Bell } from "lucide-react";

export default function Topbar() {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    return (
        <header className="h-16 border-b bg-white px-8 flex items-center justify-between">
            <h2 className="font-semibold text-lg">
                Welcome, {user.fullName}
            </h2>

            <div className="flex items-center gap-6">
                <Bell
                    className="text-slate-500"
                    size={20}
                />

                <div className="flex items-center gap-2">
                    <div className="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                        {user.fullName?.charAt(0)}
                    </div>

                    <div>
                        <p className="font-semibold">
                            {user.fullName}
                        </p>

                        <p className="text-xs text-slate-500">
                            {user.role}
                        </p>
                    </div>
                </div>
            </div>
        </header>
    );
}