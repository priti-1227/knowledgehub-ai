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