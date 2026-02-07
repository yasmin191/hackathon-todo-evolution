"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getSession, logout, isAuthenticated } from "@/lib/auth";
import ChatInterface from "@/components/ChatInterface";

export default function ChatPage() {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState<string>("");
  const [conversationId, setConversationId] = useState<number | undefined>();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
      return;
    }

    const session = getSession();
    if (session) {
      setUserEmail(session.user.email);
    }
  }, [router]);

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  const handleNewChat = () => {
    setConversationId(undefined);
    // Force re-render by using a key
    window.location.reload();
  };

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Chat Assistant</h1>
          <p className="text-sm text-gray-500">{userEmail}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleNewChat}
            className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
          >
            New Chat
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex gap-4 mb-6">
        <Link
          href="/tasks"
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          View Tasks
        </Link>
        <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg">
          Chat Assistant
        </span>
      </div>

      {/* Chat Interface */}
      <ChatInterface
        conversationId={conversationId}
        onConversationCreated={(id) => setConversationId(id)}
      />

      {/* Help text */}
      <div className="mt-4 text-center text-sm text-gray-500">
        <p>
          Try saying: &quot;Add a task to buy groceries&quot; or &quot;Show my tasks&quot;
        </p>
      </div>
    </div>
  );
}
