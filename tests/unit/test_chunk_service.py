from app.services.chunk_service import ChunkService


class FakeChunkRepository:
    pass


def test_split_text_returns_one_chunk_for_short_text() -> None:
    service = ChunkService(repo=FakeChunkRepository())
    text = "Short text."

    chunks = service.split_text(text, chunk_size=500, overlap=50)

    assert chunks == ["Short text."]


def test_split_text_returns_non_empty_chunks() -> None:
    service = ChunkService(repo=FakeChunkRepository())
    text = "word " * 300

    chunks = service.split_text(text, chunk_size=100, overlap=20)

    assert chunks
    assert all(chunk.strip() for chunk in chunks)


def test_split_text_splits_long_text_into_multiple_chunks() -> None:
    service = ChunkService(repo=FakeChunkRepository())
    text = "word " * 300

    chunks = service.split_text(text, chunk_size=100, overlap=20)

    assert len(chunks) > 1


def test_split_text_does_not_exceed_chunk_size() -> None:
    service = ChunkService(repo=FakeChunkRepository())
    text = "word " * 300
    chunk_size = 100

    chunks = service.split_text(text, chunk_size=chunk_size, overlap=20)

    assert all(len(chunk) <= chunk_size for chunk in chunks)
