
import json
from pathlib import Path

from .common import Review
from .single_agent import SingleAgent
from .multi_agent import Coordinator


def main():
    sample_review = Review(
        "The product is useful but the app is slow and frustrating."
    )

    print("\n" + "=" * 60)
    print("TOPIC 2: SINGLE-AGENT VS MULTI-AGENT ASSESSMENT")
    print("=" * 60)

    # Run Single-Agent
    single_agent = SingleAgent()

    print("\n\n######## SINGLE-AGENT EXECUTION ########")
    single_result = single_agent.run(sample_review)

    # Run Multi-Agent
    coordinator = Coordinator()

    print("\n\n######## MULTI-AGENT EXECUTION ########")
    multi_result = coordinator.run(
        review_text=sample_review.text,
        simulate_disagreement=True,
    )

    # Compare both architectures
    comparison = {
        "same_sentiment": (
            single_result["sentiment"] == multi_result["sentiment"]
        ),
        "same_issue": (
            single_result["issue"] == multi_result["issue"]
        ),
        "same_recommendation": (
            single_result["recommendation"]
            == multi_result["recommendation"]
        ),
        "single_agent_stages": len(
            single_result["execution_log"]
        ),
        "multi_agent_events": len(
            multi_result["execution_log"]
        ),
        "multi_agent_messages": multi_result["message_count"],
        "single_agent_specialists": 1,
        "multi_agent_specialists": 2,
    }

    print("\n\n######## ARCHITECTURE COMPARISON ########")

    for key, value in comparison.items():
        print(f"{key}: {value}")

    # Prepare evidence
    evidence = {
        "input_review": sample_review.text,
        "single_agent": single_result,
        "multi_agent": multi_result,
        "comparison": comparison,
    }

    # Save JSON evidence
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "comparison_evidence.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(evidence, file, indent=4)

    print(f"\n[EVIDENCE] Saved to {output_file}")
    print("\n[COMPARISON COMPLETED]")


if __name__ == "__main__":
    main()
