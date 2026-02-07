"use client";

import type { Priority } from "@/types";

interface PriorityBadgeProps {
  priority: Priority;
  size?: "sm" | "md";
}

const priorityConfig: Record<Priority, { label: string; color: string; bg: string }> = {
  urgent: { label: "Urgent", color: "text-red-700", bg: "bg-red-100" },
  high: { label: "High", color: "text-orange-700", bg: "bg-orange-100" },
  medium: { label: "Medium", color: "text-blue-700", bg: "bg-blue-100" },
  low: { label: "Low", color: "text-gray-600", bg: "bg-gray-100" },
};

export function PriorityBadge({ priority, size = "sm" }: PriorityBadgeProps) {
  const config = priorityConfig[priority];
  const sizeClasses = size === "sm" ? "px-2 py-0.5 text-xs" : "px-3 py-1 text-sm";

  return (
    <span
      className={`inline-flex items-center rounded-full font-medium ${config.bg} ${config.color} ${sizeClasses}`}
    >
      {config.label}
    </span>
  );
}
