# Voice Interview Agent

An AI-powered phone interview agent built at a hackathon in under 24 hours. The agent calls candidates over the phone and conducts a live voice interview — asking questions, listening to responses, and guiding the conversation — entirely autonomously.

## How It Works

1. A candidate's phone number and target role are submitted
2. Twilio places an outbound call to the candidate
3. The voice AI agent conducts the interview in real time — asking questions, processing spoken responses, and adapting follow-ups
4. The conversation is orchestrated end-to-end using a Langflow pipeline

## Tech Stack

| Layer | Technology |
|---|---|
| Voice & Telephony | Twilio Voice |
| AI Orchestration | Langflow |
| LLM | OpenAI |
| Backend | Python / FastAPI |

## Architecture

```
Candidate Phone
      │
      ▼
  Twilio Voice  ──►  Langflow Pipeline  ──►  OpenAI LLM
      │                    │
      │            (Question generation,
      │             response processing,
      └─────────────follow-up logic)
```

## Running Locally

1. Clone the repo and set up a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your API keys to a `.env` file:
   ```
   TWILIO_ACCOUNT_SID=...
   TWILIO_AUTH_TOKEN=...
   OPENAI_API_KEY=...
   ```
4. Start the Langflow server and import the flow
5. Run the FastAPI backend:
   ```bash
   uvicorn main:app --reload
   ```

## Context

Built as a hackathon submission for a challenge centered on voice AI agents and Langflow. Scope: under 24 hours, solo/small team.
