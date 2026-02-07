"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import AuthForm from "@/components/AuthForm";
import { demoLogin, isAuthenticated } from "@/lib/auth";

function LoginContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState("");

  useEffect(() => {
    if (isAuthenticated()) {
      router.push("/tasks");
    }

    if (searchParams.get("expired") === "true") {
      setError("Your session has expired. Please login again.");
    }
  }, [router, searchParams]);

  const handleLogin = async (email: string, _password: string) => {
    try {
      setError("");
      // For demo, we use simple login without password verification
      await demoLogin(email);
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
        <p className="text-gray-600">Login to access your tasks</p>
      </div>

      <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
        <AuthForm mode="login" onSubmit={handleLogin} error={error} />

        <div className="mt-6 text-center text-sm text-gray-600">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="text-blue-600 hover:underline">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="text-center py-8">Loading...</div>}>
      <LoginContent />
    </Suspense>
  );
}
