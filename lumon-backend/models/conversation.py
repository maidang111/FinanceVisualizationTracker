import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic
from dotenv import load_dotenv
from db.database import get_connection, init_db

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def start_conversation(user_id: int) -> int:
    """Create a new conversation row and return its id."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO conversations (user_id) VALUES (?)", (user_id,)
        )
        return cursor.lastrowid
    
def delete_conversation(user_id: int, conversation_id: int):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM messages WHERE conversation_id = ?", (conversation_id,)
        )
        conn.execute(
            "DELETE FROM conversations WHERE id = ? AND user_id = ?", (conversation_id, user_id)
        )


def load_history(conversation_id: int) -> list[dict]:
    """Load all messages for a conversation in order."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY created_at",
            (conversation_id,)
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in rows]


def save_message(conversation_id: int, role: str, content: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, role, content)
        )


def send_message(user_message: str, conversation_id: int) -> str:
    history = load_history(conversation_id)
    messages = history + [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=messages
    )

    assistant_reply = response.content[0].text

    save_message(conversation_id, "user", user_message)
    save_message(conversation_id, "assistant", assistant_reply)

    return assistant_reply

if __name__ == "__main__":
    init_db()

    USER_ID = 1
    conversation_id = start_conversation(USER_ID)
    print(f"Started conversation {conversation_id}")

    reply = send_message("Hello! Can you help me track my savings?", conversation_id)
    print(f"Assistant: {reply}")

    reply = send_message("What did I ask you just now?", conversation_id)
    print(f"Assistant: {reply}")

# passing in only the edited cells of the spread sheet
# check if the spread sheet has been edited first. if not we dont have to repass in the context
