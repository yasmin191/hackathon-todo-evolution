"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import type { Task, TaskCreate, TaskUpdate } from "@/types";
import { api } from "@/lib/api";
import { getSession, logout, isAuthenticated } from "@/lib/auth";
import TaskList from "@/components/TaskList";
import TaskForm from "@/components/TaskForm";

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [userEmail, setUserEmail] = useState<string>("");
  const [userId, setUserId] = useState<string>("");

  const loadTasks = useCallback(async () => {
    const session = getSession();
    if (!session) {
      router.push("/login");
      return;
    }

    setUserId(session.user.id);
    setUserEmail(session.user.email);
    setLoading(true);
    setError(null);

    try {
      const data = await api.getTasks(session.user.id);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
      return;
    }
    loadTasks();
  }, [router, loadTasks]);

  const handleCreateTask = async (data: TaskCreate | TaskUpdate) => {
    const newTask = await api.createTask(userId, data as TaskCreate);
    setTasks((prev) => [...prev, newTask]);
    setShowForm(false);
  };

  const handleUpdateTask = async (data: TaskCreate | TaskUpdate) => {
    if (!editingTask) return;
    const updatedTask = await api.updateTask(
      userId,
      editingTask.id,
      data as TaskUpdate
    );
    setTasks((prev) =>
      prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
    );
    setEditingTask(null);
  };

  const handleToggleComplete = async (taskId: number) => {
    const updatedTask = await api.toggleComplete(userId, taskId);
    setTasks((prev) =>
      prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
    );
  };

  const handleDeleteTask = async (taskId: number) => {
    await api.deleteTask(userId, taskId);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  const pendingCount = tasks.filter((t) => !t.completed).length;
  const completedCount = tasks.filter((t) => t.completed).length;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
          <p className="text-sm text-gray-500">{userEmail}</p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-2xl font-bold text-blue-600">{pendingCount}</p>
          <p className="text-sm text-gray-500">Pending</p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-2xl font-bold text-green-600">{completedCount}</p>
          <p className="text-sm text-gray-500">Completed</p>
        </div>
      </div>

      {/* Add Task Button */}
      <button
        onClick={() => setShowForm(true)}
        className="w-full mb-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
        Add Task
      </button>

      {/* Task List */}
      <TaskList
        tasks={tasks}
        loading={loading}
        error={error}
        onToggleComplete={handleToggleComplete}
        onEdit={(task) => setEditingTask(task)}
        onDelete={handleDeleteTask}
        onRetry={loadTasks}
      />

      {/* Task Form Modal */}
      {(showForm || editingTask) && (
        <TaskForm
          task={editingTask}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
          onCancel={() => {
            setShowForm(false);
            setEditingTask(null);
          }}
        />
      )}
    </div>
  );
}
