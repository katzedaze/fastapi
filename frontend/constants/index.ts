export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  REGISTER: "/register",
  DASHBOARD: "/dashboard",
  ITEMS: "/items",
  USERS: "/users",
  PROFILE: "/profile",
  SETTINGS: "/settings",
} as const;

export const ITEM_STATUS_LABELS = {
  draft: "Draft",
  published: "Published",
  archived: "Archived",
} as const;

export const ITEM_CATEGORY_LABELS = {
  electronics: "Electronics",
  clothing: "Clothing",
  books: "Books",
  food: "Food",
  other: "Other",
} as const;

export const USER_ROLE_LABELS = {
  admin: "Administrator",
  user: "User",
  guest: "Guest",
} as const;
