# Technology Decisions

**Project:** Enterprise Knowledge Copilot  
**Document Type:** Technology Decision Record  
**Status:** Approved Target Direction  
**Implementation Status:** 🚧 Active Development  
**Engineering Principle:** Use technology to solve requirements, not to collect buzzwords.

---

# 1. Purpose

This document records the major technology decisions for Enterprise Knowledge Copilot.

The project intentionally avoids selecting technologies simply because they appear frequently in Generative AI job descriptions.

Every technology should answer:

> **What engineering or business requirement does this solve?**

Technology choices should be evaluated according to:

- project requirements;
- maintainability;
- security;
- developer understanding;
- operational complexity;
- portability;
- cost;
- testability;
- scalability;
- portfolio learning value.

---

# 2. Decision Philosophy

The project follows:

```text
Requirement
    ↓
Engineering Problem
    ↓
Possible Solutions
    ↓
Trade-Off Analysis
    ↓
Technology Decision
    ↓
Implementation
    ↓
Measurement
```

Not:

```text
Interesting Technology
       ↓
Add to Architecture
       ↓
Find a reason later
```

---

# 3. Current Technology Direction

| Area | Technology | Status |
|---|---|---|
| Language | Python | Implemented |
| Backend | FastAPI | Implemented |
| Validation | Pydantic | Implemented |
| Dependency Management | uv | Implemented |
| Development LLM | Gemini | Implemented |
| Embeddings | Gemini Embedding API | Prototype |
| Database | PostgreSQL | Planned |
| Vector Search | PGVector | Planned |
| Frontend | Next.js + React + TypeScript | Planned |
| Containers | Docker | Planned |
| Local Orchestration | Docker Compose | Planned |
| CI/CD | GitHub Actions | Planned |
| Observability | Structured logging + selected tooling | Planned |
| Cloud Deployment | Free-first deployment | Planned |
| Infrastructure as Code | Terraform if justified | Later |
| Kubernetes | Learning / future scaling consideration | Not required initially |

---

# 4. Python

## Decision

Use:

```text
Python
```

for the backend and AI application layer.

## Why?

Python has strong support for:

- AI/ML libraries;
- LLM SDKs;
- embedding APIs;
- data processing;
- evaluation tooling;
- FastAPI;
- PostgreSQL clients;
- testing.

It also aligns with the project's existing AI engineering work.

## Trade-Off

Other languages could provide strong backend systems.

However, introducing another backend language would add complexity without currently solving a project requirement.

---

# 5. FastAPI

## Decision

Use:

```text
FastAPI
```

for the backend HTTP API.

## Requirement

The application requires an API connecting:

```text
Frontend
    ↓
Application Services
    ↓
RAG
    ↓
Data / AI Providers
```

## Why FastAPI?

Relevant capabilities include:

- Python integration;
- request/response validation;
- Pydantic;
- type hints;
- OpenAPI generation;
- asynchronous capabilities where useful;
- straightforward service integration.

---

# 6. Why Not Flask?

Flask could successfully implement the backend.

FastAPI was selected because its typed request/response models and automatic OpenAPI integration align well with the project's API-contract requirements.

This does not mean Flask is incapable of building the system.

It is a project trade-off.

---

# 7. Why Not Django?

Django provides a larger application framework including:

- ORM;
- authentication;
- administration;
- templating.

Those capabilities can be valuable.

However, the project currently benefits from a smaller API-focused backend where the AI and retrieval architecture can remain explicit.

If requirements changed significantly, the decision could be revisited.

---

# 8. Pydantic

## Decision

Use Pydantic models for FastAPI request and response validation.

## Requirement

External input must not flow directly into application services without validation.

Conceptually:

```text
External JSON
     ↓
Pydantic Schema
     ↓
Validated Application Input
```

Pydantic does not replace security controls, but it provides an important application boundary.

---

# 9. uv

## Decision

Use:

```text
uv
```

for Python project and dependency management.

## Why?

The project requires:

- reproducible environments;
- dependency installation;
- dependency declaration;
- lockfile support;
- straightforward developer workflow.

Relevant files include:

```text
pyproject.toml
uv.lock
```

---

# 10. `pyproject.toml` vs `uv.lock`

These files solve different problems.

```text
pyproject.toml
```

describes project configuration and declared dependencies.

```text
uv.lock
```

records resolved dependency versions for reproducible environments.

Both belong in source control.

---

# 11. Large Language Model Strategy

## Decision

Use a provider-isolated LLM service.

Architecture:

