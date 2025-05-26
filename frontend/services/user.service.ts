import {
  userSchema,
  type User,
  type UserCreate,
  type UserUpdate,
} from "@/types/schemas";
import { z } from "zod";
import apiClient from "./api-client";

export class UserService {
  static async register(data: UserCreate): Promise<User> {
    const response = await apiClient.post("/users", data);
    return userSchema.parse(response.data);
  }

  static async getUsers(): Promise<User[]> {
    const response = await apiClient.get("/users");
    return z.array(userSchema).parse(response.data);
  }

  static async getUser(id: string): Promise<User> {
    const response = await apiClient.get(`/users/${id}`);
    return userSchema.parse(response.data);
  }

  static async createUser(data: UserCreate): Promise<User> {
    const response = await apiClient.post("/users", data);
    return userSchema.parse(response.data);
  }

  static async updateUser(id: string, data: UserUpdate): Promise<User> {
    const response = await apiClient.patch(`/users/${id}`, data);
    return userSchema.parse(response.data);
  }

  static async deleteUser(id: string): Promise<void> {
    await apiClient.delete(`/users/${id}`);
  }
}
