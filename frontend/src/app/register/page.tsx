"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import AuthForm from "@/components/AuthForm";
import { demoLogin, isAuthenticated } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState("");

  useEffect(() => {
    if (isAuthenticated()) {
      router.push("/tasks");
    }
  }, [router]);

  const handleRegister = async (email: string, _password: string) => {
    try {
      setError("");
      // For demo, registration is the same as login
      await demoLogin(email);
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h1>
        <p className="text-gray-600">Start managing your tasks today</p>
      </div>

      <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
        <AuthForm mode="register" onSubmit={handleRegister} error={error} />

        <div className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-600 hover:underline">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}
