import {
  itemSchema,
  type Item,
  type ItemCreate,
  type ItemUpdate,
} from "@/types/schemas";
import { z } from "zod";
import apiClient from "./api-client";

export class ItemService {
  static async getItems(): Promise<Item[]> {
    const response = await apiClient.get("/items");
    return z.array(itemSchema).parse(response.data);
  }

  static async getItem(id: string): Promise<Item> {
    const response = await apiClient.get(`/items/${id}`);
    return itemSchema.parse(response.data);
  }

  static async createItem(data: ItemCreate): Promise<Item> {
    const response = await apiClient.post("/items", data);
    return itemSchema.parse(response.data);
  }

  static async updateItem(id: string, data: ItemUpdate): Promise<Item> {
    const response = await apiClient.patch(`/items/${id}`, data);
    return itemSchema.parse(response.data);
  }

  static async deleteItem(id: string): Promise<void> {
    await apiClient.delete(`/items/${id}`);
  }
}
