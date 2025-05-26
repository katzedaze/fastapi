import { z } from "zod";

// Item status enum (matching backend)
export const itemStatusSchema = z.enum(["draft", "published", "archived"]);
export type ItemStatus = z.infer<typeof itemStatusSchema>;

// Item category enum (matching backend)
export const itemCategorySchema = z.enum([
  "electronics",
  "clothing",
  "books",
  "food",
  "other",
]);
export type ItemCategory = z.infer<typeof itemCategorySchema>;

// Base item schema (for create/update operations)
export const itemBaseSchema = z.object({
  title: z.string().min(1, "Title is required").max(255),
  description: z.string().max(1000).optional(),
  price: z.number().min(0, "Price must be positive").max(1000000),
  quantity: z
    .number()
    .int()
    .min(0, "Quantity must be non-negative")
    .max(10000)
    .default(1),
  category: itemCategorySchema.default("other"),
  status: itemStatusSchema.default("draft"),
  is_available: z.boolean().default(true),
});

// Full item schema with ID and timestamps (for API responses)
export const itemSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  description: z.string().nullable(),
  price: z.number(),
  quantity: z.number(),
  category: itemCategorySchema,
  status: itemStatusSchema,
  is_available: z.boolean(),
  owner_id: z.string().uuid(),
  created_at: z.string(),
  updated_at: z.string(),
});

// Item create schema
export const itemCreateSchema = itemBaseSchema;

// Item update schema (all fields optional)
export const itemUpdateSchema = itemBaseSchema.partial();

// Type exports
export type Item = z.infer<typeof itemSchema>;
export type ItemCreate = z.infer<typeof itemCreateSchema>;
export type ItemUpdate = z.infer<typeof itemUpdateSchema>;
