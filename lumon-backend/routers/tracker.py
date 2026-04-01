from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from db.database import get_connection

router = APIRouter(prefix="/tracker", tags=["tracker"])

USER_ID = 1  # single user for now


class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: Optional[str] = None  # ISO format: YYYY-MM-DD


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None


# --- Transactions ---

@router.get("/transactions")
def list_transactions():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC",
            (USER_ID,)
        ).fetchall()
    return [dict(row) for row in rows]


@router.post("/transactions", status_code=201)
def add_transaction(body: TransactionCreate):
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO transactions (user_id, amount, category, description, date)
               VALUES (?, ?, ?, ?, COALESCE(?, DATE('now')))""",
            (USER_ID, body.amount, body.category, body.description, body.date)
        )
        transaction_id = cursor.lastrowid
    return {"id": transaction_id, **body.model_dump()}


@router.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, body: TransactionUpdate):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [transaction_id, USER_ID]

    with get_connection() as conn:
        conn.execute(
            f"UPDATE transactions SET {set_clause} WHERE id = ? AND user_id = ?",
            values
        )
    return {"updated": transaction_id}


@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM transactions WHERE id = ? AND user_id = ?",
            (transaction_id, USER_ID)
        )
    return {"deleted": transaction_id}


# --- Summary ---

@router.get("/summary")
def get_summary():
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT category, SUM(amount) as total, COUNT(*) as count
               FROM transactions WHERE user_id = ?
               GROUP BY category ORDER BY total DESC""",
            (USER_ID,)
        ).fetchall()
    return [dict(row) for row in rows]


# --- User Data (stubs) ---

@router.get("/user")
def get_user():
    # TODO: return user profile data
    pass


@router.put("/user")
def update_user():
    # TODO: update user profile (name, email, preferences, etc.)
    pass


@router.get("/user/accounts")
def get_accounts():
    # TODO: return user's linked financial accounts
    pass


@router.post("/user/accounts")
def add_account():
    # TODO: add a new financial account for the user
    pass


@router.delete("/user/accounts/{account_id}")
def delete_account(account_id: int):
    # TODO: remove a financial account
    pass
