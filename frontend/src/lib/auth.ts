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
 * Creates a simple JWT token for testing.
 */
export async function demoLogin(email: string): Promise<AuthSession> {
  // For demo purposes, create a simple user ID from email
  const userId = `user_${email.replace(/[^a-zA-Z0-9]/g, "_")}`;

  // Create a demo JWT (in production, this comes from Better Auth)
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const payload = btoa(JSON.stringify({ sub: userId, email }));
  const signature = btoa("demo-signature");
  const token = `${header}.${payload}.${signature}`;

  const session: AuthSession = {
    user: { id: userId, email },
    token,
  };

  setSession(session);
  return session;
}

export async function logout(): Promise<void> {
  clearSession();
}
