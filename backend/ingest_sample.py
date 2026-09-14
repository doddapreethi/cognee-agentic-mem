import asyncio

from app.memory_service import ingest_sample_chunks


async def main() -> None:
    print("\n========================================")
    print("       COGNEE SAMPLE INGESTION")
    print("========================================")
    print("Starting ingestion...\n")

    try:
        result = await ingest_sample_chunks()

        print("\n========================================")
        print("       INGESTION COMPLETED")
        print("========================================")
        print(f"Status : {result.get('status', 'success')}")
        print(f"Chunks : {result.get('count', 0)}")
        print(f"Dataset: {result.get('dataset', 'private_memory')}")
        print("========================================\n")

    except Exception as exc:
        print("\n========================================")
        print("       INGESTION FAILED")
        print("========================================")
        print(f"Error: {exc}")
        print("========================================\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())