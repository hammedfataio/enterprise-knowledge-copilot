# Product Requirements Specification

**Project:** Enterprise Knowledge Copilot  
**Document Type:** Product Requirements Document (PRD)  
**Status:** Approved Build Specification  
**Implementation Status:** 🚧 Active Development  
**Primary Principle:** Find → Ask → Verify

---

## 1. Purpose

This document defines the functional, non-functional, security, retrieval, user-experience, and operational requirements for Enterprise Knowledge Copilot.

It serves as the implementation contract for the project.

A capability described as a requirement in this document must not be represented as implemented until corresponding code and appropriate verification exist.

The project is designed to demonstrate production-minded Generative AI engineering rather than a simple chatbot or "chat with PDF" prototype.

---

# 2. Product Definition

Enterprise Knowledge Copilot is a source-grounded Generative AI platform that allows authorised employees to retrieve reliable information from approved organisational knowledge.

The system combines:

- organisational documents;
- document ingestion;
- chunking;
- metadata;
- embeddings;
- semantic retrieval;
- vector search;
- permission-aware filtering;
- Large Language Model generation;
- source citations;
- evaluation;
- auditability;
- observability.

The primary user experience should remain simple:

```text
Find
 ↓
Ask
 ↓
Verify
```

---

# 3. Product Goals

The system should enable employees to:

1. access organisational knowledge through natural-language questions;
2. receive answers grounded in approved organisational documents;
3. verify important answers against supporting sources;
4. avoid relying on unsupported AI-generated organisational information;
5. access only information they are authorised to retrieve.

The engineering platform should additionally demonstrate:

- maintainable application architecture;
- measurable retrieval quality;
- secure information boundaries;
- automated testing;
- operational visibility;
- reproducible deployment.

---

# 4. Non-Goals

The initial product is not intended to become:

- a general-purpose ChatGPT replacement;
- an unrestricted internet search engine;
- a document-management system replacement;
- an autonomous multi-agent organisation;
- a custom foundation model;
- a system containing multiple databases that perform the same role;
- a microservice architecture without a demonstrated scaling requirement.

Technologies must solve requirements rather than exist solely for portfolio visibility.

---

# 5. Target Users

## 5.1 Employee

An employee needs to retrieve organisational information.

Example questions:

```text
Can I work from home?
```

```text
How many days of annual leave do employees receive?
```

```text
How often should I change my company password?
```

Employees should not need to understand how RAG, embeddings, vector search, or LLMs work.

---

## 5.2 Knowledge Owner

Knowledge owners maintain organisational information.

Examples include:

- Human Resources;
- IT;
- Information Security;
- Compliance;
- Operations.

Knowledge owners may eventually manage approved documents within their authorised domain.

---

## 5.3 Administrator

Administrators manage system-level capabilities such as:

- users;
- roles;
- permissions;
- document access;
- system configuration;
- audit information.

Administrative capabilities should not clutter the normal employee experience.

---

# 6. Core User Journey

The primary user journey is:

```text
Employee
   ↓
Authenticate
   ↓
Open Knowledge Workspace
   ↓
Select / Search Sources
   ↓
Ask Question
   ↓
System Identifies Authorised Knowledge
   ↓
Retrieve Relevant Evidence
   ↓
Generate Grounded Answer
   ↓
Display Answer + Citations
   ↓
Employee Verifies Source
```

The product must prioritise this journey over unnecessary dashboard complexity.

---

# 7. Functional Requirements

## FR-001 — User Authentication

**Priority:** Must Have  
**Initial Status:** Planned

The system shall identify users before protected organisational knowledge is accessed.

### Acceptance Criteria

- protected application areas require authentication;
- authenticated requests contain user identity;
- unauthenticated access to protected resources is rejected;
- authentication secrets are not stored directly in application source code.

---

## FR-002 — Role-Based Authorisation

**Priority:** Must Have  
**Initial Status:** Planned

The system shall associate users with roles or equivalent access attributes.

Example roles may include:

```text
Employee
HR
IT
Finance
Administrator
```

### Acceptance Criteria

- user access scope can be determined;
- restricted documents cannot be retrieved by unauthorised users;
- permission checks occur before restricted document content enters the LLM context;
- access-control behaviour is testable.

---

## FR-003 — Document Ingestion

**Priority:** Must Have  
**Initial Status:** Planned

Authorised users shall be able to ingest supported organisational documents.

Target pipeline:

```text
Upload
 ↓
Validation
 ↓
Extraction
 ↓
Chunking
 ↓
Metadata
 ↓
Embedding
 ↓
Storage
```

### Acceptance Criteria

- supported documents can enter the ingestion pipeline;
- invalid/unsupported input is handled deliberately;
- ingestion failures return controlled errors;
- document identity is preserved.

---

## FR-004 — Text Extraction

