export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface BirthDetails {
  birth_date: string;
  birth_time: string;
  birth_place: string;
}

export interface ChatRequest {
  session_id: string;
  message: string;
}

export interface StreamChunk {
  token: string;
}