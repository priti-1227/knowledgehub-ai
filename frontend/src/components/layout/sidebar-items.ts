import {
    LayoutDashboard,
    Building2,
    FileText,
    MessageSquare,
    BarChart3,
    Settings,
} from "lucide-react";

export const sidebarItems = [
    {
        title: "Dashboard",
        path: "/dashboard",
        icon: LayoutDashboard,
    },
    {
        title: "Departments",
        path: "/departments",
        icon: Building2,
    },
    {
        title: "Documents",
        path: "/documents",
        icon: FileText,
    },
    {
        title: "AI Assistant",
        path: "/chat",
        icon: MessageSquare,
    },
    {
        title: "Analytics",
        path: "/analytics",
        icon: BarChart3,
    },
    {
        title: "Settings",
        path: "/settings",
        icon: Settings,
    },
];