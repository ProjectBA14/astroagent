import { create } from "zustand";

import type {
  ChatMessage,
  BirthDetails
} from "../types/chat";

interface ChatStore {

  sessionId: string | null;

  initialized: boolean;

  birthDetails: BirthDetails | null;

  messages: ChatMessage[];

  isStreaming: boolean;

  setSession: (
    sessionId: string,
    birthDetails: BirthDetails
  ) => void;

  addMessage: (
    message: ChatMessage
  ) => void;

  setStreaming: (
    value: boolean
  ) => void;
}

export const useChatStore =
  create<ChatStore>((set) => ({

    sessionId: null,

    initialized: false,

    birthDetails: null,

    messages: [],

    isStreaming: false,

    setSession: (
      sessionId,
      birthDetails
    ) =>

      set({

        sessionId,

        birthDetails,

        initialized: true
      }),

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