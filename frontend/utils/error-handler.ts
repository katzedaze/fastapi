import { apiErrorSchema } from "@/types/schemas/common";
import { AxiosError } from "axios";
import { z } from "zod";

export function getErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    const parsedError = apiErrorSchema.safeParse(error.response?.data);

    if (parsedError.success) {
      const detail = parsedError.data.detail;

      if (typeof detail === "string") {
        return detail;
      }

      // Handle validation errors
      if (Array.isArray(detail) && detail.length > 0) {
        return detail
          .map((err) => `${err.loc.join(".")}: ${err.msg}`)
          .join(", ");
      }
    }

    return error.message || "An error occurred";
  }

  if (error instanceof z.ZodError) {
    return error.errors
      .map((err) => `${err.path.join(".")}: ${err.message}`)
      .join(", ");
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "An unknown error occurred";
}
