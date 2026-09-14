"""
Application configuration for the local Cognee memory application.

IMPORTANT:
- Load .env before importing Cognee.
- Normalize filesystem paths to absolute paths.
- Export Cognee settings before Cognee is imported.
- This file MUST NOT import cognee.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


# ============================================================================
# LOAD ENVIRONMENT
# ============================================================================

load_dotenv(
    ENV_FILE,
    override=True,
)

# Prevent Cognee from loading .env a second time.
os.environ["PYTHON_DOTENV_DISABLED"] = "1"


# ============================================================================
# HELPERS
# ============================================================================

def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _absolute_path(value: str | None, fallback: str) -> str:
    raw_value = value or fallback

    path = Path(raw_value).expanduser()

    if not path.is_absolute():
        path = PROJECT_ROOT / path

    path = path.resolve()

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return str(path)


# ============================================================================
# STORAGE
# ============================================================================

DATA_ROOT_DIRECTORY = _absolute_path(
    _env("DATA_ROOT_DIRECTORY"),
    "C:/cognee/data",
)

SYSTEM_ROOT_DIRECTORY = _absolute_path(
    _env("SYSTEM_ROOT_DIRECTORY"),
    "C:/cognee/system",
)

CACHE_ROOT_DIRECTORY = _absolute_path(
    _env("CACHE_ROOT_DIRECTORY"),
    "C:/cognee/cache",
)

COGNEE_LOGS_DIR = _absolute_path(
    _env("COGNEE_LOGS_DIR"),
    "C:/cognee/logs",
)

VECTOR_DB_URL = _absolute_path(
    _env("VECTOR_DB_URL"),
    "C:/cognee/lancedb",
)


os.environ["DATA_ROOT_DIRECTORY"] = DATA_ROOT_DIRECTORY
os.environ["SYSTEM_ROOT_DIRECTORY"] = SYSTEM_ROOT_DIRECTORY
os.environ["CACHE_ROOT_DIRECTORY"] = CACHE_ROOT_DIRECTORY
os.environ["COGNEE_LOGS_DIR"] = COGNEE_LOGS_DIR
os.environ["VECTOR_DB_URL"] = VECTOR_DB_URL


# ============================================================================
# API SERVER
# ============================================================================

BACKEND_HOST = _env(
    "BACKEND_HOST",
    "127.0.0.1",
)

BACKEND_PORT = int(
    _env(
        "BACKEND_PORT",
        "8000",
    )
)

HOST = BACKEND_HOST
PORT = BACKEND_PORT

FRONTEND_HOST = _env(
    "FRONTEND_HOST",
    "127.0.0.1",
)

FRONTEND_PORT = int(
    _env(
        "FRONTEND_PORT",
        "3000",
    )
)

FRONTEND_ORIGIN = (
    f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"
)


# ============================================================================
# LOCAL STORAGE
# ============================================================================

STORAGE_BACKEND = _env(
    "STORAGE_BACKEND",
    "local",
)

os.environ["STORAGE_BACKEND"] = STORAGE_BACKEND


# ============================================================================
# LLM - OLLAMA
# ============================================================================

LLM_PROVIDER = _env(
    "LLM_PROVIDER",
    "ollama",
)

LLM_MODEL = _env(
    "LLM_MODEL",
    "ollama/llama3.1:8b",
)

LLM_ENDPOINT = _env(
    "LLM_ENDPOINT",
    "http://127.0.0.1:11434",
)

LLM_API_KEY = _env(
    "LLM_API_KEY",
    "ollama",
)

LLM_TEMPERATURE = _env(
    "LLM_TEMPERATURE",
    "0.0",
)

LLM_MAX_TOKENS = _env(
    "LLM_MAX_TOKENS",
    "2048",
)

LLM_INSTRUCTOR_MODE = _env(
    "LLM_INSTRUCTOR_MODE",
    "json_mode",
)

COGNEE_SKIP_CONNECTION_TEST = _env(
    "COGNEE_SKIP_CONNECTION_TEST",
    "true",
)

os.environ["LLM_PROVIDER"] = LLM_PROVIDER
os.environ["LLM_MODEL"] = LLM_MODEL
os.environ["LLM_ENDPOINT"] = LLM_ENDPOINT
os.environ["LLM_API_KEY"] = LLM_API_KEY
os.environ["LLM_TEMPERATURE"] = LLM_TEMPERATURE
os.environ["LLM_MAX_TOKENS"] = LLM_MAX_TOKENS
os.environ["LLM_INSTRUCTOR_MODE"] = LLM_INSTRUCTOR_MODE
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = (
    COGNEE_SKIP_CONNECTION_TEST
)


# ============================================================================
# STRUCTURED OUTPUT
# ============================================================================

STRUCTURED_OUTPUT_FRAMEWORK = _env(
    "STRUCTURED_OUTPUT_FRAMEWORK",
    "litellm_native",
)

os.environ["STRUCTURED_OUTPUT_FRAMEWORK"] = (
    STRUCTURED_OUTPUT_FRAMEWORK
)


# ============================================================================
# EMBEDDINGS
# ============================================================================

EMBEDDING_PROVIDER = _env(
    "EMBEDDING_PROVIDER",
    "ollama",
)

EMBEDDING_MODEL = _env(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)

EMBEDDING_ENDPOINT = _env(
    "EMBEDDING_ENDPOINT",
    "http://127.0.0.1:11434/api/embed",
)

EMBEDDING_DIMENSIONS = int(
    _env(
        "EMBEDDING_DIMENSIONS",
        "768",
    )
)

EMBEDDING_API_KEY = _env(
    "EMBEDDING_API_KEY",
    "ollama",
)

HUGGINGFACE_TOKENIZER = _env(
    "HUGGINGFACE_TOKENIZER",
    "nomic-ai/nomic-embed-text-v1.5",
)

os.environ["EMBEDDING_PROVIDER"] = EMBEDDING_PROVIDER
os.environ["EMBEDDING_MODEL"] = EMBEDDING_MODEL
os.environ["EMBEDDING_ENDPOINT"] = EMBEDDING_ENDPOINT
os.environ["EMBEDDING_DIMENSIONS"] = str(
    EMBEDDING_DIMENSIONS
)
os.environ["EMBEDDING_API_KEY"] = EMBEDDING_API_KEY
os.environ["HUGGINGFACE_TOKENIZER"] = (
    HUGGINGFACE_TOKENIZER
)


# ============================================================================
# DATABASES
# ============================================================================

DB_PROVIDER = _env(
    "DB_PROVIDER",
    "sqlite",
)

VECTOR_DB_PROVIDER = _env(
    "VECTOR_DB_PROVIDER",
    "lancedb",
)

VECTOR_DATASET_DATABASE_HANDLER = _env(
    "VECTOR_DATASET_DATABASE_HANDLER",
    "lancedb",
)

GRAPH_DATABASE_PROVIDER = _env(
    "GRAPH_DATABASE_PROVIDER",
    "kuzu",
)

VECTOR_DB_SUBPROCESS_ENABLED = (
    _env(
        "VECTOR_DB_SUBPROCESS_ENABLED",
        "false",
    ).lower()
    in {
        "1",
        "true",
        "yes",
        "on",
    }
)

os.environ["DB_PROVIDER"] = DB_PROVIDER
os.environ["VECTOR_DB_PROVIDER"] = VECTOR_DB_PROVIDER
os.environ["VECTOR_DATASET_DATABASE_HANDLER"] = (
    VECTOR_DATASET_DATABASE_HANDLER
)
os.environ["GRAPH_DATABASE_PROVIDER"] = (
    GRAPH_DATABASE_PROVIDER
)
os.environ["VECTOR_DB_SUBPROCESS_ENABLED"] = (
    str(VECTOR_DB_SUBPROCESS_ENABLED).lower()
)


# ============================================================================
# PRIVACY / SECURITY
# ============================================================================

TELEMETRY_DISABLED = _env(
    "TELEMETRY_DISABLED",
    "1",
)

os.environ["TELEMETRY_DISABLED"] = (
    TELEMETRY_DISABLED
)

ENABLE_BACKEND_ACCESS_CONTROL = (
    _env(
        "ENABLE_BACKEND_ACCESS_CONTROL",
        "true",
    ).lower()
    in {
        "1",
        "true",
        "yes",
        "on",
    }
)

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = (
    str(
        ENABLE_BACKEND_ACCESS_CONTROL
    ).lower()
)

BACKEND_API_TOKEN = _env(
    "BACKEND_API_TOKEN",
)


# ============================================================================
# DATASET
# ============================================================================

MEMORY_DATASET = _env(
    "MEMORY_DATASET",
    "private_memory",
)


# ============================================================================
# DEBUG HELPERS
# ============================================================================

def storage_summary() -> dict[str, str]:
    return {
        "project_root": str(PROJECT_ROOT),
        "data_root": DATA_ROOT_DIRECTORY,
        "system_root": SYSTEM_ROOT_DIRECTORY,
        "cache_root": CACHE_ROOT_DIRECTORY,
        "logs_dir": COGNEE_LOGS_DIR,
        "vector_db_url": VECTOR_DB_URL,
        "storage_backend": STORAGE_BACKEND,
        "vector_db_provider": VECTOR_DB_PROVIDER,
        "graph_database_provider": GRAPH_DATABASE_PROVIDER,
        "vector_db_subprocess_enabled": (
            str(VECTOR_DB_SUBPROCESS_ENABLED)
        ),
        "dataset": MEMORY_DATASET,
    }


def llm_summary() -> dict[str, str]:
    return {
        "provider": LLM_PROVIDER,
        "model": LLM_MODEL,
        "endpoint": LLM_ENDPOINT,
        "structured_output_framework": (
            STRUCTURED_OUTPUT_FRAMEWORK
        ),
        "instructor_mode": LLM_INSTRUCTOR_MODE,
    }


# ============================================================================
# DO NOT IMPORT COGNEE IN THIS FILE
# ============================================================================