# Logic-01 — Rule-Based AI Chatbot

Logic-01 is my Project 1 submission for the DecodeLabs Artificial Intelligence track. I built it as a small, terminal-based chatbot to practise the foundations that come before machine learning: control flow, clear decision-making, and reliable user interaction.

The chatbot does not use an AI API or a trained model. Instead, it compares each message against a set of intentionally simple rules and selects the first matching response. That makes the behaviour easy to understand, test, and extend.

## What it can do

- Respond to greetings such as `hello`, `hi`, and `hey`
- Explain its capabilities
- Answer a basic question about artificial intelligence
- Tell a short programming joke
- Show the current time
- Handle thanks and unknown inputs gracefully
- Continue accepting messages until the user enters `bye`, `goodbye`, `exit`, or `quit`

## How the logic works

Every message passes through `get_response()` in `chatbot.py`. The function normalizes the input and evaluates explicit conditions in sequence. A matching condition returns a response immediately; if no condition matches, the chatbot uses a friendly fallback response.

The `run_chat()` function provides the continuous loop. It prints each response, checks for an exit command, and then either keeps the conversation going or ends it cleanly.

## Run it locally

You only need Python 3.9 or newer. No third-party packages are required.

```bash
python chatbot.py
```

Example session:

```text
Logic-01: Hello! I’m a rule-based AI chatbot. Type 'help' to see what I can do.
You: hello
Logic-01: Hello! I’m Logic-01. How can I help you today?
You: what is AI?
Logic-01: Artificial intelligence is the field of building systems that perform tasks that normally require human intelligence. My responses are selected by explicit rules.
You: bye
Logic-01: Goodbye! Thanks for chatting with Logic-01.
```

## Run the tests

The project includes a small standard-library test suite covering the main decision branches:

```bash
python -m unittest -v
```

## Project structure

```text
.
├── chatbot.py       # Rule engine and continuous chat loop
├── test_chatbot.py  # Behaviour tests for the core rules
└── README.md        # Project notes and usage guide
```

## What I learned

This project helped me see that a conversational interface starts with disciplined input handling. Before a system can learn from data, it still needs predictable flow, sensible fallbacks, and a clear way to stop. My next improvement would be to move the rules into a data structure so that adding new intents does not require changing the main control flow.

## Project checklist

- [x] Greeting and exit commands
- [x] Explicit if/else decision-making
- [x] Continuous interaction loop
- [x] Friendly fallback response
- [x] Automated tests for core behaviour

Built as part of my DecodeLabs AI internship learning journey.
