import { useState } from "react";
import { sendMessage } from "../services/api";

import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

export default function Home() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "👋 Welcome to SHL Recruit AI.\n\nAsk me to recommend SHL assessments for any job role."
    }
  ]);

  const [loading, setLoading] = useState(false);

  const handleSend = async (text) => {

    if (!text.trim()) return;

    const updatedMessages = [
      ...messages,
      {
        role: "user",
        content: text,
      },
    ];

    setMessages(updatedMessages);

    setLoading(true);

    try {

      const data = await sendMessage(text);

      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);

    } catch (error) {

      console.error(error);

      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content:
            "❌ Unable to generate recommendations. Please try again.",
        },
      ]);

    } finally {

      setLoading(false);

    }
  };

  return (

    <div className="min-h-screen bg-slate-100">

      <Header />

      <main className="max-w-6xl mx-auto h-[calc(100vh-70px)] flex flex-col">

        <ChatWindow
          messages={messages}
          loading={loading}
        />

        <ChatInput
          onSend={handleSend}
          disabled={loading}
        />

      </main>

    </div>

  );

}