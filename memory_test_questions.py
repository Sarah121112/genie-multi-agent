"""
Generate test questions to verify SQLite memory is working.
Run this first to see what questions to ask the agent.
"""
import uuid


def print_test_questions():
    """Print a list of memory test questions to ask the agent."""
    
    thread_id = str(uuid.uuid4())
    
    print("\n" + "="*70)
    print("MEMORY TEST - QUESTIONS TO ASK THE AGENT")
    print("="*70)
    
    print(f"\nThread ID: {thread_id}")
    print("\nTo test if memory is working:")
    print("1. Run: python main.py")
    print("2. Ask these questions in order (the agent should remember earlier answers)")
    print("3. Later questions reference earlier answers - watch if the agent understands context\n")
    
    questions = [
        {
            "num": 1,
            "question": "What is the total revenue by region?",
            "expects": "Agent should give revenue breakdown by region (North vs South)"
        },
        {
            "num": 2,
            "question": "Which region has the highest churn risk?",
            "expects": "Agent should identify the region with highest churn (South)"
        },
        {
            "num": 3,
            "question": "Based on the revenue and churn data you just shared, which region needs the most attention?",
            "expects": "Agent should remember: North has high revenue but South has 100% churn risk"
        },
        {
            "num": 4,
            "question": "What are the top 3 products in the high-revenue region?",
            "expects": "Agent should know 'high-revenue region' = North from earlier answer"
        },
        {
            "num": 5,
            "question": "Compare the customer lifetime value between the regions we discussed.",
            "expects": "Agent should remember both regions (North and South) from context"
        },
        {
            "num": 6,
            "question": "If we focus on reducing churn in the region with high risk, what products should we promote?",
            "expects": "Agent should know that's South, and suggest products sold there (Furniture/Chair)"
        }
    ]
    
    print("QUESTIONS (ask in order):\n")
    for q in questions:
        print(f"Q{q['num']}: {q['question']}")
        print(f"   → Expects agent to show memory of: {q['expects']}\n")
    
    print("="*70)
    print("\nTO TEST PERSISTENCE:")
    print(f"Save this thread_id: {thread_id}")
    print("Exit and re-run main.py later with same thread_id to verify it remembers everything!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_test_questions()
