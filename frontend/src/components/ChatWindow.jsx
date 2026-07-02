import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="flex-1 overflow-hidden">

      <div
        className="
          h-full
          overflow-y-auto
          rounded-2xl
          border
          border-gray-200
          bg-gray-50
          p-6
          shadow-sm
        "
      >

        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            role={msg.role}
            text={msg.content}
          />
        ))}

        {loading && (
          <div className="flex gap-3 mb-6">

            <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white">
              🤖
            </div>

            <div className="bg-white rounded-2xl px-5 py-4 shadow border">

              <p className="font-semibold text-gray-700 mb-2">
                SHL Recruit AI
              </p>

              <div className="flex gap-2">

                <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></span>

                <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-100"></span>

                <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-200"></span>

              </div>

            </div>

          </div>
        )}

        <div ref={bottomRef} />

      </div>

    </div>
  );
}