from robot_experience_memory.store import ExperienceBundle, MemoryStore


def test_memory_store_interface_exports_expected_methods() -> None:
    assert MemoryStore.put.__name__ == "put"
    assert MemoryStore.get.__name__ == "get"
    assert MemoryStore.list.__name__ == "list"


def test_experience_bundle_export_is_available() -> None:
    assert ExperienceBundle.__name__ == "ExperienceBundle"