```text
RAG Service
    ↓
LLM Service
    ↓
Provider SDK
    ↓
Model Provider
```

Application endpoints should not directly contain provider-specific model calls.

---

# 12. Development LLM

## Current Decision

Use Gemini during the current free-first development phase.

The current integration has already demonstrated connectivity through the provider SDK.

## Why?

The project currently has a strict cost constraint.

A development provider should therefore allow the RAG architecture to be built and understood without making paid API usage a prerequisite.

---

# 13. Gemini Is Not the Architecture

The architecture should not become:

```text
Enterprise Knowledge Copilot
=
Gemini Application
```

Instead:

```text
Enterprise Knowledge Copilot
      ↓
LLM Service
      ↓
Configured Provider
```

This separation allows provider decisions to evolve.

---

# 14. Provider Isolation

Provider-specific logic should remain inside a dedicated boundary.

For example:

```text
LLMService
│
└── Gemini implementation
```

A future architecture could support:

```text
LLMService
│
├── Gemini
├── OpenAI
├── Azure OpenAI
└── Local Model
```

only if requirements justify those providers.

The project does not need multiple providers simply to demonstrate abstraction.

---

# 15. Why Not Depend on OpenAI Immediately?

A paid external API is not necessary to prove:

- RAG architecture;
- retrieval;
- grounding;
- evaluation;
- API design;
- frontend integration;
- security concepts.

The project can preserve provider independence while using a free-first development option.

If another provider becomes appropriate later, it can be evaluated separately.

---

# 16. Local Models / Ollama

Local model execution remains an optional development capability.

Potential benefit:

```text
Application
   ↓
Local Model
```

reduces reliance on an external generation API.

However, local models require adequate hardware.

The project should not force large local models onto hardware that cannot run them effectively.

Local execution is therefore optional rather than a core architecture requirement.

---

# 17. Embedding Strategy

The project currently uses a hosted embedding model during learning/prototyping.

Conceptually:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

The embedding provider should eventually be isolated similarly to the LLM provider where that abstraction provides practical value.

---

# 18. Embedding Model vs LLM

These solve different problems.

```text
Embedding Model
=
FIND
```

It creates semantic representations used for retrieval.

```text
LLM
=
ANSWER
```

It generates natural-language responses from evidence.

Understanding this separation is more important than selecting a large number of AI frameworks.

---

# 19. PostgreSQL

## Decision

Use:

```text
PostgreSQL
```

as the primary persistent database.

## Requirement

The application needs structured storage for:

- users;
- roles;
- permissions;
- documents;
- versions;
- metadata;
- conversations;
- feedback;
- audit information.

PostgreSQL provides a mature relational model for these requirements.

---

# 20. PGVector

## Decision

Use:

```text
PGVector
```

for initial persistent vector retrieval.

## Requirement

The application needs semantic search over document chunks.

PGVector allows vectors to exist alongside relational metadata inside PostgreSQL.

Conceptually:

```text
PostgreSQL
│
├── Users
├── Roles
├── Permissions
├── Documents
├── Metadata
└── Chunk Embeddings
```

---

# 21. Why PostgreSQL + PGVector?

Permission-aware RAG requires vector retrieval to interact closely with relational information.

For example:

```text
Semantic Similarity
       +
User Permissions
       +
Document Status
       +
Department Metadata
```

Using PostgreSQL + PGVector allows these concerns to remain closely connected.

---

# 22. Why Not Multiple Vector Databases?

The project does not initially require:

```text
PGVector
+
Pinecone
+
Qdrant
+
Chroma
```

simultaneously.

Operating multiple vector systems would increase:

- complexity;
- configuration;
- testing;
- operational burden.

without currently solving a demonstrated requirement.

---

# 23. Qdrant

Qdrant may be studied or evaluated later if requirements justify a dedicated vector database.

Possible reasons could include:

- scaling requirements;
- retrieval capabilities;
- operational separation;
- measured performance needs.

It should not be introduced merely to add another technology to the CV.

---

# 24. Pinecone

The same principle applies to managed vector services such as Pinecone.

A managed vector database may reduce infrastructure management in some production environments.

However, the initial project already requires relational data and has a zero-cost development constraint.

PGVector is therefore the initial target.

---

# 25. MongoDB

MongoDB is not currently required.

The project already has strongly relational concepts:

```text
Users
Roles
Permissions
Documents
Versions
Chunks
Citations
```

PostgreSQL provides a natural fit.

MongoDB should only be introduced if a future requirement benefits materially from its document-oriented model.

---

# 26. Frontend Language

## Decision

Use:

```text
TypeScript
```

