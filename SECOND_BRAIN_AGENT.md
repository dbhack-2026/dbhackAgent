# Local Second-Brain Context Agent

This package retrieves context from a local `state.db` SQLite file and Markdown
knowledge files, then can call a GitHub Models-compatible chat-completions
endpoint using the same effective connection strategy as the working Java
utility shown during development.

The retrieval layer still has no third-party Python runtime dependency.

## Expected repository layout

```text
repo/
├── state.db
├── knowledge/
│   ├── services/
│   ├── architecture/
│   ├── incidents/
│   └── decisions/
└── second_brain_agent/
```

The Markdown files remain the human-readable source of knowledge. `state.db`
holds machine-readable relationships.

## SQLite schema

The graph traversal currently understands this minimal schema:

```sql
CREATE TABLE nodes (
    id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE relationships (
    source_id TEXT,
    relationship TEXT,
    target_id TEXT
);
```

`nodes` is optional. `relationships` is the important table.

Example:

```sql
INSERT INTO relationships VALUES
  ('daas-trade-manager', 'USES', 'kafka'),
  ('daas-trade-manager', 'STORES_IN', 'sql-server'),
  ('daas-trade-manager', 'CALLS', 'security-master');
```

The database is opened in SQLite read-only mode by the agent.

## Model connection strategy

The Python client in `second_brain_agent/inference.py` mirrors the behavior of
the working desktop utility:

1. Build a JSON request with `model` and `messages`.
2. POST it to the configured chat-completions endpoint.
3. Send the inference credential as an `Authorization: Bearer ...` header.
4. Optionally route the HTTPS request through an explicit corporate HTTP proxy.
5. Optionally authenticate to that proxy with username/password.
6. Parse the answer from `choices[0].message.content`.
7. Parse token counts from the response `usage` object when present.

Credentials are never hard-coded by this package and are never written to
`state.db` or Markdown notes.

### Environment variables

Set these in the IntelliJ run configuration, terminal environment, or an
enterprise-approved secret injection mechanism:

```text
SECOND_BRAIN_MODEL=your-model-id
SECOND_BRAIN_INFERENCE_TOKEN=your-inference-token
SECOND_BRAIN_MODELS_URL=https://models.github.ai/inference/chat/completions

# Only when your network requires an authenticated proxy:
SECOND_BRAIN_PROXY_HOST=your-proxy-host
SECOND_BRAIN_PROXY_PORT=8080
SECOND_BRAIN_PROXY_USERNAME=your-proxy-user
SECOND_BRAIN_PROXY_PASSWORD=your-proxy-password

# Optional
SECOND_BRAIN_TIMEOUT_SECONDS=120
```

See `second_brain_agent.env.example` for the same placeholders.

Do **not** put real tokens, proxy passwords, or personal credentials in the
repository.

## End-to-end run

From the repository root, after the environment variables are set:

```bash
python -m second_brain_agent.cli \
  --db state.db \
  --notes knowledge \
  "Why could daas-trade-manager be experiencing Kafka delays?"
```

The default flow is now:

```text
User prompt
    |
    v
Local context builder
    |-- query state.db read-only
    |-- traverse relationships
    |-- search relevant Markdown
    v
Compact context bundle
    |
    v
GitHub Models compatible endpoint
    |-- bearer inference token
    |-- optional authenticated corporate proxy
    v
Model answer
```

To inspect exactly what local context would be sent without making an inference
request:

```bash
python -m second_brain_agent.cli \
  --context-only \
  --db state.db \
  --notes knowledge \
  "What depends on Kafka?"
```

To print both the retrieved context and the answer:

```bash
python -m second_brain_agent.cli \
  --show-context \
  --db state.db \
  --notes knowledge \
  "What depends on Kafka?"
```

## Why the model cannot query `state.db` directly

The LLM itself is not given arbitrary SQL execution capability. The local
`ContextBuilder` performs bounded read-only retrieval first and sends only the
resulting context to the model. This keeps the database access deterministic
and prevents generated SQL from becoming an execution surface.

## IntelliJ integration

A normal AI chat plugin does not automatically call this local agent simply
because the files exist in the project. The immediate options are:

1. Run the CLI from the IntelliJ terminal.
2. Add the CLI as an IntelliJ External Tool.
3. If the installed AI plugin supports MCP/tool calling, expose the local
   context/inference agent as an MCP tool.
4. Otherwise create a small IntelliJ action/plugin that calls
   `SecondBrainAgent.ask()` and renders the returned answer.

The important part is now complete: `SecondBrainAgent.ask(prompt)` performs both
local retrieval and inference, so an IDE integration only needs to pass the
prompt and display the answer.

## Run the tests

The retrieval tests use the standard library only:

```bash
python -m unittest tests/test_second_brain_agent.py
```

Additional inference tests should mock the HTTP opener so no real credentials
or network calls are required during test execution.

## Security notes

- `state.db` is opened read-only.
- SQL parameters are bound rather than interpolated.
- TLS certificate verification remains enabled.
- Tokens and proxy credentials come only from environment variables.
- HTTP error bodies are truncated before being surfaced.
- The agent never logs authorization headers or credentials.
- Do not disable TLS verification to work around enterprise certificate issues;
  configure the machine/Python trust store correctly instead.
