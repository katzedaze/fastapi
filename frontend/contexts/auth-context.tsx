"use client";

import { ROUTES } from "@/constants";
import { AuthService } from "@/services";
import { type User, type UserRole } from "@/types/schemas";
import { useRouter } from "next/navigation";
import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);
  const router = useRouter();

  const refreshUser = async () => {
    try {
      // Only check authentication after component is mounted to avoid SSR mismatch
      if (!mounted) return;

      if (!AuthService.isAuthenticated()) {
        setUser(null);
        return;
      }

      const userData = await AuthService.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      setUser(null);
    }
  };

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const initAuth = async () => {
      try {
        await refreshUser();
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, [mounted]);

  const login = async (email: string, password: string) => {
    try {
      await AuthService.login({ email, password });
      await refreshUser();
      router.push(ROUTES.DASHBOARD);
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await AuthService.logout();
      setUser(null);
      router.push(ROUTES.LOGIN);
    } catch (error) {
      console.error("Logout error:", error);
      // Force logout even if API call fails
      AuthService.logout();
      setUser(null);
      router.push(ROUTES.LOGIN);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export function useRequireAuth(requiredRole?: UserRole) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push(ROUTES.LOGIN);
      } else if (
        requiredRole &&
        user.role !== requiredRole &&
        user.role !== "admin"
      ) {
        router.push("/unauthorized");
      }
    }
  }, [user, loading, requiredRole, router]);

  return { user, loading };
}
