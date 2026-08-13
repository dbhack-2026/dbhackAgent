# Local Second-Brain Context Agent

This package retrieves context from a local `state.db` SQLite file and Markdown
knowledge files without requiring a database server or any third-party Python
package.

It is intentionally separated from the existing Vertex/Gemini application.
The retrieval layer can later be called from an IntelliJ integration, an MCP
server, a local HTTP endpoint, or an LLM wrapper.

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

## Run locally

From the repository root:

```bash
python -m second_brain_agent.cli \
  --db state.db \
  --notes knowledge \
  "Why could daas-trade-manager be experiencing Kafka delays?"
```

The output is Markdown suitable for supplying to an LLM:

```text
# Retrieved second-brain context

## Query
Why could daas-trade-manager be experiencing Kafka delays?

## Knowledge-graph relationships
- daas-trade-manager --USES--> kafka
...

## Relevant notes
### knowledge/services/daas-trade-manager.md
...
```

## Run the tests

No external packages are needed:

```bash
python -m unittest tests/test_second_brain_agent.py
```

## IntelliJ integration

A normal ChatGPT IntelliJ plugin will not automatically execute this local
retrieval code merely because `state.db` is in the project. There must be an
integration point.

Recommended progression:

1. **Validate retrieval from the IntelliJ terminal** using the CLI above.
2. Add the CLI as an IntelliJ **External Tool** so it can run against the current
   project.
3. If the AI plugin supports **MCP/tool calling**, expose `ContextBuilder.build`
   through a small local MCP server and let the model call it as a tool.
4. If the plugin has no tool-extension mechanism, build a small IntelliJ plugin
   or local wrapper that sends the user prompt to this context builder first,
   then sends `context + prompt` to the chosen LLM.

The important boundary is:

```text
User prompt
    |
    v
Local context agent
    |-- query state.db
    |-- traverse relationships
    |-- search relevant Markdown
    v
Compact context bundle
    |
    v
LLM / IntelliJ AI integration
```

This avoids sending the whole second brain on every request and avoids allowing
the LLM to execute arbitrary SQL.

## Next extension

The next useful addition is a tool interface with a few narrow operations such
as:

- `find_entity(name)`
- `find_related(entity)`
- `search_notes(query)`
- `build_context(prompt)`

Those can be exposed over MCP or a local endpoint when the IntelliJ AI plugin's
extension mechanism is known.
