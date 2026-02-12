/**
 * Authentication utilities.
 *
 * For hackathon purposes, this is a simplified auth implementation.
 * In production, use Better Auth or similar library.
 */

import { api } from "./api";
import type { User, AuthSession } from "@/types";

const AUTH_STORAGE_KEY = "todo_auth_session";

export function getSession(): AuthSession | null {
  if (typeof window === "undefined") return null;

  const stored = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!stored) return null;

  try {
    const session = JSON.parse(stored) as AuthSession;
    api.setToken(session.token);
    return session;
  } catch {
    return null;
  }
}

export function setSession(session: AuthSession): void {
  if (typeof window === "undefined") return;

  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
  api.setToken(session.token);
}

export function clearSession(): void {
  if (typeof window === "undefined") return;

  localStorage.removeItem(AUTH_STORAGE_KEY);
  api.setToken(null);
}

export function isAuthenticated(): boolean {
  return getSession() !== null;
}

export function getCurrentUser(): User | null {
  const session = getSession();
  return session?.user || null;
}

/**
 * Demo authentication for hackathon.
 * Calls backend to get a properly signed JWT token.
 */
export async function demoLogin(email: string): Promise<AuthSession> {
  const response = await fetch("/auth/demo-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  const data = await response.json();
  const session: AuthSession = {
    user: { id: data.user_id, email: data.email },
    token: data.token,
  };

  setSession(session);
  return session;
}

export async function logout(): Promise<void> {
  clearSession();
}
