CREATE TABLE IF NOT EXISTS users (
    id      INTEGER PRIMARY KEY,
    email   TEXT NOT NULL UNIQUE
);

-- Seed the single user
INSERT OR IGNORE INTO users (id, email) VALUES (1, 'user@example.com');

CREATE TABLE IF NOT EXISTS conversations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    role            TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    amount      REAL NOT NULL,
    category    TEXT NOT NULL,
    description TEXT,
    date        DATE NOT NULL DEFAULT (DATE('now')),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
