import type { LoginInput } from "../schemas/login.schema";
import type { RegisterInput } from "../schemas/register.schema";

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

  register: async (data: RegisterInput): Promise<LoginResponse> => {
    // Simulate network latency
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Mock verification
    if (data.email.includes("error")) {
      throw new Error("Email is already registered");
    }

    return {
      user: {
        id: Math.random().toString(36).substring(2, 9),
        email: data.email,
        name: data.fullName,
        role: "user",
      },
      token: "mock-jwt-token-reg-" + Math.random().toString(36).substring(2, 9),
    };
  },

  logout: async (): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 800));
  },
};
