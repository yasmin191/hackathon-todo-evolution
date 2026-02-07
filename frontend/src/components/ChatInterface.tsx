"use client";

import { useState, useRef, useEffect, FormEvent } from "react";
import { api, Message } from "@/lib/api";

interface ChatInterfaceProps {
  conversationId?: number;
  onConversationCreated?: (id: number) => void;
}

interface ChatMessage {
  id: number | string;
  role: "user" | "assistant";
  content: string;
  pending?: boolean;
}

export default function ChatInterface({
  conversationId,
  onConversationCreated,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentConversationId, setCurrentConversationId] = useState<
    number | undefined
  >(conversationId);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load existing messages if conversationId provided
  useEffect(() => {
    if (conversationId) {
      loadMessages(conversationId);
    } else {
      // Show welcome message for new conversation
      setMessages([
        {
          id: "welcome",
          role: "assistant",
          content:
            "Hello! I'm your task assistant. You can ask me to:\n\n• Add tasks (e.g., \"Add a task to buy groceries\")\n• Show your tasks (e.g., \"What do I need to do?\")\n• Complete tasks (e.g., \"Mark task 1 as complete\")\n• Delete tasks (e.g., \"Delete task 2\")\n\nHow can I help you today?",
        },
      ]);
    }
  }, [conversationId]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadMessages = async (convId: number) => {
    try {
      const msgs = await api.getMessages(convId);
      setMessages(
        msgs.map((m: Message) => ({
          id: m.id,
          role: m.role,
          content: m.content,
        }))
      );
      setCurrentConversationId(convId);
    } catch (err) {
      setError("Failed to load messages");
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setError(null);

    // Add user message to UI immediately
    const tempId = `temp-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: tempId, role: "user", content: userMessage },
      { id: "pending", role: "assistant", content: "", pending: true },
    ]);

    setLoading(true);

    try {
      const response = await api.sendMessage(userMessage, currentConversationId);

      // Update conversation ID if this is a new conversation
      if (!currentConversationId) {
        setCurrentConversationId(response.conversation_id);
        onConversationCreated?.(response.conversation_id);
      }

      // Replace pending message with actual response
      setMessages((prev) =>
        prev
          .filter((m) => m.id !== "pending")
          .concat({
            id: response.message_id,
            role: "assistant",
            content: response.response,
          })
      );
    } catch (err) {
      // Remove pending message and show error
      setMessages((prev) => prev.filter((m) => m.id !== "pending"));
      setError(err instanceof Error ? err.message : "Failed to send message");
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-900"
              } ${message.pending ? "animate-pulse" : ""}`}
            >
              {message.pending ? (
                <div className="flex items-center gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                  <span
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></span>
                  <span
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></span>
                </div>
              ) : (
                <p className="whitespace-pre-wrap">{message.content}</p>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Error message */}
      {error && (
        <div className="px-4 py-2 bg-red-50 border-t border-red-200">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Input area */}
      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-200 p-4 flex gap-2"
      >
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={loading}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}
