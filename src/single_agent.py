
from .common import Review


class SingleAgent:
    """
    One agent performs the complete product-review workflow:
    sentiment analysis, issue detection, and recommendation.
    """

    def __init__(self, name="SingleAgent"):
        self.name = name
        self.execution_log = []

    def _log_stage(self, stage):
        """Record and display each execution stage."""

        self.execution_log.append(stage)
        print(f"[LOG] {self.name}: {stage}")

    def run(self, review: Review) -> dict:
        """Analyze a product review and return a structured result."""

        if not isinstance(review, Review):
            raise TypeError("Input must be a Review object.")

        if not isinstance(review.text, str) or not review.text.strip():
            raise ValueError("Review text cannot be empty.")

        self.execution_log = []

        print(f"\n[START] {self.name}")

        self._log_stage("Input received")

        text = review.text.lower()

        # Stage 1: Analyze sentiment
        self._log_stage("Analyzing sentiment")

        negative_words = {
            "bad",
            "poor",
            "slow",
            "broken",
            "frustrating",
        }

        sentiment = (
            "negative"
            if any(word in text for word in negative_words)
            else "positive"
        )

        # Stage 2: Detect the main issue
        self._log_stage("Detecting main issue")

        issue = "performance" if "slow" in text else "general"

        # Stage 3: Generate recommendation
        self._log_stage("Generating recommendation")

        recommendation = (
            "Investigate application performance."
            if issue == "performance"
            else "Continue monitoring customer feedback."
        )

        # Stage 4: Complete execution and build structured result
        self._log_stage("Execution completed")

        result = {
            "sentiment": sentiment,
            "issue": issue,
            "recommendation": recommendation,
            "architecture": "single-agent",
            "execution_log": self.execution_log.copy(),
        }

        print(f"[RESULT] {result}")

        return result