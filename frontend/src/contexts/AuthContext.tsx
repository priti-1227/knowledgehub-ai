import {
    createContext,
    useEffect,
    useState,
} from "react";

import type {
    AuthContextType,
    User,
} from "@/features/auth/types/auth.types";

export const AuthContext =
    createContext<AuthContextType | null>(null);

interface Props {
    children: React.ReactNode;
}

export function AuthProvider({
    children,
}: Props) {

    const [user, setUser] =
        useState<User | null>(null);

    const [token, setToken] =
        useState<string | null>(null);

    const login = (
        token: string,
        user: User
    ) => {

        localStorage.setItem(
            "token",
            token
        );

        localStorage.setItem(
            "user",
            JSON.stringify(user)
        );

        setToken(token);

        setUser(user);
    };
    const logout = () => {

        localStorage.removeItem("token");

        localStorage.removeItem("user");

        setToken(null);

        setUser(null);

    };
    useEffect(() => {

        const token =
            localStorage.getItem("token");

        const user =
            localStorage.getItem("user");

        if (token && user) {

            setToken(token);

            setUser(JSON.parse(user));

        }

    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                isAuthenticated: !!token,

                login,

                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}