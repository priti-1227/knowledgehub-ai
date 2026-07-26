import { sidebarItems } from "./sidebar-items";
import NavItem from "./NavItem";

export default function Sidebar() {
    return (
        <aside className="w-64 border-r bg-white h-screen flex flex-col">
            <div className="border-b p-6">
                <h1 className="text-2xl font-bold text-indigo-600">
                    KnowledgeHub AI
                </h1>

                <p className="text-xs text-slate-500 mt-1">
                    Enterprise Knowledge Assistant
                </p>
            </div>

            <nav className="flex-1 p-4 space-y-2">
                {sidebarItems.map((item) => (
                    <NavItem
                        key={item.path}
                        {...item}
                    />
                ))}
            </nav>
        </aside>
    );
}