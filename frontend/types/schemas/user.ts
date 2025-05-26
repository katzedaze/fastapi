import { z } from "zod";

// User role enum
export const userRoleSchema = z.enum(["admin", "user", "guest"]);
export type UserRole = z.infer<typeof userRoleSchema>;

// Base user schema
export const userBaseSchema = z.object({
  email: z.string().email(),
  full_name: z.string().min(1, "Full name is required"),
  is_active: z.boolean().default(true),
  role: userRoleSchema.default("user"),
});

// User schema with ID and timestamps
export const userSchema = userBaseSchema.extend({
  id: z.string().uuid(),
  created_at: z.string(),
  updated_at: z.string(),
});

// User create schema
export const userCreateSchema = userBaseSchema.extend({
  password: z.string().min(6, "Password must be at least 6 characters"),
});

// User update schema (all fields optional)
export const userUpdateSchema = userBaseSchema.partial().extend({
  password: z.string().min(6).optional(),
});

// Type exports
export type User = z.infer<typeof userSchema>;
export type UserCreate = z.infer<typeof userCreateSchema>;
export type UserUpdate = z.infer<typeof userUpdateSchema>;
