# Topic 2: Single-Agent vs Multi-Agent Assessment

## Project Overview
This project compares single-agent and multi-agent architectures using a product-review analysis scenario.

**Sample input:** “The product is useful but the app is slow and frustrating.”

**Expected result**
- Sentiment: `negative`
- Issue: `performance`
- Recommendation: `Investigate application performance.`

The implementation uses deterministic Python keyword rules and the standard library. It does not require an external LLM, API key, or third-party package.

## Objectives
1. Implement a single agent that performs the complete review-analysis workflow.
2. Implement a multi-agent workflow with a Coordinator, Analyst, and Reviewer.
3. Define and validate structured agent messages.
4. Demonstrate delegation, handoffs, and message passing.
5. Detect and resolve a disagreement.
6. Compare the outputs and workflow traces.

## Project Structure
```text
Single_vs_Multi_Agent_Assessment/
├── src/
│   ├── __init__.py
│   ├── common.py
│   ├── single_agent.py
│   ├── multi_agent.py
│   └── main.py
├── outputs/
│   └── comparison_evidence.json
├── test_single_agent.py
├── test_multi_agent.py
├── test_topic2.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Architecture

### Single-Agent
`SingleAgent` receives the review, analyzes sentiment, detects the main issue, generates a recommendation, and returns the result with an execution log. The sample execution records five stages.

### Multi-Agent
- **Coordinator:** orchestrates the workflow, delegates tasks, receives responses, resolves conflicts, and combines the result.
- **Analyst:** analyzes sentiment and identifies the issue with supporting evidence.
- **Reviewer:** independently reviews the Analyst's issue classification.

Messages use the fields `sender`, `receiver`, `task`, and `payload`, with a completion status. The demonstrated workflow contains four inter-agent messages.

### Conflict Resolution
The assessment deliberately configures the Reviewer to propose `general` while the Analyst identifies `performance`. The Coordinator checks the original review for explicit evidence. Because it contains `slow`, the Coordinator selects `performance` and records its reason.

**Important:** This disagreement is deliberately simulated to test conflict resolution. It is not a naturally occurring agent disagreement.

## Setup
Only the Python standard library is used. No third-party package installation is required.

If you need to create a virtual environment:
```cmd
python -m venv .venv
.venv\Scripts\activate
```

## Run the Project
From the project root:
```cmd
python -m src.main
```
The program prints both architecture results and a comparison summary. It saves persistent evidence to:
```text
outputs/comparison_evidence.json
```
To inspect the evidence in Windows CMD:
```cmd
type outputs\comparison_evidence.json
```

## Run Tests
```cmd
python -m unittest test_topic2 -v
```
Verified result: **9 tests passed**.

## Observed Results

| Comparison item | Single-Agent | Multi-Agent |
|---|---|---|
| Final sentiment | negative | negative |
| Final issue | performance | performance |
| Recommendation | Investigate application performance. | Investigate application performance. |
| Recorded workflow stages/events | 5 stages | 5 events |
| Specialist agents | 1 | 2 |
| Agent messages | No inter-agent handoffs | 4 messages |

Both architectures produced the same final classification and recommendation for the sample review. The multi-agent workflow additionally demonstrates delegation, structured messages, independent review, and conflict resolution.

The counts describe this program's logs and message records. They are not latency, cost, throughput, or accuracy benchmarks.

## Limitations
- The analysis uses simple keyword-based deterministic rules.
- The disagreement is a controlled test configuration.
- Only a small sample scenario is used; broader datasets would be needed to evaluate generalization.
- No live LLM, external tool, or production multi-agent runtime is involved.

## Conclusion
This assessment demonstrates the structural difference between a single-agent workflow and a coordinated multi-agent workflow. A single agent is straightforward for a compact task. A multi-agent design makes responsibilities, communication, review, and conflict handling explicit, while introducing additional coordination complexity.

## Reflection
Completing this assessment helped me understand the practical architectural difference between a single agent and a multi-agent system. In the single-agent implementation, one component performs the entire review-analysis process, keeping the workflow simple and easy to follow. In the multi-agent implementation, responsibilities are divided between a Coordinator, an Analyst, and a Reviewer. This made delegation, message passing, and orchestration clearer.

The message contract was an important part of the exercise. Instead of passing unstructured information between components, each message carries a sender, receiver, task, and payload. This makes the communication flow easier to inspect and validate. The Coordinator demonstrates why an orchestrator is useful: it assigns work, receives specialist responses, handles disagreements, and combines the final result.

The controlled disagreement test was particularly useful because it exercised a conflict-resolution path consistently. The Analyst identifies the performance issue, while the Reviewer is deliberately configured to return a general issue. The Coordinator then uses explicit evidence from the original review—the word “slow”—to select the performance issue. This is a deterministic demonstration, not evidence that independent agents will always disagree in this way.

The assessment reinforced the importance of testing. The nine passing unit tests verify the main analysis behavior, message validation, reviewer agreement, controlled disagreement, and conflict resolution. Saving the comparison as JSON provides a persistent evidence artifact that can be inspected later.

Overall, I learned that multi-agent architecture is not automatically better than a single-agent design. It is useful when specialization, review, and coordination justify the added complexity. For a small task, a single agent may be sufficient; for workflows with distinct responsibilities, a multi-agent structure can make the system easier to organize and extend.
