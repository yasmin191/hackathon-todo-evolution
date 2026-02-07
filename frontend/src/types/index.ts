/**
 * TypeScript types for the Todo application.
 */

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
}

export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface AuthSession {
  user: User;
  token: string;
}

export interface ApiError {
  error: string;
  detail?: unknown;
}
