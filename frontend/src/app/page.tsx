"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";
import Link from "next/link";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.push("/tasks");
    }
  }, [router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Todo App
      </h1>
      <p className="text-lg text-gray-600 mb-8 max-w-md">
        A full-stack todo application built with Next.js and FastAPI.
        Manage your tasks efficiently with our simple interface.
      </p>
      <div className="flex gap-4">
        <Link
          href="/login"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Login
        </Link>
        <Link
          href="/register"
          className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
        >
          Register
        </Link>
      </div>
    </div>
  );
}
