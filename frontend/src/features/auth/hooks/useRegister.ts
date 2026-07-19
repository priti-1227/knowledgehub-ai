import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { RegisterInput } from "../schemas/register.schema";
import { authApi } from "../services/auth.api";

export function useRegister() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const registerUser = async (data: RegisterInput) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authApi.register(data);
      
      // Save auth details to local storage upon successful registration
      localStorage.setItem("token", response.token);
      localStorage.setItem("user", JSON.stringify(response.user));
      
      // Navigate to dashboard
      navigate("/dashboard");
    } catch (err: any) {
      setError(err?.message || "Something went wrong during registration. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return {
    register: registerUser,
    isLoading,
    error,
  };
}
