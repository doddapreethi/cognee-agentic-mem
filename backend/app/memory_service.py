from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import config
import cognee


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "sample_data"
    / "chunks.json"
)

DATASET_NAME = config.MEMORY_DATASET


async def remember(text: str) -> Any:
    text = text.strip()

    if not text:
        raise ValueError("Memory text cannot be empty.")

    return await cognee.remember(
        data=text,
        dataset_name=DATASET_NAME,
        self_improvement=False,
    )


async def recall(query: str, top_k: int = 5) -> Any:
    query = query.strip()

    if not query:
        raise ValueError("Recall query cannot be empty.")

    # IMPORTANT:
    # Do not let Cognee auto-route the query.
    # Auto-routing can select GRAPH_COMPLETION_CONTEXT_EXTENSION,
    # which is much more expensive for local Ollama inference.
    return await cognee.recall(
        query_text=query,
        datasets=[DATASET_NAME],
        query_type=cognee.SearchType.HYBRID_COMPLETION,
        top_k=top_k,
    )


async def improve() -> Any:
    return await cognee.improve(
        dataset=DATASET_NAME
    )


async def forget() -> Any:
    return await cognee.forget(
        dataset=DATASET_NAME
    )


async def ingest_sample_chunks() -> dict:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Sample data file not found: {DATA_FILE}"
        )

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    texts: list[str] = []

    for item in items:
        if isinstance(item, str):
            text = item.strip()

        elif isinstance(item, dict):
            text = str(item.get("text", "")).strip()

        else:
            continue

        if text:
            texts.append(text)

    if not texts:
        return {
            "status": "error",
            "message": "No valid chunks found.",
            "count": 0,
            "dataset": DATASET_NAME,
        }

    print(f"Loaded {len(texts)} sample chunks.")

    print("Step 1/2: Adding data to Cognee...")

    add_result = await cognee.add(
        data=texts,
        dataset_name=DATASET_NAME,
    )

    print("Step 1/2 completed.")

    print("Step 2/2: Building knowledge graph...")

    cognify_result = await cognee.cognify(
        datasets=[DATASET_NAME]
    )

    print("Step 2/2 completed.")

    return {
        "status": "success",
        "count": len(texts),
        "dataset": DATASET_NAME,
        "add_result": add_result,
        "cognify_result": cognify_result,
    }