for the frontend.

## Why?

The frontend communicates with structured backend contracts.

TypeScript can help detect incorrect assumptions about:

- API responses;
- component properties;
- source objects;
- application states.

---

# 27. React

## Decision

Use React as the component model for the frontend.

The application naturally decomposes into reusable UI components such as:

```text
SourcesPanel
QuestionInput
AssistantAnswer
CitationCard
SourceViewer
```

---

# 28. Next.js

## Decision

Use:

```text
Next.js
```

as the frontend framework.

## Requirement

The project requires a production-oriented React application with:

- routing;
- application structure;
- deployment options;
- TypeScript support;
- reusable components.

Next.js provides these capabilities without requiring the project to assemble the entire frontend toolchain manually.

---

# 29. Why Not Streamlit?

Streamlit is useful for:

- prototypes;
- data applications;
- internal demonstrations.

However, the target role requires full-stack engineering capability.

A Next.js frontend better demonstrates:

```text
Frontend Architecture
API Integration
Application State
TypeScript
Component Design
Authentication Integration
Production Web Development
```

Therefore Streamlit is not the target UI framework.

---

# 30. RAG Framework Decision

The initial RAG implementation should remain explicit.

Conceptually:

```text
Question
 ↓
Embedding
 ↓
Retrieval
 ↓
Evidence
 ↓
Prompt
 ↓
LLM
 ↓
Answer
```

The user should understand every stage before introducing a framework that abstracts those stages.

---

# 31. LangChain

## Decision

Do not make LangChain a core dependency until it solves a demonstrated requirement.

Potential future value may include:

- integrations;
- reusable RAG components;
- provider abstraction;
- structured workflows.

But adding LangChain solely because the target job mentions it would weaken rather than strengthen the engineering rationale.

---

# 32. LangGraph

LangGraph is useful for stateful graph-based AI workflows.

Example:

```text
Classify Request
      ↓
Retrieve
      ↓
Check Evidence
      ↓
Tool Action
      ↓
Review State
```

The current core RAG flow does not require this complexity.

LangGraph may be introduced later if a real agent/workflow requirement emerges.

---

# 33. CrewAI

Multi-agent orchestration is not required for the current business problem.

The project should not create:

```text
Research Agent
Policy Agent
Security Agent
Answer Agent
Manager Agent
```

merely to demonstrate multi-agent terminology.

The current problem can be solved more predictably with explicit application services.

---

# 34. Agents

Agentic behaviour may be explored later.

A real requirement might involve:

```text
Retrieve Policy
      ↓
Determine Approved Action
      ↓
Call Authorised Business Tool
      ↓
Confirm Result
```

Tool-using agents introduce additional security and reliability concerns.

They should therefore follow, not precede, a trustworthy RAG foundation.

---

# 35. Docker

## Decision

Use:

```text
Docker
```

for containerisation.

## Requirement

The application should run consistently across:

```text
Developer Machine
CI Environment
Deployment Environment
```

Docker packages application runtime requirements into reproducible container images.

---

# 36. Docker Compose

## Decision

Use Docker Compose for local multi-container orchestration.

Example:

```text
Docker Compose
│
├── Frontend
├── Backend
└── PostgreSQL + PGVector
```

This is appropriate for local development and demonstration.

---

# 37. Kubernetes

## Initial Decision

Do not deploy Kubernetes merely to make the project appear enterprise-grade.

Kubernetes solves problems involving areas such as:

- container orchestration;
- scheduling;
- service discovery;
- scaling;
- self-healing;
- deployment management.

The initial portfolio application does not yet demonstrate a scale requiring Kubernetes.

---

# 38. Kubernetes Learning Value

Kubernetes remains relevant to the target role.

Therefore the project may later document or demonstrate Kubernetes fundamentals separately after Docker and deployment concepts are understood.

The important interview answer is not:

```text
"I used Kubernetes because enterprise applications use Kubernetes."
```

It is:

```text
"I understand the operational problems Kubernetes solves,
and I would introduce it when deployment scale and availability
requirements justify the additional complexity."
```

---

# 39. Modular Monolith

## Decision

Start with a:

```text
Modular Monolith
```

rather than microservices.

Conceptually:

```text
FastAPI Application
│
├── Authentication
├── Retrieval
├── RAG
├── LLM
├── Ingestion
└── Data Access
```

The modules have clear responsibilities while remaining deployable as one backend application.

---

# 40. Why Not Microservices?

Microservices introduce:

- network communication;
- service discovery;
- distributed tracing;
- deployment coordination;
- distributed failure modes;
- additional infrastructure.

