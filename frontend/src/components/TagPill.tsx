"use client";

import type { Tag } from "@/types";

interface TagPillProps {
  tag: Tag;
  onRemove?: () => void;
  size?: "sm" | "md";
}

export function TagPill({ tag, onRemove, size = "sm" }: TagPillProps) {
  const sizeClasses = size === "sm" ? "px-2 py-0.5 text-xs" : "px-3 py-1 text-sm";

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full font-medium ${sizeClasses}`}
      style={{ backgroundColor: `${tag.color}20`, color: tag.color }}
    >
      {tag.name}
      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-1 hover:opacity-70"
          aria-label={`Remove ${tag.name} tag`}
        >
          &times;
        </button>
      )}
    </span>
  );
}
