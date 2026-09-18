"""Logic-01: a small rule-based chatbot built with Python's standard library."""

from datetime import datetime


EXIT_COMMANDS = {"bye", "goodbye", "exit", "quit", "see you"}


def get_response(message: str) -> str:
    """Return a deterministic response using a sequence of explicit rules."""
    text = message.strip().lower()

    if not text:
        return "Please type something so I can respond."
    if text in EXIT_COMMANDS:
        return "Goodbye! Thanks for chatting with Logic-01."
    if text.startswith(("hi", "hello", "hey")):
        return "Hello! I’m Logic-01. How can I help you today?"
    if "how are you" in text:
        return "I’m running smoothly and ready to chat. Thanks for asking!"
    if any(word in text for word in ("help", "what can you do", "capabilities")):
        return "I can greet you, explain basic AI concepts, tell a joke, share the time, and end the conversation when you say goodbye."
    if any(word in text for word in ("what is ai", "artificial intelligence", "machine learning")):
        return "Artificial intelligence is the field of building systems that perform tasks that normally require human intelligence. My responses are selected by explicit rules."
    if "joke" in text or "funny" in text:
        return "Why did the programmer bring a ladder? Because the bugs were on the next level."
    if "time" in text or "clock" in text:
        current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
        return f"The current time is {current_time}."
    if "thank" in text:
        return "You’re welcome! Ask me another question whenever you like."

    return "I’m still learning the rules for that one. Try asking about AI, my capabilities, a joke, or the time."


def run_chat() -> None:
    """Keep accepting messages until the user enters an exit command."""
    print("Logic-01: Hello! I’m a rule-based AI chatbot. Type 'help' to see what I can do.")

    while True:
        try:
            message = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nLogic-01: Goodbye! Thanks for chatting.")
            break

        response = get_response(message)
        print(f"Logic-01: {response}")
        if message.strip().lower() in EXIT_COMMANDS:
            break


if __name__ == "__main__":
    run_chat()
