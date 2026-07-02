import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ChatMessage({ role, text }) {
  const isUser = role === "user";

  return (
    <div
      className={`flex mb-6 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="mr-3 flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white text-lg shadow">
          🤖
        </div>
      )}

      <div
        className={`
          max-w-4xl
          rounded-2xl
          px-5
          py-4
          shadow-md
          ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-white border border-gray-200 text-gray-900"
          }
        `}
      >
        {!isUser && (
          <div className="mb-3 border-b pb-2">
            <h3 className="font-bold text-blue-600">
              SHL Recruit AI
            </h3>
          </div>
        )}

        {isUser ? (
          <p className="whitespace-pre-wrap leading-7">
            {text}
          </p>
        ) : (
          <article className="prose prose-sm max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {text}
            </ReactMarkdown>
          </article>
        )}
      </div>

      {isUser && (
        <div className="ml-3 flex h-10 w-10 items-center justify-center rounded-full bg-gray-800 text-white text-lg shadow">
          👤
        </div>
      )}
    </div>
  );
}