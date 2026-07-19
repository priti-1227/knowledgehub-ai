import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { LoginInput } from "../schemas/login.schema";
import { authApi } from "../services/auth.api";
import type { User } from "../services/auth.api";

export function useLogin() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const login = async (data: LoginInput) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authApi.login(data);
      
      // Save auth details to local storage (or your state management)
      localStorage.setItem("token", response.token);
      localStorage.setItem("user", JSON.stringify(response.user));
      
      // Navigate to dashboard after successful login
      navigate("/dashboard");
    } catch (err: any) {
      setError(err?.message || "Something went wrong during login. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await authApi.logout();
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      navigate("/login");
    } catch (err: any) {
      console.error("Logout failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const isAuthenticated = (): boolean => {
    return !!localStorage.getItem("token");
  };

  const getCurrentUser = (): User | null => {
    const userStr = localStorage.getItem("user");
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  };

  return {
    login,
    logout,
    isLoading,
    error,
    isAuthenticated,
    getCurrentUser,
  };
}
