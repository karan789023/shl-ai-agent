import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim() || disabled) return;

    onSend(text);
    setText("");
  };

  return (
    <div className="sticky bottom-0 bg-white border-t border-gray-200 p-4">

      <div className="flex items-end gap-3 max-w-6xl mx-auto">

        <textarea
          rows={1}
          value={text}
          disabled={disabled}
          placeholder="Ask about SHL assessments..."
          className="
            flex-1
            resize-none
            rounded-2xl
            border
            border-gray-300
            px-5
            py-3
            outline-none
            focus:border-blue-500
            focus:ring-2
            focus:ring-blue-200
            text-gray-700
            shadow-sm
          "
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <button
          onClick={handleSend}
          disabled={disabled}
          className="
            rounded-2xl
            bg-blue-600
            px-6
            py-3
            font-semibold
            text-white
            shadow-md
            transition
            hover:bg-blue-700
            disabled:cursor-not-allowed
            disabled:bg-gray-400
          "
        >
          {disabled ? "Thinking..." : "Send"}
        </button>

      </div>

    </div>
  );
}