**Priority:** Must Have  
**Initial Status:** Planned

The system shall extract searchable text from supported documents.

### Acceptance Criteria

- extracted content is available to the chunking process;
- extraction errors are detectable;
- empty documents are not silently indexed as valid knowledge.

---

## FR-005 — Document Chunking

**Priority:** Must Have  
**Initial Status:** Planned

Large documents shall be divided into retrieval-sized chunks.

### Acceptance Criteria

Each chunk maintains a relationship to its original document.

Where available, metadata should preserve information such as:

- document identifier;
- document title;
- section;
- page;
- chunk identifier.

Chunking strategy must be documented and evaluated rather than selected arbitrarily.

---

## FR-006 — Document Metadata

**Priority:** Must Have  
**Initial Status:** Planned

Documents and chunks shall contain metadata required for retrieval, traceability, lifecycle management, and access control.

Potential metadata includes:

```text
document_id
title
department
version
status
owner
effective_date
access_scope
section
page
chunk_id
```

Not every field must be required for every document type.

---

## FR-007 — Embedding Generation

**Priority:** Must Have  
**Initial Status:** Prototype Implemented

The system shall convert user queries and document chunks into numerical vector representations suitable for semantic retrieval.

### Acceptance Criteria

- document chunks can be embedded;
- user questions can be embedded;
- embedding failures are handled;
- embedding model information is documented.

---

## FR-008 — Persistent Vector Storage

**Priority:** Must Have  
**Initial Status:** Planned

Embeddings shall eventually be persisted rather than recreated from an in-memory Python list for every query.

Target technology:

```text
PostgreSQL + PGVector
```

### Acceptance Criteria

- document embeddings can be stored;
- embeddings can be queried;
- source metadata remains associated with embeddings;
- stored knowledge persists across application restarts.

---

## FR-009 — Semantic Retrieval

**Priority:** Must Have  
**Initial Status:** In Progress

The system shall retrieve document chunks based on semantic relevance to the user's question.

Initial retrieval concepts include:

- query embeddings;
- vector similarity;
- ranking;
- Top-K retrieval.

### Acceptance Criteria

- query is converted into an embedding;
- candidate chunks are compared/retrieved;
- results are ranked;
- configured Top-K results can be returned;
- retrieval results contain source metadata.

---

## FR-010 — Permission-Aware Retrieval

**Priority:** Must Have  
**Initial Status:** Planned

Retrieval shall respect the authenticated user's authorised knowledge scope.

The intended security boundary is:

```text
User
 ↓
Identity
 ↓
Permissions
 ↓
Authorised Retrieval Scope
 ↓
Vector Search
 ↓
Retrieved Evidence
 ↓
LLM
```

The application must not depend solely on asking the LLM to ignore unauthorised information.

### Acceptance Criteria

- retrieval queries can be restricted using access metadata;
- unauthorised chunks are excluded before generation;
- permission tests demonstrate expected behaviour.

---

## FR-011 — Ranked / Top-K Retrieval

**Priority:** Must Have  
**Initial Status:** Prototype Implemented / Refactoring In Progress

The system shall rank retrieved evidence by relevance and select a configurable number of results.

### Acceptance Criteria

- results are ordered by retrieval score;
- Top-K is configurable;
- retrieved chunks can be inspected during development/evaluation.

Top-K must not automatically be interpreted as evidence that every returned chunk is sufficiently relevant.

---

## FR-012 — Insufficient-Evidence Handling

**Priority:** Must Have  
**Initial Status:** Planned

The system shall support situations where available organisational knowledge does not provide sufficient evidence to answer the user's question.

Example:

Knowledge base:

```text
Annual Leave
Remote Working
Password Security
```

Question:

```text
What is our maternity leave policy?
```

The application should not invent a maternity policy simply because the retrieval system returns its closest available chunks.

### Acceptance Criteria

- unsupported questions exist in the evaluation dataset;
- system behaviour is measurable;
- unsupported organisational claims are not intentionally presented as verified company policy;
- fallback behaviour is visible to the user.

---

## FR-013 — Grounded LLM Generation

**Priority:** Must Have  
**Initial Status:** Prototype Implemented

The system shall provide retrieved evidence to the LLM when generating organisational answers.

### Acceptance Criteria

- question and retrieved context reach the generation layer;
- generation instructions distinguish organisational evidence from general model knowledge;
- insufficient evidence can produce an appropriate fallback;
- LLM provider logic remains separated from API request handling.

---

## FR-014 — Source Citations

**Priority:** Must Have  
**Initial Status:** Planned

Answers shall expose supporting source information.

Citation information should include as much of the following as the source supports:

```text
Document
Section
Page
Version
```

### Acceptance Criteria

- answer citations map to retrieved evidence;
- user can identify the source document;
- citations are not fabricated by the LLM independently of retrieval metadata.

