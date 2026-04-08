const BASE_URL = "http://localhost:8000";

export async function startConversation(): Promise<number> {
  const res = await fetch(`${BASE_URL}/agent/conversations`, { method: "POST" });
  const data = await res.json();
  return data.conversation_id;
}

export async function sendMessage(conversationId: number, content: string): Promise<string> {
  const res = await fetch(`${BASE_URL}/agent/conversations/${conversationId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  const data = await res.json();
  return data.content;
}