The current project does not require these costs.

If future scaling or team-boundary requirements justify service extraction, the modular architecture provides a clearer path.

---

# 41. Git

## Decision

Use Git for version control.

Git provides:

```text
Change History
Branches
Commits
Reviewable Changes
Rollback Capability
```

Commits should represent meaningful project changes.

---

# 42. GitHub

## Decision

Use GitHub as the portfolio repository and collaboration platform.

The repository provides evidence of:

- architecture;
- implementation;
- documentation;
- tests;
- CI/CD;
- engineering progression.

The repository itself is part of the portfolio deliverable.

---

# 43. GitHub Actions

## Decision

Use:

```text
GitHub Actions
```

for initial CI/CD automation.

Potential pipeline:

```text
Push / Pull Request
        ↓
Install Dependencies
        ↓
Lint / Static Checks
        ↓
Tests
        ↓
Build
        ↓
Deployment where configured
```

The exact workflow will be introduced after tests and containers exist.

---

# 44. Why Not GitLab CI or Jenkins?

GitLab CI and Jenkins are valid CI/CD technologies.

However, the source repository is already hosted on GitHub.

GitHub Actions provides the simplest initial integration.

The underlying CI/CD concepts remain transferable.

---

# 45. Observability Technology

Observability technology will be selected incrementally.

Initial requirement:

```text
Structured Logging
Request IDs
Latency
Errors
Retrieval Events
LLM Events
```

Possible later tools include:

```text
OpenTelemetry
Langfuse
LangSmith
Cloud Monitoring
```

A tool should not be introduced until the application produces useful telemetry.

---

# 46. Langfuse vs LangSmith

Both may provide useful GenAI observability capabilities.

The project does not need both.

Selection should consider:

- required traces;
- evaluation integration;
- provider/framework compatibility;
- hosting;
- free-tier constraints;
- operational complexity.

The project will choose based on requirements at implementation time.

---

# 47. Cloud Strategy

The deployment strategy is:

> **Free-first, portable architecture.**

The application should avoid unnecessary coupling to a cloud provider during early development.

Target conceptual deployment:

```text
Internet
   ↓
Frontend
   ↓
Backend
   ↓
PostgreSQL + PGVector
   ↓
External AI Provider
```

---

# 48. Cloud Learning

The target role references AWS and Azure.

The portfolio should eventually demonstrate understanding of cloud concepts such as:

```text
Compute
Networking
Secrets
Databases
Logging
Identity
Deployment
```

It is better to understand one deployment architecture deeply than create superficial deployments across several clouds.

---

# 49. Infrastructure as Code

Terraform is relevant to reproducible infrastructure.

Potential flow:

```text
Terraform
    ↓
Cloud Resources
    ↓
Repeatable Infrastructure
```

However, Terraform should only be introduced once the project has infrastructure worth provisioning.

Writing Terraform for nonexistent architecture would add documentation without engineering value.

---

# 50. Security Technology

The project does not treat a single security product as the security solution.

Security emerges from:

```text
Authentication
Authorisation
Validation
Permission-Aware Retrieval
Secret Management
Database Controls
Transport Security
Testing
Monitoring
```

Technology supports these controls but does not replace secure architecture.

---

# 51. Testing Technology

The backend will use appropriate Python testing tools, likely centred around:

```text
pytest
```

FastAPI's testing ecosystem can support API-level testing.

Frontend tests will be selected based on implemented component and integration requirements.

The project should avoid adding several testing frameworks without a testing need.

---

# 52. Development Environment

Target development workflow:

```text
Git
+
GitHub
+
Python
+
uv
+
FastAPI
+
TypeScript / Next.js
+
Docker
```

During the current documentation phase, project documentation may be created directly through the GitHub web interface.

---

# 53. Cost Constraint

The portfolio currently operates under a strict:

```text
£0 development budget
```

Therefore technology selection must consider free development options.

This influences:

- model provider;
- database hosting;
- deployment platform;
- observability platform;
- CI/CD.

A free-first strategy should not compromise architectural understanding.

---

# 54. Technology Decision Matrix

