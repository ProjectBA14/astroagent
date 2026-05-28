import { useState } from "react";

import { API_BASE_URL }
  from "../lib/api";

import { getSessionId }
  from "../lib/session";

import {
  useChatStore
} from "../store/chatStore";

export default function ChatPage() {

  const [input, setInput] =
    useState("");

  const {
    messages,
    addMessage
  } = useChatStore();

  async function handleSend() {

    if (!input.trim()) return;

    const userMessage = input;

    addMessage({
      role: "user",
      content: userMessage
    });

    setInput("");

    addMessage({
      role: "assistant",
      content: ""
    });

    const response = await fetch(

      `${API_BASE_URL}/chat/stream`,

      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({

          session_id:
            getSessionId(),

          message:
            userMessage
        })
      }
    );

    if (!response.body) return;

    const reader =
      response.body.getReader();

    const decoder =
      new TextDecoder();

    let assistantText = "";

    while (true) {

      const {
        done,
        value
      } = await reader.read();

      if (done) break;

      const chunk =
        decoder.decode(value);

      const lines =
        chunk.split("\n");

      for (const line of lines) {

        if (
          line.startsWith("data:")
        ) {

          const jsonString =
            line.replace(
              "data:",
              ""
            );

          try {

            const parsed =
              JSON.parse(jsonString);

            assistantText +=
              parsed.token;

            useChatStore.setState(
              (state) => {

                const updated =
                  [...state.messages];

                updated[
                  updated.length - 1
                ] = {

                  role: "assistant",

                  content:
                    assistantText
                };

                return {
                  messages:
                    updated
                };
              }
            );

          } catch (err) {

            console.error(err);
          }
        }
      }
    }
  }

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      <div className="max-w-4xl mx-auto h-screen flex flex-col">

        {/* Header */}

        <div className="p-6 border-b border-slate-800">

          <h1 className="text-4xl font-bold">
            AstroAgent
          </h1>

          <p className="text-slate-400 mt-2">
            Calm astrology guidance grounded
            in your natal chart.
          </p>

        </div>

        {/* Messages */}

        <div className="flex-1 overflow-y-auto p-6 space-y-4">

          {messages.length === 0 && (

            <div className="text-slate-500">

              Ask AstroAgent anything
              about your chart.

            </div>
          )}

          {messages.map((message, index) => (

            <div
              key={index}
              className={
                message.role === "user"

                  ? "ml-auto max-w-xl bg-indigo-600 p-4 rounded-2xl"

                  : "mr-auto max-w-xl bg-slate-800 p-4 rounded-2xl"
              }
            >

              {message.content}

            </div>
          ))}

        </div>

        {/* Input */}

        <div className="p-6 border-t border-slate-800">

          <div className="flex gap-4">

            <input
              value={input}

              onChange={(e) =>
                setInput(
                  e.target.value
                )
              }

              onKeyDown={(e) => {

                if (e.key === "Enter") {

                  handleSend();
                }
              }}

              placeholder="Ask about your chart..."

              className="
                flex-1
                bg-slate-900
                border
                border-slate-700
                rounded-xl
                px-4
                py-3
                text-white
                outline-none
              "
            />

            <button
              onClick={handleSend}

              className="
                bg-indigo-600
                hover:bg-indigo-500
                px-6
                rounded-xl
                font-medium
              "
            >

              Send

            </button>

          </div>

        </div>

      </div>

    </div>
  );
}