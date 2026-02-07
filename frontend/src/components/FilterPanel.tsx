"use client";

import { useState } from "react";
import type { Priority, Tag, TaskFilters } from "@/types";

interface FilterPanelProps {
  filters: TaskFilters;
  onFiltersChange: (filters: TaskFilters) => void;
  tags: Tag[];
}

export function FilterPanel({ filters, onFiltersChange, tags }: FilterPanelProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const updateFilter = <K extends keyof TaskFilters>(key: K, value: TaskFilters[K]) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  const clearFilters = () => {
    onFiltersChange({});
  };

  const hasActiveFilters = Object.values(filters).some(
    (v) => v !== undefined && v !== "" && v !== false
  );

  return (
    <div className="mb-4 rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative">
            <input
              type="text"
              placeholder="Search tasks..."
              value={filters.search || ""}
              onChange={(e) => updateFilter("search", e.target.value || undefined)}
              className="w-64 rounded-md border border-gray-300 px-3 py-2 pl-9 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
            <svg
              className="absolute left-3 top-2.5 h-4 w-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>

          {/* Quick filters */}
          <select
            value={filters.status || "all"}
            onChange={(e) =>
              updateFilter(
                "status",
                e.target.value === "all" ? undefined : (e.target.value as TaskFilters["status"])
              )
            }
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="all">All Status</option>
            <option value="incomplete">Pending</option>
            <option value="completed">Completed</option>
          </select>

          <select
            value={filters.priority || ""}
            onChange={(e) =>
              updateFilter("priority", (e.target.value || undefined) as Priority | undefined)
            }
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            {isExpanded ? "Less filters" : "More filters"}
          </button>
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="rounded-md bg-gray-100 px-3 py-1 text-sm text-gray-600 hover:bg-gray-200"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {isExpanded && (
        <div className="mt-4 flex flex-wrap items-center gap-4 border-t border-gray-100 pt-4">
          {/* Tag filter */}
          <select
            value={filters.tag || ""}
            onChange={(e) => updateFilter("tag", e.target.value || undefined)}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">All Tags</option>
            {tags.map((tag) => (
              <option key={tag.id} value={tag.name}>
                {tag.name}
              </option>
            ))}
          </select>

          {/* Overdue toggle */}
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={filters.overdue || false}
              onChange={(e) => updateFilter("overdue", e.target.checked || undefined)}
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            Show only overdue
          </label>

          {/* Sort */}
          <select
            value={`${filters.sort || "created_at"}-${filters.order || "desc"}`}
            onChange={(e) => {
              const [sort, order] = e.target.value.split("-");
              updateFilter("sort", sort);
              updateFilter("order", order as "asc" | "desc");
            }}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="created_at-desc">Newest first</option>
            <option value="created_at-asc">Oldest first</option>
            <option value="due_date-asc">Due date (earliest)</option>
            <option value="due_date-desc">Due date (latest)</option>
            <option value="priority-desc">Priority (highest)</option>
            <option value="priority-asc">Priority (lowest)</option>
          </select>
        </div>
      )}
    </div>
  );
}
