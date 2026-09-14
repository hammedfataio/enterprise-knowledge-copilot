# Enterprise Knowledge Copilot

An enterprise-oriented Generative AI engineering project for retrieving
reliable, source-grounded answers from organisational knowledge.

## Current Development Stage

### Milestone 1 — API Foundation

Implemented:

- FastAPI backend
- Root API endpoint
- Health-check endpoint
- POST question endpoint
- Pydantic request validation
- Interactive API documentation

Current endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API root |
| GET | `/health` | Basic service health check |
| POST | `/questions` | Accept and validate user questions |

> The `/questions` endpoint does not yet call an LLM. The current milestone
> focuses on API design, HTTP communication, and request validation.