
import unittest

from src.common import Message, Review, validate_message
from src.single_agent import SingleAgent
from src.multi_agent import Coordinator, Analyst, Reviewer


SAMPLE_REVIEW = (
    "The product is useful but the app is slow and frustrating."
)


class TestSingleAgent(unittest.TestCase):

    def test_single_agent_analysis(self):
        agent = SingleAgent()
        result = agent.run(Review(SAMPLE_REVIEW))

        self.assertEqual(result["sentiment"], "negative")
        self.assertEqual(result["issue"], "performance")
        self.assertEqual(
            result["recommendation"],
            "Investigate application performance.",
        )

    def test_single_agent_execution_log(self):
        agent = SingleAgent()
        result = agent.run(Review(SAMPLE_REVIEW))

        self.assertEqual(len(result["execution_log"]), 5)
        self.assertIn(
            "Execution completed",
            result["execution_log"],
        )

    def test_empty_review_rejected(self):
        agent = SingleAgent()

        with self.assertRaises(ValueError):
            agent.run(Review(""))


class TestMultiAgent(unittest.TestCase):

    def test_analyst_analysis(self):
        analyst = Analyst()
        response = analyst.run(SAMPLE_REVIEW)

        self.assertEqual(response.sender, "Analyst")
        self.assertEqual(response.receiver, "Coordinator")
        self.assertEqual(
            response.payload["sentiment"],
            "negative",
        )
        self.assertEqual(
            response.payload["issue"],
            "performance",
        )

    def test_reviewer_agreement(self):
        analyst = Analyst()
        analysis = analyst.run(SAMPLE_REVIEW)

        reviewer = Reviewer()
        response = reviewer.run(
            SAMPLE_REVIEW,
            analysis.payload,
        )

        self.assertTrue(response.payload["agrees"])
        self.assertEqual(
            response.payload["issue"],
            "performance",
        )

    def test_conflict_resolution(self):
        coordinator = Coordinator()

        issue, reason = coordinator.resolve_conflict(
            {"issue": "performance"},
            {"issue": "general"},
            SAMPLE_REVIEW,
        )

        self.assertEqual(issue, "performance")
        self.assertIn("explicit evidence", reason)

    def test_multi_agent_controlled_disagreement(self):
        coordinator = Coordinator()

        result = coordinator.run(
            SAMPLE_REVIEW,
            simulate_disagreement=True,
        )

        self.assertEqual(result["message_count"], 4)
        self.assertEqual(result["issue"], "performance")
        self.assertFalse(result["reviewer_output"]["agrees"])

    def test_empty_multi_agent_input_rejected(self):
        coordinator = Coordinator()

        with self.assertRaises(ValueError):
            coordinator.run("")

    def test_invalid_message_rejected(self):
        message = Message(
            sender="",
            receiver="Coordinator",
            task="analyze_review",
            payload={"text": SAMPLE_REVIEW},
        )

        with self.assertRaises(ValueError):
            validate_message(message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
