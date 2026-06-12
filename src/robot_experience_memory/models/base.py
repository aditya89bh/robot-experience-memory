"""Shared model serialization support."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class MemoryModel(BaseModel):
    """Base class for immutable memory data models."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the model to a Python dictionary."""
        return self.model_dump(mode="json")

    def to_json(self) -> str:
        """Serialize the model to a JSON string."""
        return self.model_dump_json(indent=2)

    def to_file(self, path: str | Path) -> Path:
        """Serialize the model to a JSON file and return the written path."""
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(self.to_json() + "\n", encoding="utf-8")
        return destination
