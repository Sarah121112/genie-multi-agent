"""Test script to verify SQLite memory is working with the coordinator."""
import uuid
from agents.coordinator import build_coordinator


def test_conversation_memory():
    """Test if the agent remembers context across multiple invocations."""
    
    print("=" * 70)
    print("TESTING SQLITE MEMORY WITH COORDINATOR")
    print("=" * 70)
    
    # Build coordinator (will create/use checkpoints.sqlite)
    agent = build_coordinator()
    
    # Use a fixed thread_id so we can test memory across calls
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"\nUsing thread_id: {thread_id}\n")
    
    # Test questions that build on each other
    test_questions = [
        "What is the total revenue by region?",
        "Which region has the highest churn risk?",
        "Based on the revenue and churn data, what region needs the most attention?",
        "What are the top products in the high-revenue region?",
        "Compare customer lifetime value between the high-revenue and low-revenue regions.",
    ]
    
    print("This test will ask multiple questions and check if the agent remembers context.\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"QUESTION {i}: {question}")
        print('='*70)
        
        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": question}]},
                config=config
            )
            
            # Extract and print the last assistant message
            if "messages" in result and result["messages"]:
                for msg in reversed(result["messages"]):
                    if hasattr(msg, "content") and msg.content and hasattr(msg, "role") and msg.role == "assistant":
                        print(f"\nRESPONSE:\n{msg.content}\n")
                        break
            
            print("✓ Question processed successfully")
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n{'='*70}")
    print("TEST COMPLETE")
    print(f"{'='*70}")
    print(f"\nTo verify memory persistence:")
    print(f"1. Check 'checkpoints.sqlite' file exists in the project root")
    print(f"2. Run this test again with the SAME thread_id to see if context is retained")
    print(f"3. Questions that reference previous answers should show understanding of prior context")
    print(f"\nThread ID for this session: {thread_id}")
    print("Copy this ID to test memory persistence in future runs.\n")


if __name__ == "__main__":
    test_conversation_memory()
