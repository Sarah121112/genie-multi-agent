"""Main entry point for the CaseStudyAgent application."""
import sys
import uuid
from agents.coordinator import build_coordinator


def main():
    """Main interactive agent loop."""
    print("Initializing agent...")
    try:
        agent = build_coordinator()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    
    # Generate a thread ID for checkpointing
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("Agent ready! Ask questions about sales or customers.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            q = input("Question: ").strip()
            if not q:
                continue
            if q.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # Invoke the agent with required config
            result = agent.invoke({"messages": [{"role": "user", "content": q}]}, config=config)
            
            # Extract the last assistant message
            if "messages" in result and result["messages"]:
                # Find the last assistant message with content
                for msg in reversed(result["messages"]):
                    if hasattr(msg, "content") and msg.content:
                        print(f"\n{msg.content}\n")
                        break
                    elif isinstance(msg, dict) and msg.get("role") == "assistant" and msg.get("content"):
                        print(f"\n{msg['content']}\n")
                        break
            else:
                print("\nNo response received\n")
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            # Print full traceback to aid debugging connection errors
            import traceback
            print("\nError encountered (full traceback below):\n")
            traceback.print_exc()


if __name__ == "__main__":
    main()

    main()
