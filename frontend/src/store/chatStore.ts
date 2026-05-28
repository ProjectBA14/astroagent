import { create } from "zustand";

import type {
  ChatMessage
} from "../types/chat";


interface ChatStore {

  messages: ChatMessage[];

  isStreaming: boolean;

  addMessage: (
    message: ChatMessage
  ) => void;

  setStreaming: (
    value: boolean
  ) => void;
}

export const useChatStore =
  create<ChatStore>((set) => ({

    messages: [],

    isStreaming: false,

    addMessage: (message) =>

      set((state) => ({

        messages: [
          ...state.messages,
          message
        ]
      })),

    setStreaming: (value) =>

      set({
        isStreaming: value
      })
}));