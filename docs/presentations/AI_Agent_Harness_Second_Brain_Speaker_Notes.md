# AI Agent Harness + Second Brain — Speaker Talk Track

Companion speaker notes for the presentation **AI Agent Harness + Second Brain: How persistent engineering context turns AI-assisted coding into a repeatable delivery system**.

---

## Slide 1 — AI Agent Harness + Second Brain

### Main message
AI-assisted coding becomes much more valuable when we combine the model with reusable context, workflows, and engineering memory.

### Talking points
- AI coding tools are already good at generating code, but code generation alone is not the main bottleneck.
- The bigger challenge is giving AI the **right context at the right time**.
- An **Agent Harness** provides instructions, tools, guardrails, and a repeatable workflow.
- A **Second Brain** preserves architecture, domain knowledge, decisions, lessons, and reusable engineering knowledge.
- A **Knowledge Graph** connects those pieces so the system understands relationships rather than isolated documents.
- The goal is to move from repeated context gathering toward **faster and safer software delivery**.

### What to explain to the audience
Think of the LLM as the engine. The harness is the operating system around that engine, while the Second Brain provides long-term organizational memory.

---

## Slide 2 — The problem: coding AI is powerful, but context is fragmented

### Main message
Most AI coding inefficiency comes from repeatedly rebuilding context.

### Talking points
- Developers often start each AI conversation almost from zero.
- We repeatedly explain architecture, APIs, coding patterns, dependencies, testing requirements, business rules, and previous decisions.
- The model usually sees the current file, the prompt, and whatever context we manually attach.
- It may generate code that is syntactically correct but architecturally wrong.
- This creates context hunting, inconsistent implementation, repeated explanations, additional review cycles, and loss of knowledge across sessions.

### What to explain to the audience
The AI is often not failing because it cannot code. It is failing because we have not given it enough organizational knowledge to make the correct engineering decision.

A useful example is: **“Add a new Kafka consumer.”** Without context, AI does not know the organization’s retry approach, partitioning strategy, error handling, observability requirements, naming conventions, or deployment constraints.

---

## Slide 3 — What an AI agent harness adds

### Main message
The harness converts prompting into a structured engineering process.

### Talking points
1. **Understand** — identify the requirement and acceptance criteria.
2. **Retrieve** — find relevant service, domain, architecture, and historical context.
3. **Plan** — determine impacted files and bounded changes.
4. **Execute** — generate or modify code using approved patterns and tools.
5. **Validate** — build, test, run static analysis, and inspect the diff.
6. **Learn** — capture important decisions or fixes for future tasks.

### What to explain to the audience
Today we often ask: **“Implement this requirement.”**

With a harness, the system internally transforms that into:

**Understand → collect context → plan → implement → verify → retain knowledge**

The key idea is that **the prompt is no longer the entire workflow**.

---

## Slide 4 — Why the harness accelerates AI-assisted coding

### Main message
Acceleration comes mainly from reducing repeated reasoning and rework.

### Talking points
- **Less context hunting:** service and architecture information can be retrieved automatically.
- **Reusable prompts:** common engineering tasks become predefined playbooks.
- **Fewer rework loops:** constraints are given before AI writes code.
- **Automatic conventions:** frameworks, libraries, security requirements, and patterns travel with the task.
- **Repeatable validation:** testing is part of the agent process instead of something remembered afterward.
- **Compounding learning:** solved incidents improve future tasks.

### What to explain to the audience
The objective is not simply to generate code faster. The real productivity gain is to **generate the right change with fewer iterations**.

One 30-second code generation followed by two hours of corrections is not acceleration.

---

## Slide 5 — The Second Brain: persistent engineering memory

### Main message
Important engineering knowledge should survive beyond individual conversations.

### Talking points
The Second Brain can hold:
- Architecture decisions and constraints
- Service responsibilities and dependencies
- APIs and Kafka topics
- Schemas and database tables
- Domain vocabulary
- Known errors and fixes
- Runbooks and review checklists
- Coding patterns and prompt templates
- Testing and security practices

### What to explain to the audience
Chat history is useful, but it is not a reliable engineering knowledge system.

A Second Brain should be:
- Persistent
- Structured
- Searchable
- Versionable
- Reusable by multiple developers and agents

Most importantly: **do not send the whole Second Brain to the model**. Retrieve only the small portion relevant to the current task. This keeps prompts focused and reduces token usage.

---

## Slide 6 — Knowledge graph = a smarter Second Brain

### Main message
Knowledge becomes significantly more powerful when relationships are represented explicitly.

### Talking points
Use the microservice in the center of the diagram to explain relationships such as:
- Service **consumes** Kafka topic
- Service **publishes** another topic
- Service **reads/writes** specific SQL tables
- Service is **constrained by** an architecture decision
- Service was **affected by** a previous production incident
- Service is **validated by** particular security and testing requirements

### What to explain to the audience
Keyword search may find documents mentioning a service.

A Knowledge Graph can answer a more valuable engineering question: **“If I modify this service, what else is likely to be affected?”**

Retrieval can then follow relationships such as:

