# Business Problem

**Project:** Enterprise Knowledge Copilot  
**Document Status:** Approved Project Specification  
**Implementation Status:** 🚧 Active Development

---

## 1. Background

Modern organisations generate and maintain large volumes of internal knowledge.

This knowledge may include:

- employee handbooks;
- HR policies;
- remote-working policies;
- annual-leave guidance;
- IT procedures;
- cybersecurity policies;
- compliance documentation;
- operational procedures;
- technical documentation;
- training materials;
- internal standards.

Although this information exists, employees may still struggle to locate the correct answer when they need it.

Knowledge is often distributed across document repositories, shared drives, internal portals, email attachments, and departmental systems.

The challenge is therefore not simply whether organisational information exists.

The challenge is:

> **Can an employee retrieve the correct, current and authorised information quickly enough to make a reliable decision?**

---

## 2. Problem Statement

Traditional enterprise search often requires employees to know:

- where a document is stored;
- which document contains the answer;
- which search terms to use;
- whether the document is current;
- whether another version exists;
- which section contains the relevant information.

Employees may therefore spend unnecessary time searching through documents or asking colleagues and subject-matter experts questions that have already been documented.

Generative AI provides a more natural way of accessing information, but directly sending organisational questions to a general-purpose Large Language Model creates another problem.

An LLM may:

- not have access to private organisational information;
- not know the latest company policy;
- generate a plausible but unsupported answer;
- combine general knowledge with company-specific questions;
- provide an answer without showing its evidence.

For enterprise use, an answer that merely **sounds correct** is insufficient.

The system must help users determine:

> **Where did this answer come from?**

---

## 3. Example Business Scenario

Consider an employee who asks:

```text
Can I work from home?
```

A general-purpose LLM may know what remote-working policies commonly look like.

However, it does not automatically know the organisation's approved remote-working policy.

The correct organisational answer may be:

```text
Employees may work remotely for up to two days per week,
subject to approval from their line manager.
```

The system should therefore retrieve the relevant organisational policy before generating the answer.

Target flow:

```text
Employee Question
        ↓
Identify Authorised Knowledge
        ↓
Retrieve Relevant Policy Information
        ↓
Provide Evidence to the LLM
        ↓
Generate Grounded Answer
        ↓
Return Answer + Source
```

The employee should be able to verify the response against its supporting document.

---

## 4. Why a Simple Chatbot Is Not Enough

This project is deliberately not designed as a generic chatbot or a simple "chat with PDF" application.

A production-oriented enterprise knowledge system must consider several additional problems.

### 4.1 Knowledge Grounding

The system must distinguish between:

- the LLM's general knowledge; and
- approved organisational knowledge.

Organisational answers should be generated from retrieved evidence wherever the use case requires company-specific information.

---

### 4.2 Source Traceability

Users should be able to identify the evidence supporting an answer.

Target citation metadata may include:

- document title;
- document section;
- page where available;
- document version;
- source identifier.

---

### 4.3 Access Control

Not every employee should necessarily be able to retrieve every document.

For example:

```text
Employee
   ├── General HR Policies
   ├── IT Policies
   └── Employee Handbook

Finance Team
   ├── General Policies
   └── Finance Documents

Executives
   ├── General Policies
   └── Restricted Executive Documents
```

The system must therefore eventually combine retrieval with authorisation.

A critical architectural principle is:

> **Authorisation should restrict the retrieval scope before confidential document content is provided to the LLM.**

This reduces the risk of unauthorised information entering the model context.

---

### 4.4 Outdated Knowledge

Policies change.

A knowledge system may contain:

```text
Remote_Working_Policy_v1
Remote_Working_Policy_v2
Remote_Working_Policy_v3
```

Retrieving an obsolete version could produce an incorrect answer even if semantic retrieval itself works correctly.

Document metadata and lifecycle management are therefore part of the target design.

---

### 4.5 Unsupported Questions

Retrieval systems normally return the closest available results.

However:

> **Closest does not necessarily mean relevant enough.**

Suppose the knowledge base contains only:

```text
Annual Leave Policy
Remote Working Policy
Password Security Policy
```

