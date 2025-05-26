import { apiErrorSchema } from "@/types/schemas/common";
import axios, { AxiosError, AxiosInstance } from "axios";
import Cookies from "js-cookie";
import { toast } from "sonner";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token =
          localStorage.getItem("access_token") || Cookies.get("access_token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const parsedError = apiErrorSchema.safeParse(error.response?.data);
        const message = parsedError.success
          ? typeof parsedError.data.detail === "string"
            ? parsedError.data.detail
            : "Validation error"
          : "An error occurred";

        if (error.response?.status === 401) {
          // Clear auth data on 401
          localStorage.removeItem("access_token");
          Cookies.remove("access_token");

          // Redirect to login if not already there
          if (window.location.pathname !== "/login") {
            window.location.href = "/login";
          }
        } else if (error.response?.status === 403) {
          toast.error("You do not have permission to perform this action");
        } else if (error.response?.status === 500) {
          toast.error("Server error. Please try again later.");
        } else if (error.response?.status !== 422) {
          // Don't show toast for validation errors (422)
          toast.error(message);
        }

        return Promise.reject(error);
      }
    );
  }

  get instance() {
    return this.client;
  }
}

export const apiClient = new ApiClient();
export default apiClient.instance;
