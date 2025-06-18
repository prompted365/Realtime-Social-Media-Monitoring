import argparse
import asyncio

from orchestrator.core import ScraperOrchestrator
from analytics.sentiment import analyze
from database.storage import store_raw, store_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Run scraping agents")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Number of posts per agent")
    parser.add_argument("--raw-table", default="scraped", help="Database table for raw data")
    parser.add_argument(
        "--analysis-table",
        default="analysis",
        help="Database table for sentiment results",
    )
    args = parser.parse_args()

    orchestrator = ScraperOrchestrator()
    orchestrator.load_agents()

    df = asyncio.run(orchestrator.scrape_and_analyze(args.query, args.limit, analyze))

    store_raw(args.raw_table, df[["source", "text"]].itertuples(index=False, name=None))
    store_analysis(args.analysis_table, df)
    print(df)
    print("Metrics:", df.attrs.get("metrics"))


if __name__ == "__main__":
    main()
