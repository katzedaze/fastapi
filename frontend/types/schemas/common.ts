import { z } from "zod";

// API Error response schema
export const apiErrorSchema = z.object({
  detail: z.union([
    z.string(),
    z.array(
      z.object({
        loc: z.array(z.union([z.string(), z.number()])),
        msg: z.string(),
        type: z.string(),
      })
    ),
  ]),
});

export type ApiError = z.infer<typeof apiErrorSchema>;

// Pagination schema
export const paginationSchema = z.object({
  total: z.number(),
  skip: z.number(),
  limit: z.number(),
});

export type Pagination = z.infer<typeof paginationSchema>;