---

## FR-015 — Question API

**Priority:** Must Have  
**Initial Status:** Foundation Implemented

The backend shall provide an API for submitting questions.

Target example:

```http
POST /questions
```

Conceptual request:

```json
{
  "question": "Can I work from home?"
}
```

Conceptual response:

```json
{
  "answer": "Employees may work remotely for up to two days per week.",
  "sources": [
    {
      "document": "Remote Working Policy",
      "section": "3.1"
    }
  ]
}
```

The final API contract will be documented separately.

---

## FR-016 — Health Endpoint

**Priority:** Must Have  
**Initial Status:** Implemented

The application shall expose a health/liveness endpoint.

The initial health endpoint proves application availability only.

Dependency readiness should not be claimed unless dependency checks are explicitly implemented.

---

## FR-017 — Knowledge Workspace

**Priority:** Must Have  
**Initial Status:** Planned

The frontend shall provide a minimal knowledge workspace.

Primary areas:

```text
Sources | Conversation
```

The interface should prioritise:

```text
Find → Ask → Verify
```

over dashboard complexity.

---

## FR-018 — Source Inspection

**Priority:** Must Have  
**Initial Status:** Planned

Users shall be able to inspect the evidence supporting an answer.

The target experience allows a citation to reveal or navigate to the relevant document context.

---

## FR-019 — Conversation Feedback

**Priority:** Should Have  
**Initial Status:** Planned

Users should be able to indicate whether an answer was useful or problematic.

Feedback may later support:

- evaluation;
- knowledge-gap identification;
- retrieval improvement;
- operational review.

---

## FR-020 — Document Lifecycle Awareness

**Priority:** Must Have  
**Initial Status:** Planned

The system shall be designed to distinguish document lifecycle states.

Potential states include:

```text
draft
active
superseded
archived
```

Retrieval should eventually favour or restrict documents according to approved lifecycle rules.

---

## FR-021 — Audit Events

**Priority:** Must Have  
**Initial Status:** Planned

Security- and knowledge-related activity should produce appropriate audit information.

Potential events include:

- authentication;
- document upload;
- document update;
- access denial;
- question submission;
- retrieved source identifiers;
- administrative action.

Sensitive content should not be indiscriminately logged.

---

# 8. RAG Requirements

The minimum target RAG pipeline is:

```text
Question
   ↓
Query Embedding
   ↓
Authorised Retrieval Scope
   ↓
Vector Search
   ↓
Ranking
   ↓
Top-K Evidence
   ↓
Evidence Validation
   ↓
Prompt Construction
   ↓
LLM
   ↓
Answer
   ↓
Citations
```

The project should allow individual stages to be evaluated independently.

---

# 9. Security Requirements

## SEC-001 — Secret Management

Secrets must not be committed to source control.

Development may use environment variables.

Production deployment should use an appropriate secret-management mechanism.

---

## SEC-002 — Authentication

Protected organisational knowledge requires authenticated identity.

---

## SEC-003 — Authorisation Before Generation

Restricted knowledge must be filtered before it is included in LLM context.

---

## SEC-004 — Input Validation

API and document inputs must be validated.

---

## SEC-005 — Document Trust Boundary

Retrieved documents must be treated as data, not trusted system instructions.

This is important because organisational documents may contain content that conflicts with application instructions or attempts to manipulate model behaviour.

---

## SEC-006 — Minimal Sensitive Logging

Sensitive document content, credentials, tokens, and unnecessary personal information must not be written indiscriminately to logs.

---

## SEC-007 — Development Data

Synthetic organisational documents should be used where external development services do not have suitable data-handling guarantees for confidential enterprise data.

---

# 10. Evaluation Requirements

The system must include a repeatable evaluation dataset.

A conceptual evaluation record may contain:

```json
{
  "question": "Can employees work remotely?",
  "expected_source": "Remote Working Policy",
  "expected_evidence": "up to two days per week",
  "user_role": "employee"
}
```

Evaluation categories should include:

### Retrieval

- expected source retrieved;
- retrieval at K;
- irrelevant retrieval;
- metadata filtering.

### Generation

- evidence-grounded answer;
- unsupported claims;
- citation consistency.

### Security

- authorised source retrieval;
- unauthorised source exclusion.

### Failure Behaviour

- unsupported question;
- provider failure;
- database failure;
- malformed request.

### Performance

- API latency;
- retrieval latency;
- model latency.

No target metric should be reported as achieved until measured.

---

# 11. Observability Requirements

The target system should make it possible to understand:

```text
What happened?
Where did it happen?
How long did it take?
Which evidence was retrieved?
Did an external dependency fail?
```

Observability should eventually cover:

- request identifiers;
- API latency;
- retrieval latency;
- LLM latency;
- errors;
- retrieval metadata;
- model/provider information;
- relevant audit events.

