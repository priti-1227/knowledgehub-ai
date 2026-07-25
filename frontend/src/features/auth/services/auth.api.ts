import { API_BASE_URL } from "@/config/api";
import type { LoginInput } from "../schemas/login.schema";
import type { RegisterRequest } from "../types/auth.types";

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

export interface LoginResponse {
  user: User;
  token: string;
}

/**
 * Simulates authentication API calls.
 * Replace the implementation with actual fetch / axios calls when backend is ready.
 */
export const authApi = {
  login: async (data: LoginInput) => {
    const response = await fetch(
      `${API_BASE_URL}/api/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message);
    }

    return result;
  },

  register: async (data: RegisterRequest) => {
    const response = await fetch(
      `${API_BASE_URL}/api/auth/register`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message);
    }

    return result;
  },

  logout: async (): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 800));
  },
};
