/**
 * API client for backend communication.
 */

import type {
  Tag,
  TagCreate,
  TagUpdate,
  Task,
  TaskCreate,
  TaskFilters,
  TaskUpdate,
} from "@/types";
/* eslint-disable @typescript-eslint/no-unused-vars */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "";

class ApiClient {
  private token: string | null = null;

  setToken(token: string | null): void {
    this.token = token;
  }

  private async fetch<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };

    if (this.token) {
      (headers as Record<string, string>)["Authorization"] =
        `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Token expired or invalid
      this.token = null;
      if (typeof window !== "undefined") {
        window.location.href = "/login?expired=true";
      }
      throw new Error("Session expired");
    }

    if (response.status === 204) {
      return undefined as T;
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || error.error || "Request failed");
    }

    return response.json();
  }

  // Task operations
  async getTasks(userId: string, filters?: TaskFilters): Promise<Task[]> {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.status) params.append("status", filters.status);
      if (filters.priority) params.append("priority", filters.priority);
      if (filters.tag) params.append("tag", filters.tag);
      if (filters.search) params.append("search", filters.search);
      if (filters.overdue) params.append("overdue", "true");
      if (filters.sort) params.append("sort", filters.sort);
      if (filters.order) params.append("order", filters.order);
    }
    const query = params.toString();
    return this.fetch<Task[]>(
      `/api/${userId}/tasks${query ? `?${query}` : ""}`,
    );
  }

  async createTask(userId: string, data: TaskCreate): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}`);
  }

  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdate,
  ): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.fetch<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  // Tag operations
  async getTags(userId: string): Promise<Tag[]> {
    return this.fetch<Tag[]>(`/api/${userId}/tags`);
  }

  async createTag(userId: string, data: TagCreate): Promise<Tag> {
    return this.fetch<Tag>(`/api/${userId}/tags`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateTag(
    userId: string,
    tagId: number,
    data: TagUpdate,
  ): Promise<Tag> {
    return this.fetch<Tag>(`/api/${userId}/tags/${tagId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteTag(userId: string, tagId: number): Promise<void> {
    return this.fetch<void>(`/api/${userId}/tags/${tagId}`, {
      method: "DELETE",
    });
  }

  async addTagsToTask(
    userId: string,
    taskId: number,
    tagIds: number[],
  ): Promise<void> {
    return this.fetch<void>(`/api/${userId}/tasks/${taskId}/tags`, {
      method: "POST",
      body: JSON.stringify({ tag_ids: tagIds }),
    });
  }

  async removeTagFromTask(
    userId: string,
    taskId: number,
    tagId: number,
  ): Promise<void> {
    return this.fetch<void>(`/api/${userId}/tasks/${taskId}/tags/${tagId}`, {
      method: "DELETE",
    });
  }

  // Chat operations (Phase III)
  async sendMessage(
    message: string,
    conversationId?: number,
  ): Promise<ChatResponse> {
    return this.fetch<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        conversation_id: conversationId || null,
      }),
    });
  }

  async getConversations(): Promise<Conversation[]> {
    return this.fetch<Conversation[]>("/api/conversations");
  }

  async getMessages(conversationId: number): Promise<Message[]> {
    return this.fetch<Message[]>(
      `/api/conversations/${conversationId}/messages`,
    );
  }
}

export const api = new ApiClient();

// Chat types
export interface ChatResponse {
  response: string;
  conversation_id: number;
  message_id: number;
}

export interface Conversation {
  id: number;
  user_id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message: string | null;
}

export interface Message {
  id: number;
  conversation_id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}
