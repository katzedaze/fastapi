import {
  tokenResponseSchema,
  userSchema,
  type LoginInput,
  type TokenResponse,
  type User,
} from "@/types/schemas";
import Cookies from "js-cookie";
import apiClient from "./api-client";

export class AuthService {
  static async login(credentials: LoginInput): Promise<TokenResponse> {
    const formData = new FormData();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const response = await apiClient.post("/auth/login", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    const data = tokenResponseSchema.parse(response.data);

    // Store token
    localStorage.setItem("access_token", data.access_token);
    Cookies.set("access_token", data.access_token, { expires: 1 }); // 1 day

    return data;
  }

  static async logout(): Promise<void> {
    localStorage.removeItem("access_token");
    Cookies.remove("access_token");
  }

  static async getCurrentUser(): Promise<User> {
    const response = await apiClient.get("/users/me");
    return userSchema.parse(response.data);
  }

  static getToken(): string | null {
    // Check if we're in the browser environment
    if (typeof window === "undefined") return null;

    return (
      localStorage.getItem("access_token") ||
      Cookies.get("access_token") ||
      null
    );
  }

  static isAuthenticated(): boolean {
    return !!this.getToken();
  }

  static async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    const response = await apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  }
}