and the employee asks:

```text
What is our maternity leave policy?
```

A similarity search may still return one or more of those documents.

The system must therefore be designed to recognise situations where the available evidence is insufficient rather than treating every Top-K result as a valid answer source.

---

### 4.6 Conflicting Information

Different documents may contain conflicting information.

For example:

```text
Policy A:
Employees may work remotely 3 days per week.

Policy B:
Employees may work remotely 2 days per week.
```

A production knowledge system must eventually consider metadata such as:

- version;
- publication date;
- approval status;
- document owner;
- effective date.

The LLM should not silently decide which policy represents organisational truth without appropriate evidence or rules.

---

## 5. Proposed Solution

Enterprise Knowledge Copilot is designed as a source-grounded Generative AI platform for organisational knowledge.

The target solution combines:

- document ingestion;
- text extraction;
- chunking;
- metadata;
- embeddings;
- semantic retrieval;
- vector search;
- permission-aware filtering;
- grounded LLM generation;
- citations;
- evaluation;
- observability;
- auditability.

The high-level architecture is:

```text
Organisational Documents
          ↓
       Ingestion
          ↓
        Parsing
          ↓
       Chunking
          ↓
       Metadata
          ↓
      Embeddings
          ↓
 PostgreSQL + PGVector
          ↓
          ↓
Employee Question
          ↓
   Authentication
          ↓
    Authorisation
          ↓
  Query Embedding
          ↓
Permission-Aware Search
          ↓
    Ranked Evidence
          ↓
   Grounded Generation
          ↓
 Answer + Citations
```

---

## 6. Target Users

### 6.1 Employees

Employees need fast access to reliable organisational information without manually searching multiple documents.

Typical questions could include:

```text
How many days of annual leave do I receive?
```

```text
Can I work remotely?
```

```text
How frequently must I change my company password?
```

---

### 6.2 Knowledge Owners

Knowledge owners may include:

- HR teams;
- IT teams;
- security teams;
- compliance teams;
- operations teams.

They are responsible for organisational information that employees need to access.

The target system should eventually allow authorised knowledge owners to manage relevant source documents.

---

### 6.3 Administrators

Administrators may require capabilities such as:

- user management;
- role management;
- document management;
- access-control configuration;
- audit review;
- system monitoring.

Administrative functionality should remain separated from the simplified employee experience.

---

## 7. Business Objectives

The project aims to demonstrate how Generative AI can improve access to organisational knowledge while maintaining enterprise engineering principles.

The primary objectives are to:

1. reduce the effort required to find organisational information;
2. generate answers grounded in approved documents;
3. provide supporting sources for important answers;
4. prevent unsupported organisational claims where evidence is insufficient;
5. respect document access boundaries;
6. support document version and metadata awareness;
7. evaluate retrieval and answer quality;
8. provide operational visibility into the system;
9. create a simple employee experience despite complex backend engineering.

---

## 8. Functional Requirements

The target product is expected to support the following capabilities as development progresses.

### FR-01 — Document Ingestion

Authorised users should be able to add supported organisational documents to the knowledge base.

### FR-02 — Text Processing

Documents should be converted into searchable text.

### FR-03 — Chunking

Large documents should be divided into meaningful retrieval units.

### FR-04 — Metadata

Chunks should retain metadata connecting them to their original source.

### FR-05 — Embeddings

Document chunks and user queries should be represented as embeddings for semantic retrieval.

### FR-06 — Retrieval

The system should retrieve and rank relevant authorised document chunks.

### FR-07 — Grounded Generation

The LLM should receive retrieved organisational evidence when generating company-specific answers.

### FR-08 — Citations

Generated answers should expose their supporting source information.

### FR-09 — Insufficient Evidence

The system should support an appropriate response when the available knowledge does not sufficiently answer a question.

### FR-10 — Authentication

Users should be identifiable before accessing protected organisational knowledge.

### FR-11 — Authorisation

Retrieval should respect the user's permitted knowledge scope.

### FR-12 — Document Lifecycle

The system should support metadata required to distinguish current, obsolete, draft, or otherwise controlled documents.

