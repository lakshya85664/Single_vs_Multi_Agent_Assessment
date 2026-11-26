
from .common import Message, log_message, validate_message


class Agent:
    """Base class for specialized agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def describe(self) -> str:
        return f"{self.name} ({self.role})"


class Analyst(Agent):
    """Analyzes sentiment and identifies the main issue."""

    def __init__(self):
        super().__init__("Analyst", "Analysis Specialist")

    def run(self, review_text: str) -> Message:
        print(f"\n[START] {self.describe()}")
        print("[ANALYST] Analyzing product review...")

        text = review_text.lower()

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

        issue = "performance" if "slow" in text else "general"

        message = Message(
            sender=self.name,
            receiver="Coordinator",
            task="analyze_review",
            payload={
                "sentiment": sentiment,
                "issue": issue,
                "evidence": [
                    word
                    for word in ("slow", "frustrating", "bad", "poor", "broken")
                    if word in text
                ],
            },
        )

        validate_message(message)

        print("[ANALYST] Analysis completed.")
        return message


class Reviewer(Agent):
    """Reviews the Analyst's result independently."""

    def __init__(self):
        super().__init__("Reviewer", "Quality Reviewer")

    def run(
        self,
        review_text: str,
        analysis: dict,
        simulate_disagreement: bool = False,
    ) -> Message:
        print(f"\n[START] {self.describe()}")
        print("[REVIEWER] Reviewing the Analyst's findings...")

        text = review_text.lower()

        # Independent review of the product review.
        issue = "performance" if "slow" in text else "general"

        # Optional controlled disagreement for assessment purposes.
        if simulate_disagreement:
            issue = "general"
            print(
                "[REVIEWER] Controlled disagreement enabled: "
                "Reviewer proposes a general issue."
            )

        message = Message(
            sender=self.name,
            receiver="Coordinator",
            task="review_analysis",
            payload={
                "issue": issue,
                "agrees": issue == analysis["issue"],
                "review_note": (
                    "Reviewer independently identified the issue."
                    if not simulate_disagreement
                    else "Controlled disagreement: Reviewer proposes a different issue."
                ),
            },
        )

        validate_message(message)

        print(f"[REVIEWER] Review completed: {message.payload}")
        return message


class Coordinator(Agent):
    """Coordinates delegation, handoff, conflict resolution, and results."""

    def __init__(self):
        super().__init__("Coordinator", "Orchestrator")
        self.analyst = Analyst()
        self.reviewer = Reviewer()
        self.execution_log = []
        self.message_log = []

    def record_event(self, event: str) -> None:
        self.execution_log.append(event)
        print(f"[LOG] {event}")

    def delegate(self, agent: Agent, task: str, review_text: str) -> Message:
        print(
            f"\n[DELEGATE] {self.name} -> {agent.name} | task={task}"
        )

        message = Message(
            sender=self.name,
            receiver=agent.name,
            task=task,
            payload={"review_text": review_text},
        )

        validate_message(message)
        log_message(message)
        self.message_log.append(message)

        self.record_event(f"Delegated {task} to {agent.name}")

        response = agent.run(review_text)

        validate_message(response)
        log_message(response)
        self.message_log.append(response)

        return response

    def handoff(
        self,
        analysis_message: Message,
    ) -> Message:
        """Pass the Analyst's structured output to the Reviewer."""

        print("\n[HANDOFF] Coordinator -> Reviewer")

        handoff_message = Message(
            sender=self.name,
            receiver=self.reviewer.name,
            task="review_analysis",
            payload={
                "analysis": analysis_message.payload,
                "original_review": self.original_review,
            },
        )

        validate_message(handoff_message)
        log_message(handoff_message)
        self.message_log.append(handoff_message)

        self.record_event("Handed Analyst output to Reviewer")

        review_message = self.reviewer.run(
            review_text=self.original_review,
            analysis=analysis_message.payload,
            simulate_disagreement=self.simulate_disagreement,
        )

        validate_message(review_message)
        log_message(review_message)
        self.message_log.append(review_message)

        return review_message

    def resolve_conflict(
        self,
        analysis: dict,
        review: dict,
        review_text: str,
    ) -> tuple[str, str]:
        """Resolve disagreement using a deterministic evidence rule."""

        analyst_issue = analysis["issue"]
        reviewer_issue = review["issue"]

        if analyst_issue == reviewer_issue:
            return analyst_issue, "Both agents agree on the identified issue."

        print("\n[CONFLICT] Analyst and Reviewer disagree.")
        print(f"[CONFLICT] Analyst issue: {analyst_issue}")
        print(f"[CONFLICT] Reviewer issue: {reviewer_issue}")

        # Evidence-priority rule:
        # Explicit 'slow' evidence takes priority for performance issues.
        if "slow" in review_text.lower():
            selected_issue = "performance"
            reason = (
                "Analyst selected because the original review contains "
                "explicit evidence of slow application performance."
            )
        else:
            selected_issue = reviewer_issue
            reason = (
                "Reviewer selected because no explicit performance "
                "evidence was found in the original review."
            )

        print(f"[RESOLUTION] Selected issue: {selected_issue}")
        print(f"[RESOLUTION] Reason: {reason}")

        return selected_issue, reason

    def run(
        self,
        review_text: str,
        simulate_disagreement: bool = False,
    ) -> dict:
        """Run the complete coordinated multi-agent workflow."""

        if not isinstance(review_text, str) or not review_text.strip():
            raise ValueError("Review text cannot be empty.")

        self.execution_log = []
        self.message_log = []
        self.original_review = review_text
        self.simulate_disagreement = simulate_disagreement

        print("\n========== MULTI-AGENT WORKFLOW ==========")
        print(f"[START] {self.describe()}")

        self.record_event("Coordinator received product review")

        # Step 1: Delegate analysis to Analyst.
        analysis_message = self.delegate(
            self.analyst,
            "analyze_review",
            review_text,
        )

        # Step 2: Handoff the structured analysis to Reviewer.
        review_message = self.handoff(analysis_message)

        # Step 3: Resolve disagreement.
        issue, reason = self.resolve_conflict(
            analysis_message.payload,
            review_message.payload,
            review_text,
        )

        self.record_event("Conflict resolution completed")

        # Step 4: Combine the outputs.
        result = {
            "sentiment": analysis_message.payload["sentiment"],
            "issue": issue,
            "recommendation": (
                "Investigate application performance."
                if issue == "performance"
                else "Continue monitoring customer feedback."
            ),
            "architecture": "multi-agent",
            "analyst_output": analysis_message.payload,
            "reviewer_output": review_message.payload,
            "resolution_reason": reason,
            "execution_log": self.execution_log.copy(),
            "message_count": len(self.message_log),
            "messages": [
                {
                    "sender": message.sender,
                    "receiver": message.receiver,
                    "task": message.task,
                    "payload": message.payload,
                    "status": message.status,
                }
                for message in self.message_log
            ],
        }

        self.record_event("Coordinator combined all outputs")

        # Include the final event in the result.
        result["execution_log"] = self.execution_log.copy()

        print("\n[FINAL RESULT]")
        print(result)

        return result
