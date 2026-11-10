import asyncio
from app.database import connect_db, close_db
from app.agent.tools import search_notes, SearchNotesInput


async def main():
    await connect_db()
    results = await search_notes(
        SearchNotesInput(query="What is a ml?")
    )
    print(f"✅ Matches found: {len(results)}")
    if results:
        top = results[0]
        print(f"📄 Top match file: {top['filename']} (Page {top['page']})")
        print(f"🎯 Similarity score: {top['score']}")
        print(f"📝 Preview:\n{top['text'][:1500]}...")
    else:
        print("⚠️ No chunks matched. Make sure you uploaded a note in Step 5!")

    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
