import { API_BASE_URL } from "@/config/api";
import type {
    DepartmentResponse,
    CreateDepartmentPayload,
} from "../types/department";

const API_URL = `${API_BASE_URL}/api/departments`;

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

    async update(id: string, data: CreateDepartmentPayload) {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message);
        }

        return response.json();
    },




    async delete(id: string) {

        const response = await fetch(

            `${API_URL}/${id}`,

            {

                method: "DELETE",

                headers: getAuthHeaders(),

            }

        );

        if (!response.ok)

            throw new Error("Delete failed");

    }

}