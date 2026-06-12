"""Backend configuration and factory helpers."""

from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store.base import MemoryStore
from robot_experience_memory.store.errors import StoreConfigurationError
from robot_experience_memory.store.jsonl import JSONLMemoryStore
from robot_experience_memory.store.memory import InMemoryStore
from robot_experience_memory.store.sqlite import SQLiteMemoryStore

StoreBackend = Literal["memory", "jsonl", "sqlite"]


class StoreConfig(MemoryModel):
    """Configuration for selecting a memory store backend."""

    backend: StoreBackend = "memory"
    path: Path | None = Field(default=None)

    @model_validator(mode="after")
    def validate_path(self) -> "StoreConfig":
        """Require a path for durable backends."""
        if self.backend in {"jsonl", "sqlite"} and self.path is None:
            msg = f"path is required for {self.backend} backend"
            raise ValueError(msg)
        return self


def create_memory_store(config: StoreConfig) -> MemoryStore:
    """Create a memory store from backend configuration."""
    if config.backend == "memory":
        return InMemoryStore()
    if config.backend == "jsonl":
        if config.path is None:
            raise StoreConfigurationError("path is required for jsonl backend")
        return JSONLMemoryStore(config.path)
    if config.backend == "sqlite":
        if config.path is None:
            raise StoreConfigurationError("path is required for sqlite backend")
        return SQLiteMemoryStore(config.path)
    raise StoreConfigurationError(f"unsupported backend: {config.backend}")