| Technology | Decision | Reason |
|---|---|---|
| Python | Use | AI/backend ecosystem |
| FastAPI | Use | Typed Python API |
| Pydantic | Use | API validation |
| uv | Use | Dependency/environment management |
| Gemini | Development provider | Free-first model access |
| PostgreSQL | Use | Relational application data |
| PGVector | Use | Vector search alongside relational metadata |
| Next.js | Use | Production-oriented React frontend |
| TypeScript | Use | Typed frontend development |
| Docker | Use | Reproducible runtime |
| Docker Compose | Use | Local service orchestration |
| GitHub Actions | Use | Repository-integrated CI/CD |
| LangChain | Conditional | Add when abstraction provides value |
| LangGraph | Conditional | Add for justified stateful AI workflows |
| Qdrant | Conditional | Evaluate if dedicated vector DB needed |
| MongoDB | Not currently needed | PostgreSQL fits current data model |
| Kubernetes | Not initially required | Operational complexity not yet justified |
| Terraform | Later/conditional | Add when infrastructure exists |
| Microservices | Not initially required | Modular monolith is sufficient |
| Multi-Agent Architecture | Not currently required | No demonstrated business need |

---

# 55. Avoiding Resume-Driven Development

A dangerous portfolio strategy is:

```text
Job Description Mentions:
Kubernetes
LangChain
MongoDB
Qdrant
Terraform
Agents

Therefore:
Add all of them.
```

This creates an architecture that may be difficult to explain or defend.

The project instead follows:

```text
Understand Technology
        ↓
Understand Requirement
        ↓
Determine Fit
        ↓
Implement if Justified
        ↓
Measure Result
        ↓
Explain Trade-Off
```

---

# 56. Technology Introduction Test

Before adding a new technology, answer:

### 1. What problem exists?

If there is no identifiable problem, stop.

### 2. Why does the current architecture not solve it adequately?

If it already does, stop.

### 3. How does the proposed technology solve the problem?

Explain technically.

### 4. What complexity does it introduce?

Consider:

```text
Development
Testing
Security
Deployment
Operations
Cost
```

### 5. How will success be measured?

There should be evidence that the change helped.

---

# 57. Example: Reranker Decision

Bad reason:

```text
Reranking is advanced RAG.
```

Better process:

```text
Evaluation shows relevant evidence
is frequently ranked too low.
        ↓
Introduce reranker.
        ↓
Run same benchmark.
        ↓
Compare Recall / Ranking / Latency.
```

The technology earns its place through evidence.

---

# 58. Example: Kubernetes Decision

Bad reason:

```text
Senior engineers use Kubernetes.
```

Better reasoning:

```text
Multiple containerised services
        +
Scaling requirements
        +
Availability requirements
        +
Deployment complexity
        ↓
Evaluate orchestration platform
        ↓
Kubernetes may become appropriate
```

---

# 59. Example: LangGraph Decision

Bad reason:

```text
Agents are popular.
```

Better reasoning:

```text
Business workflow requires
multiple stateful steps
        +
branching
        +
tool execution
        +
recoverable state
        ↓
Evaluate LangGraph
```

---

# 60. Technology Decisions Are Revisable

Architecture decisions are not permanent simply because they are documented.

The project may later discover that:

```text
PGVector performance is insufficient

A different deployment platform is required

Another model performs better

A workflow requires orchestration
```

When evidence changes, the decision can change.

The important requirement is that the reason is documented.

---

# 61. Current vs Target Technology

## Currently Implemented / Prototyped

```text
Python
uv
FastAPI
Pydantic
Gemini LLM integration
Gemini embedding experiments
Manual cosine similarity
Top-K retrieval experiment
Initial retrieval service
```

---

## Planned Core Technologies

```text
PostgreSQL
PGVector
Next.js
React
TypeScript
Docker
Docker Compose
GitHub Actions
Structured Observability
Authentication
```

---

## Conditional / Later Technologies

```text
LangChain
LangGraph
Qdrant
Terraform
Kubernetes
Specialised LLM Observability Platform
Additional Model Providers
```

These should not be represented as implemented.

---

# 62. Senior Engineering Principle

A senior engineering decision is not:

> "Which technology is more impressive?"

It is:

> "Which solution satisfies the requirement with an acceptable balance of capability, complexity, risk, cost and maintainability?"

This project should provide evidence of that reasoning.

---

# 63. Technology North Star

The target architecture is intentionally understandable:

```text
Next.js / TypeScript
        ↓
FastAPI / Python
        ↓
Application Services
        ↓
Permission-Aware RAG
        ↓
PostgreSQL + PGVector
        ↓
Provider-Isolated AI
```

Operationally:

```text
GitHub
   ↓
CI/CD
   ↓
Docker
   ↓
Deployment
   ↓
Observability
```

Additional technologies should only enter this architecture when they solve a demonstrated problem.

The project's core technology principle is:

> **Use the simplest architecture that satisfies the requirements, measure where it fails, and add complexity only when evidence justifies it.**
