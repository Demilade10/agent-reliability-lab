from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class SQLiteMemory:
    """Small persistent key-value memory scoped by user."""

    def __init__(self, path: str | Path = "agent_memory.db") -> None:
        self.path = str(path)
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS memories (
                user_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                PRIMARY KEY (user_id, key)
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def set(self, user_id: str, key: str, value: Any) -> None:
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO memories(user_id, key, value) VALUES (?, ?, ?)
                ON CONFLICT(user_id, key) DO UPDATE SET value = excluded.value""",
                (user_id, key, json.dumps(value)),
            )

    def get(self, user_id: str, key: str) -> Any | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT value FROM memories WHERE user_id = ? AND key = ?", (user_id, key)
            ).fetchone()
        return None if row is None else json.loads(row[0])