**Service → API → downstream consumer → schema → test → architecture decision**

This is more useful than searching isolated documents independently.

---

## Slide 7 — How the Second Brain improves prompting

### Main message
Better prompts are created by selecting better evidence, not by simply making prompts longer.

### Talking points
Use the example: **“Add a new harmonization rule to the trade service and update tests.”**

The context compiler can retrieve:
- Service responsibilities
- Current harmonization configuration
- Coding conventions
- Impacted Kafka or API contracts
- Existing tests
- Architecture decisions
- Previous similar implementations

It then constructs a focused prompt containing:
- **Goal**
- **Scope**
- **Constraints**
- **Evidence**
- **Acceptance criteria**
- **Output format**
- **Validation steps**

### What to explain to the audience
Instead of developers manually writing very large prompts, the system creates the prompt dynamically.

The user gives **intent**. The harness produces **context-rich instructions**.

---

## Slide 8 — Recommended architecture: Context OS for coding agents

### Main message
Treat engineering context as a platform capability.

### Talking points
#### Sources
- Git
- Jira
- Documentation
- Source code
- Telemetry
- Previous conversations

#### Knowledge layer
- Markdown
- ADRs
- Search index
- Knowledge Graph

#### Context compiler
- Classify the task
- Retrieve related knowledge
- Rank evidence
- Remove irrelevant content

#### Agent harness
- Planner
- Coder
- Reviewer
- Validator
- Memory/documentation writer

#### Coding surfaces
- IntelliJ
- GitHub Copilot
- CLI
- CI/CD

### What to explain to the audience
The idea is not to replace existing developer tools. Instead, the same organizational intelligence can sit behind multiple coding experiences.

An IntelliJ developer and a CI agent can therefore use the **same engineering knowledge base**.

---

## Slide 9 — Prompt-first operating model

### Main message
Separate persistent knowledge from task-specific prompting.

### Talking points
Persistent assets may include:
- `AGENTS.md`
- `ARCHITECTURE.md`
- `SERVICES.md`
- `DOMAINS.md`
- ADRs
- `patterns/`
- `skills/`
- `prompts/`
- `incidents/`

For each task, the developer provides only:
- Goal
- Requirement
- Target service
- Constraints
- Acceptance criteria
- Desired output

The retrieval system then performs:
- Semantic search
- Graph traversal
- Dependency expansion
- Previous-fix retrieval
- Prompt pruning

### What to explain to the audience
This is particularly important for token efficiency.

Instead of putting dozens of documents into every prompt, **store them once, retrieve the relevant pieces, and create a compact context bundle**.

Stable context can also be reused or cached while task-specific information changes.

---

## Slide 10 — Adoption path: build the memory before adding autonomy

### Main message
Do not jump directly to fully autonomous coding agents.

### Talking points
#### Stage 1 — Context files
Document architecture, services, domains, and standards.

#### Stage 2 — Prompt templates
Standardize how recurring engineering tasks are described.

#### Stage 3 — Retrieval index
Automatically discover relevant information.

#### Stage 4 — Knowledge Graph
Add dependencies and relationships.

#### Stage 5 — Agent workflows
Plan → code → test → review → learn.

### What to explain to the audience
Organizations often try to start at Stage 5, but autonomous agents without good context simply automate mistakes faster.

The better sequence is:

**Knowledge first → retrieval second → autonomy third**

---

## Slide 11 — What success looks like

### Main message
Measure quality and context reuse, not just the amount of AI-generated code.

### Talking points
Track metrics such as:
- **Context reuse:** percentage of tasks successfully using reusable engineering knowledge
- **First-pass quality:** how often generated changes are accepted with minimal correction
- **Cycle time:** time from requirement to validated implementation
- **Knowledge capture:** how many important fixes and decisions are added back to the Second Brain

Additional measures can include:
- Review iterations
- Escaped defects
- Build failures
- Prompt size
- Token usage
- Developer time spent collecting context

### What to explain to the audience
The wrong KPI is: **“How many lines of AI-generated code did we produce?”**

A better KPI is: **“How much engineering effort did we eliminate while maintaining or improving quality?”**

---

## Slide 12 — Final message

### Main message
Bring the three concepts together.

### Talking points
- **AI Agent Harness = execution discipline**
- **Second Brain = persistent engineering memory**
- **Knowledge Graph = relationship-aware context retrieval**

Together they create a system where:

**Developer intent**
↓
**Relevant organizational knowledge**
↓
**Structured agent workflow**
↓
**Validated code change**
↓
**New knowledge captured**

The process continuously improves.

### Strong closing statement
The real opportunity with AI-assisted development is not merely giving every developer a more powerful autocomplete. It is giving AI access to the same architecture knowledge, domain understanding, engineering standards, previous decisions, and lessons that an experienced engineer gradually builds over years.

The Agent Harness provides the process, the Second Brain provides the memory, and the Knowledge Graph provides the relationships. Together, they allow AI-assisted coding to become repeatable, scalable, and continuously improving.

### Final line
> **Don’t make every AI prompt rediscover your engineering organization.**
