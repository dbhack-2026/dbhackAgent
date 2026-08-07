# AI Agent Harness + Second Brain

**How persistent engineering context turns AI-assisted coding into a repeatable delivery system**

---

## Slide 1 — AI Agent Harness + Second Brain

### Harness
- Instructions
- Tools
- Guardrails
- Workflow

### Second Brain
- Persistent architecture
- Domain knowledge
- Decisions
- Lessons learned

### Knowledge Graph
- Relationship-aware retrieval
- Compact, task-specific context for prompts

### Goal
**Less context hunting → fewer rework loops → safer changes → faster delivery**

---

## Slide 2 — The problem: coding AI is powerful, but context is fragmented

### Without a harness
Every prompt starts from scratch.

Developers repeatedly explain:
- Architecture
- Conventions
- APIs
- Dependencies
- Test expectations
- Prior decisions

### What the model sees
- Current file
- Current prompt
- Whatever context was manually attached

Missing relationships can lead to plausible code that violates local constraints.

### Result
- Context hunting
- Repeated explanations
- Inconsistent outputs
- More review cycles
- Knowledge lost between sessions

---

## Slide 3 — What an AI agent harness adds

**A thin operating layer around the coding model**

1. **Understand** — Task template + acceptance criteria
2. **Retrieve** — Relevant service/domain context
3. **Plan** — Bounded change plan + impacted files
4. **Execute** — Code using approved tools/patterns
5. **Validate** — Build • tests • static checks • diff
6. **Learn** — Capture decision, fix, and reusable lesson

### Key shift
**The prompt is no longer the workflow.**

The harness assembles the right prompt, context, tools, and validation for the workflow.

---

## Slide 4 — Why the harness accelerates AI-assisted coding

### Less context hunting
Architecture and service facts are retrieved automatically.

### Reusable prompts
Common tasks become structured, repeatable playbooks.

### Fewer rework loops
Constraints and acceptance criteria arrive before code generation.

### Automatic conventions
Patterns, libraries, security rules, and testing standards travel with the task.

### Repeatable validation
Build/test/review steps are part of the agent workflow.

### Compounding learning
Every resolved incident or design choice improves the next task.

---

## Slide 5 — The Second Brain: persistent engineering memory

### What it remembers
- Architecture decisions & constraints
- Service maps and dependencies
- APIs, topics, schemas, and tables
- Domain vocabulary
- Known errors and fixes
- Runbooks and review checklists
- Prompt templates and coding patterns

### Why it matters
Chat history is not a reliable engineering knowledge system.

A curated Second Brain gives durable, versionable, and reusable context across sessions, developers, repositories, and agents.

### Design principle
1. Store knowledge once.
2. Retrieve only what the current task needs.
3. Do **not** send the whole knowledge base to the LLM.
4. Compile a compact context bundle for each prompt.

---

## Slide 6 — Knowledge graph = a smarter Second Brain

**Relationships make retrieval more useful than keyword search alone.**

### Example: Microservice relationships
A microservice can be connected to:

- **Kafka topics** → publishes / consumes
- **SQL tables** → reads / writes
- **Architecture decisions** → constrained by
- **Known incidents** → affected by
- **Test & security rules** → validated by

### Why this helps
Instead of retrieving isolated documents, the system can traverse relationships and identify the context that is truly relevant to a change.

---

## Slide 7 — How the Second Brain improves prompting

**Prompt quality comes from selected evidence, not prompt length.**

### User asks
> “Add a new harmonization rule to the trade service and update tests.”

### Context compiler retrieves
- Service responsibilities
- Relevant harmonization maps
- Current coding conventions
- Impacted Kafka/API contracts
- Existing tests
- Known constraints / ADRs
- Similar previous changes

### Compiled prompt
- **GOAL**
- **SCOPE**
- **CONSTRAINTS**
- **EVIDENCE**
- **ACCEPTANCE CRITERIA**
- **OUTPUT FORMAT**
- **VALIDATION STEPS**

---

## Slide 8 — Recommended architecture: Context OS for coding agents

### Sources
Git • Jira • Docs • code • telemetry • conversations

### Knowledge layer
Markdown / ADRs + searchable index + knowledge graph

### Context compiler
Task classification → graph traversal → evidence ranking → prompt pruning

### Agent harness
Planner → coder → reviewer → validator → documentation / memory

### Coding surfaces
IntelliJ • GitHub Copilot • CLI • CI

---

## Slide 9 — Prompt-first operating model

**Keep the knowledge outside ad hoc prompts; inject only what is needed.**

### Persistent assets
- `AGENTS.md`
- `ARCHITECTURE.md`
- `SERVICES.md`
- `DOMAINS.md`
- ADRs
- `patterns/`
- `skills/`
- `prompts/`
- `incidents/`

### Task input
- Goal
- Requirement
- Target service
- Constraints
- Acceptance criteria
- Requested output

### Retrieval
- Semantic search
- Graph traversal
- Recent decisions
- Similar fixes
- Dependency expansion
- Prompt pruning

### Compact context bundle
Only the evidence required for the task.

Benefits:
- Stable prefix can be cached
- Task-specific context stays small
- Output becomes more consistent
- Output becomes more idempotent

---

## Slide 10 — Adoption path: build the memory before adding autonomy

### 1. Context files
Architecture, services, domain, standards

### 2. Prompt templates
Repeatable inputs + expected outputs

### 3. Retrieval index
Search the right snippets automatically

### 4. Knowledge graph
Follow relationships and dependencies

### 5. Agent workflows
Plan → code → test → review → learn

### Compounding advantage
**Every task can leave the system with better context for the next task.**

---

## Slide 11 — What success looks like

**Measure the harness as an engineering productivity system.**

### Context reuse
% of tasks using retrieved context

### First-pass quality
Changes accepted with minimal rework

### Cycle time
Prompt → validated change

### Knowledge capture
Decisions/fixes added back to memory

### Core message
**AI-assisted coding scales when the organization stops treating each prompt as a fresh conversation and starts treating context as reusable engineering infrastructure.**

---

## Slide 12 — Final message

### AI Agent Harness
**Execution discipline**

### Second Brain
**Persistent engineering memory**

### Knowledge Graph
**Relationship-aware context retrieval**

### Together
They transform AI coding from isolated autocomplete into a reusable, governed, and continuously improving engineering system.
