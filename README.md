# AI Knowledge Base (RAG)
## Описание проекта

Асинхронный backend-сервис, который позволяет загружать документы, сохранять их в базу данных, создавать embeddings, выполнять векторный поиск и отвечать на вопросы по документам с использованием LLM (RAG — Retrieval-Augmented Generation).

### Стек:
- FastAPI
- PostgreSQL
- pgvector
- Redis
- Celery
- Alembic
- Docker
- OpenAI API / Local LLM
- Async SQLAlchemy