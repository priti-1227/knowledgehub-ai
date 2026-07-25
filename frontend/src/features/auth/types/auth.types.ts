export interface RegisterRequest {
    fullName: string;
    email: string;
    password: string;
    confirmPassword: string;
}

export interface User {
    id: string;
    fullName: string;
    email: string;
    role: "ADMIN" | "EMPLOYEE";
}

export interface AuthResponse {
    success: boolean;
    user: User;
}
export interface AuthContextType {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;

    login: (token: string, user: User) => void;
    logout: () => void;
}