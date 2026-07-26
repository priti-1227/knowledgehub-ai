import type {
    DepartmentResponse,
    CreateDepartmentPayload,
} from "../types/department";

const API_URL = `${import.meta.env.VITE_API_URL}/departments`;

function getAuthHeaders() {
    const token = localStorage.getItem("token");

    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };
}

export const departmentApi = {
    async getAll(): Promise<DepartmentResponse> {
        const response = await fetch(API_URL, {
            headers: getAuthHeaders(),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch departments.");
        }

        return response.json();
    },

    async create(data: CreateDepartmentPayload) {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message);
        }

        return response.json();
    },
};