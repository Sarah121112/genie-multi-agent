import uuid
from agents.coordinator import build_coordinator
from utils.retry import retry_call


def main():
    print("Starting coordinator agent...")

    agent = build_coordinator()

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("Agent ready!")
    print("Ask questions about sales, customers, or inventory.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Questions: ").strip()

        if not question:
            continue

        if question.lower() in ("exit", "quit"):
            print("Bye 👋")
            break

        ok, result, err, attempts = retry_call(
            lambda: agent.invoke({"messages": [("user", question)]}, config=config),
            retries=2,
            base_delay=1.0,
            max_delay=6.0,
        )

        if not ok:
            print("\nAgent: Sorry — I couldn’t complete that request.\n")
            print(f"Agent: Attempts: {attempts}")
            print(f"Agent: Error: {err}\n")
            continue

        messages = result.get("messages", [])
        if messages:
            print(f"\nAgent: {messages[-1].content}\n")
        else:
            print("\nAgent: (no response)\n")


if __name__ == "__main__":
    main()
