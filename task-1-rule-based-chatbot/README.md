# Task 1 — Rule-Based AI Chatbot

This is my first DecodeLabs AI internship task. I built a small terminal chatbot to practise the basics of conversational logic before moving into machine learning: input handling, control flow, explicit decision-making, and a reliable interaction loop.

## What it does

- Responds to greetings such as `hello`, `hi`, and `hey`
- Explains its capabilities
- Answers a basic artificial intelligence question
- Tells a short programming joke
- Shows the current time
- Handles thanks and unknown messages politely
- Keeps chatting until the user enters `bye`, `goodbye`, `exit`, or `quit`

## Run the chatbot

Python 3.9 or newer is enough, and there are no third-party dependencies.

```bash
python chatbot.py
```

## Run the tests

```bash
python -m unittest -v
```

The tests cover the greeting, exit, AI explanation, and fallback rules.

## Implementation notes

The `get_response()` function normalizes each message and checks explicit rules in sequence. The first matching condition returns a deterministic response. If nothing matches, the chatbot uses a fallback message instead of failing silently.

The `run_chat()` function wraps the rule engine in a continuous loop. It prints each response and ends cleanly when the user enters an exit command or closes the terminal.

## Files

- `chatbot.py` — rule engine and continuous chat loop
- `test_chatbot.py` — standard-library tests for the core responses
