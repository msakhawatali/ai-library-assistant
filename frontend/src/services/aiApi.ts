interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface ChatResponse {
  response: string;
  conversation_id: string;
}

const API_URL = "http://127.0.0.1:8000/api/ai/chat";

export async function sendChatMessage(
  message: string,
  conversationId: string
): Promise<ChatResponse> {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    throw new Error("Request failed");
  }

  const data: ChatResponse = await response.json();
  return data;
}

export type { ChatMessage, ChatResponse };