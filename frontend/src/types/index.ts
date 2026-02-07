/**
 * TypeScript types for the Todo application.
 */

export type Priority = "low" | "medium" | "high" | "urgent";

export interface Tag {
  id: number;
  name: string;
  color: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
  due_date: string | null;
  reminder_at: string | null;
  recurrence_rule: string | null;
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: Priority;
  due_date?: string;
  reminder_at?: string;
  recurrence_rule?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: Priority;
  due_date?: string;
  reminder_at?: string;
  recurrence_rule?: string;
}

export interface TagCreate {
  name: string;
  color?: string;
}

export interface TagUpdate {
  name?: string;
  color?: string;
}

export interface TaskFilters {
  status?: "all" | "completed" | "incomplete";
  priority?: Priority;
  tag?: string;
  search?: string;
  overdue?: boolean;
  sort?: string;
  order?: "asc" | "desc";
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
