from app.services.cache_service import CacheService


def test_build_key_is_stable() -> None:
    service = CacheService()
    value = "What is pgvector?"

    key_1 = service.build_key("llm", value)
    key_2 = service.build_key("llm", value)

    assert key_1 == key_2


def test_build_key_changes_for_different_values() -> None:
    service = CacheService()

    key_1 = service.build_key("llm", "question one")
    key_2 = service.build_key("llm", "question two")

    assert key_1 != key_2


def test_build_key_contains_prefix() -> None:
    service = CacheService()

    key = service.build_key("embedding", "some text")

    assert key.startswith("embedding:")


def test_build_key_does_not_contain_raw_value() -> None:
    service = CacheService()
    raw_value = "very long and potentially sensitive user input"

    key = service.build_key("llm", raw_value)

    assert raw_value not in key
