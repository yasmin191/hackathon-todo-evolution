"use client";

import { useState } from "react";
import type { Task } from "@/types";

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => Promise<void>;
}

export default function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const [loading, setLoading] = useState(false);
  const [showDescription, setShowDescription] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleToggle = async () => {
    setLoading(true);
    try {
      await onToggleComplete(task.id);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      await onDelete(task.id);
    } finally {
      setLoading(false);
      setShowDeleteConfirm(false);
    }
  };

  return (
    <div
      className={`p-4 bg-white rounded-lg border ${
        task.completed ? "border-green-200 bg-green-50" : "border-gray-200"
      }`}
    >
      <div className="flex items-start gap-3">
        <button
          onClick={handleToggle}
          disabled={loading}
          className={`mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
            task.completed
              ? "bg-green-500 border-green-500 text-white"
              : "border-gray-300 hover:border-blue-500"
          }`}
          aria-label={task.completed ? "Mark incomplete" : "Mark complete"}
        >
          {task.completed && (
            <svg
              className="w-3 h-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3
            className={`font-medium ${
              task.completed ? "text-gray-500 line-through" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <button
              onClick={() => setShowDescription(!showDescription)}
              className="text-sm text-blue-600 hover:underline mt-1"
            >
              {showDescription ? "Hide details" : "Show details"}
            </button>
          )}

          {showDescription && task.description && (
            <p className="mt-2 text-sm text-gray-600 whitespace-pre-wrap">
              {task.description}
            </p>
          )}
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onEdit(task)}
            disabled={loading}
            className="px-3 py-1 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
          >
            Edit
          </button>

          {!showDeleteConfirm ? (
            <button
              onClick={() => setShowDeleteConfirm(true)}
              disabled={loading}
              className="px-3 py-1 text-sm text-gray-600 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            >
              Delete
            </button>
          ) : (
            <div className="flex gap-1">
              <button
                onClick={handleDelete}
                disabled={loading}
                className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700"
              >
                Confirm
              </button>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                disabled={loading}
                className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