Sensitive content should be protected appropriately.

---

# 12. Reliability Requirements

The system should fail deliberately rather than unpredictably.

Expected failure categories include:

```text
Invalid Request
Authentication Failure
Authorisation Failure
Document Processing Failure
Embedding Failure
Retrieval Failure
Database Failure
LLM Provider Failure
Timeout
Insufficient Evidence
```

Each failure category should eventually have defined application behaviour.

---

# 13. Performance Requirements

Performance claims will be evidence-based.

The project will measure:

- request latency;
- retrieval latency;
- generation latency;
- relevant database performance.

Performance targets may be established after baseline measurements exist.

---

# 14. Maintainability Requirements

The backend should separate responsibilities.

Target direction:

```text
API Layer
   ↓
Application / RAG Layer
   ↓
Retrieval Service
   ↓
LLM Service
   ↓
Data / External Providers
```

Provider-specific implementation details should not unnecessarily spread across the application.

---

# 15. Testability Requirements

The system should support:

- unit testing;
- API testing;
- integration testing;
- retrieval evaluation;
- permission testing;
- failure-path testing.

External services should be mockable where appropriate so automated tests do not require unnecessary paid API calls.

---

# 16. Deployment Requirements

The target system should support reproducible execution using containers.

Target direction:

```text
Frontend
Backend
PostgreSQL + PGVector
```

with:

```text
Docker / Docker Compose
```

CI/CD should automate appropriate validation before deployment.

Cloud architecture should remain proportional to the project's actual requirements.

---

# 17. User Experience Requirements

## UX-001 — Simplicity

The normal employee interface should avoid unnecessary technical controls.

---

## UX-002 — Source First

Sources should remain visible and understandable.

---

## UX-003 — Citation Visibility

Users should be able to identify which organisational knowledge supports an answer.

---

## UX-004 — Clear Failure Behaviour

If the system lacks sufficient information, the UI should communicate this clearly.

---

## UX-005 — Progressive Complexity

Administrative and technical capabilities should not overwhelm ordinary users.

---

# 18. Initial Technology Direction

| Requirement | Current Technology Direction |
|---|---|
| Backend | Python + FastAPI |
| Validation | Pydantic |
| Dependency Management | uv |
| Development LLM | Gemini |
| Development Embeddings | Gemini Embedding |
| Persistent Database | PostgreSQL |
| Vector Search | PGVector |
| Frontend | Next.js + React + TypeScript |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Version Control | Git + GitHub |

Technology decisions will be documented separately with their rationale and alternatives.

---

# 19. Definition of Enterprise-Ready for This Project

The word **enterprise** will not be used merely because the application uses an LLM.

For this portfolio project, the target enterprise standard requires evidence across the following areas:

```text
Business Requirement
        +
Maintainable Architecture
        +
Persistent Data
        +
Security Boundaries
        +
Grounded Retrieval
        +
Traceability
        +
Evaluation
        +
Testing
        +
Failure Handling
        +
Observability
        +
Reproducible Deployment
```

The project will be described as enterprise-ready only to the extent supported by implemented and verified capabilities.

---

# 20. Definition of Done

The initial portfolio release is complete when the core user journey can be demonstrated end-to-end:

```text
Authorised User
      ↓
Knowledge Workspace
      ↓
Ask Question
      ↓
Permission-Aware Retrieval
      ↓
Relevant Evidence
      ↓
Grounded Generation
      ↓
Answer + Citation
      ↓
Source Verification
```

and when the repository contains evidence of:

- working frontend;
- working backend;
- document ingestion;
- persistent vector retrieval;
- authentication;
- permission-aware retrieval;
- grounded answers;
- citations;
- evaluation results;
- automated tests;
- containerisation;
- CI/CD;
- observability;
- documented architecture;
- deployment or reproducible deployment instructions.

---

# 21. Requirements Traceability

Implementation progress should eventually be tracked against requirement identifiers rather than vague feature claims.

Example:

| Requirement | Capability | Status | Evidence |
|---|---|---|---|
| FR-007 | Embeddings | Prototype Implemented | Retrieval experiment |
| FR-009 | Semantic Retrieval | In Progress | Retrieval service |
| FR-013 | Grounded Generation | Prototype Implemented | RAG experiment |
| FR-015 | Question API | Foundation Implemented | FastAPI endpoint |
| FR-016 | Health Endpoint | Implemented | `/health` |
| FR-002 | RBAC | Planned | — |
| FR-014 | Citations | Planned | — |

This table should be updated as implementation progresses.

---

# 22. Guiding Engineering Rule

Every proposed technology or architectural component must answer:

> **What requirement does this solve?**

If that question cannot be answered clearly, the component should not be added.

The objective is not maximum architectural complexity.

The objective is:

> **A simple product supported by defensible enterprise engineering.**
