
from src.common import Review
from src.single_agent import SingleAgent


sample_review = Review(
    "The product is useful but the app is slow and frustrating."
)

agent = SingleAgent()

result = agent.run(sample_review)

print("\n========== SINGLE-AGENT SUMMARY ==========")
print("Sentiment:", result["sentiment"])
print("Issue:", result["issue"])
print("Recommendation:", result["recommendation"])
print("Execution stages:", len(result["execution_log"]))
