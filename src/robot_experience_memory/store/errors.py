"""Store-specific exceptions."""


class MemoryStoreError(Exception):
    """Base exception for memory store failures."""


class DuplicateExperienceError(MemoryStoreError):
    """Raised when a store rejects a duplicate experience ID."""

    def __init__(self, experience_id: str) -> None:
        super().__init__(f"experience already exists: {experience_id}")
        self.experience_id = experience_id


class ExperienceNotFoundError(MemoryStoreError):
    """Raised when a required experience cannot be found."""

    def __init__(self, experience_id: str) -> None:
        super().__init__(f"experience not found: {experience_id}")
        self.experience_id = experience_id


class StoreConfigurationError(MemoryStoreError):
    """Raised when a store is configured with invalid settings."""
