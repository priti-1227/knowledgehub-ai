import { createBrowserRouter } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import AuthLayout from "../layouts/AuthLayout";
import LoginPage from "../features/auth/pages/LoginPage";
import NotFoundPage from "../pages/NotFoundPage";
import { DashboardPage } from "../features/dashboard/pages/DashboardPage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <AuthLayout />,
        children: [
            {
                index: true,
                element: <LoginPage />,
            },
            {
                path: "login",
                element: <LoginPage />,
            },
        ],
    },
    {
        path: "/dashboard",
        element: <DashboardLayout />,
        children: [
            {
                index: true,
                element: <DashboardPage />,
            },
        ],
    },
    {
        path: "*",
        element: <NotFoundPage />,
    },
]);