### FR-13 — Feedback

Users should eventually be able to provide feedback on generated answers.

### FR-14 — Auditability

Relevant system activity should be recorded for operational and governance purposes.

---

## 9. Non-Functional Requirements

### Security

The system should minimise the risk of exposing organisational information to unauthorised users or inappropriate services.

### Reliability

External service failures should not cause uncontrolled application behaviour.

### Traceability

Important generated answers should be traceable to their supporting knowledge.

### Maintainability

Application responsibilities should remain separated into understandable components.

### Testability

Core services should be testable independently.

### Observability

The system should provide sufficient information to diagnose errors, latency, retrieval problems, and model failures.

### Performance

Response latency should be measured and improved based on evidence rather than assumed.

### Scalability

The architecture should permit retrieval and application components to evolve as document and user volumes increase.

### Usability

The employee-facing interface should remain simple.

The primary experience should follow:

> **Find → Ask → Verify**

---

## 10. Success Criteria

The project will not define success using unsupported claims such as:

```text
99% accurate
```

without measurement.

Instead, the project will establish an evaluation dataset containing representative questions and expected evidence.

Success will be evaluated using measurable indicators such as:

- expected-source retrieval;
- retrieval quality at K;
- citation correctness;
- grounded answer behaviour;
- unsupported-question handling;
- access-control test outcomes;
- API reliability;
- response latency.

Actual results will be documented after the relevant evaluation experiments have been implemented.

---

## 11. Constraints

### Development Cost

The project currently follows a **free-first development strategy**.

Paid infrastructure or APIs should not be introduced unless they become necessary and their purpose is understood.

### Development Data

Synthetic organisational documents are used during early development.

Real confidential enterprise documents should not be sent to external development services without an appropriate organisational agreement and data-handling assessment.

### Time

The project is being developed through an intensive portfolio sprint.

This means implementation decisions must prioritise features that demonstrate genuine engineering value rather than unnecessary architectural complexity.

---

## 12. Out of Scope for the Initial Release

The following are not initial requirements unless later justified:

- autonomous multi-agent organisations;
- Kubernetes deployment solely for portfolio complexity;
- multiple vector databases performing the same role;
- unnecessary microservices;
- blockchain;
- custom foundation-model training;
- replacing enterprise document-management systems;
- unrestricted internet search.

These capabilities should not be added merely to increase the number of technologies in the project.

---

## 13. Key Risks

| Risk | Example | Target Mitigation |
|---|---|---|
| Hallucination | LLM invents company policy | Ground responses in retrieved evidence |
| Poor retrieval | Wrong chunk ranks highly | Retrieval evaluation and ranking improvements |
| Data leakage | Restricted document enters context | Permission-aware retrieval |
| Stale information | Old policy is retrieved | Version/status metadata |
| Missing information | No document answers question | Insufficient-evidence behaviour |
| Provider outage | LLM API unavailable | Error handling and resilience strategy |
| Prompt injection | Document contains malicious instructions | Treat retrieved content as untrusted data |
| Secret exposure | API key committed to GitHub | Environment/secret management |
| Untraceable answer | User cannot verify response | Source citations |

Mitigations listed above represent the target architecture and will be marked as implemented only when supported by code and tests.

---

## 14. Expected Business Value

If implemented successfully, an enterprise knowledge assistant of this type could help organisations:

- reduce time spent searching internal documentation;
- reduce repetitive questions to support teams;
- improve discoverability of organisational knowledge;
- make AI-generated answers easier to verify;
- provide a consistent interface across multiple knowledge domains;
- identify knowledge gaps through unanswered questions;
- improve visibility into how organisational information is being accessed.

These are intended product outcomes. They are not claimed as measured benefits of the current prototype.

---

## 15. Product Principle

The project is governed by one central idea:

> **Simple outside. Serious engineering underneath.**

Employees should not need to understand embeddings, vector databases, RAG pipelines, access filters, evaluation frameworks, or LLM providers.

They should experience:

```text
Find
 ↓
Ask
 ↓
Verify
```

The engineering underneath is responsible for making that interaction reliable, traceable, secure, measurable, and maintainable.
