import { NavLink } from "react-router-dom";
import type { LucideIcon } from "lucide-react";

interface NavItemProps {
    title: string;
    path: string;
    icon: LucideIcon;
}

export default function NavItem({
    title,
    path,
    icon: Icon,
}: NavItemProps) {
    return (
        <NavLink
            to={path}
            className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 transition-all font-medium
        ${isActive
                    ? "bg-indigo-600 text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`
            }
        >
            <Icon size={20} />
            <span>{title}</span>
        </NavLink>
    );
}