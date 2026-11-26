
from src.multi_agent import Coordinator


sample_review = (
    "The product is useful but the app is slow and frustrating."
)

coordinator = Coordinator()

result = coordinator.run(
    review_text=sample_review,
    simulate_disagreement=True,
)

print("\n========== MULTI-AGENT SUMMARY ==========")
print("Sentiment:", result["sentiment"])
print("Issue:", result["issue"])
print("Recommendation:", result["recommendation"])
print("Architecture:", result["architecture"])
print("Message count:", result["message_count"])
print("Execution events:", len(result["execution_log"]))
print("Resolution reason:", result["resolution_reason"])
