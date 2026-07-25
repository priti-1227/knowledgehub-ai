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
  login: async (credentials: LoginInput): Promise<LoginResponse> => {
    // Simulate network latency
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Mock verification
    if (credentials.email === "admin@gmail.com" && credentials.password === "admin123") {
      return {
        user: {
          id: "1",
          email: credentials.email,
          name: "Admin User",
          role: "admin",
        },
        token: "mock-jwt-token-xyz-12345",
      };
    }

    // Generic mock response for demo purposes (unless it is invalid)
    if (credentials.email.includes("error")) {
      throw new Error("Invalid email or password");
    }

    return {
      user: {
        id: "2",
        email: credentials.email,
        name: credentials.email.split("@")[0],
        role: "user",
      },
      token: "mock-jwt-token-abc-98765",
    };
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
