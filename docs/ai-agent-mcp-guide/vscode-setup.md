# Complete VS Code MCP and Agent Skills Setup

This is a **generic, hands-on guide** using public example servers. It contains no employer names, private endpoints, internal repository identifiers, or credentials. Check your organization's software policy before installing Node.js, npm packages, or any command-line tool.

## 1. Install and verify prerequisites

Install a supported Node.js **LTS** release from https://nodejs.org/ (or your approved software catalog). npm is normally bundled with Node.js.

Open **VS Code → Terminal → New Terminal** and run:

```powershell
node --version
npm --version
npx --version
git --version
```

If a command is missing, check installation and PATH; restart VS Code after installation. On Windows, `where.exe node` and `where.exe npm` can help identify binaries. `npx` runs package executables; it may download packages, so only use approved, reviewed sources. For a restricted corporate workstation, skip unapproved local CLI installation and use approved remote MCP servers through the IDE.

## 2. Create a workspace

```powershell
mkdir mcp-demo
cd mcp-demo
mkdir .vscode
mkdir .agents
mkdir .agents\skills
code .
```

Expected layout:

```text
mcp-demo/
  .vscode/mcp.json
  .agents/skills/security-remediation/SKILL.md
  audit/vulnerabilities.md
```

The `mcp.json` file configures MCP **servers**; `SKILL.md` configures reusable **agent instructions**. These are separate mechanisms.

## 3. Add a server through the VS Code interface

1. Open the workspace in VS Code.
2. Open the **Command Palette** (`Ctrl+Shift+P` on Windows).
3. Run **MCP: Add Server** (exact wording depends on VS Code version).
4. Choose **Command (stdio)** for a local server, or **HTTP** for a remote server.
5. Supply the command/URL, give the server a friendly name, and select **Workspace** scope.
6. Inspect the generated `.vscode/mcp.json`.
7. Run **MCP: List Servers** or **MCP: Browse MCP Servers** where supported; start the server and inspect tools.

If your version lacks these commands, use the MCP configuration UI provided by your VS Code version/extension, or create the JSON manually as below.

## 4. Understand `.vscode/mcp.json`

VS Code's workspace MCP configuration uses a top-level `servers` object.

### Example A: remote HTTP MCP server (recommended when available)

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "sample-remote": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

**Important:** `mcp.example.com` is a nonfunctional placeholder. Replace it with an authorized MCP endpoint from the provider's documentation. An ordinary REST endpoint is **not** automatically an MCP endpoint.

### Example B: remote HTTP server with a token

```json
{
  "inputs": [
    {
      "id": "sample-mcp-token",
      "type": "promptString",
      "description": "Access token for the approved MCP server",
      "password": true
    }
  ],
  "servers": {
    "sample-remote": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:sample-mcp-token}"
      }
    }
  }
}
```

VS Code can prompt for the token via the `inputs` mechanism. Do not put the token itself in the file. Some servers use OAuth or different header names: follow the server provider's authentication instructions.

### Example C: local stdio MCP server through `npx`

The following is a **generic configuration pattern**, not an endorsement of a particular npm package:

```json
{
  "servers": {
    "example-local": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@example/your-approved-mcp-server"],
      "env": {
        "EXAMPLE_MODE": "read-only"
      }
    }
  }
}
```

Replace `@example/your-approved-mcp-server` with a real, reviewed npm package and replace environment variables with those documented by its publisher. This example will not work unchanged. On some Windows systems `npx.cmd` may be needed. For security and reproducibility, prefer an approved, pinned package version and a vetted package registry; `-y` suppresses install prompts.

### JSON fields explained

| Field | Meaning |
|---|---|
| `servers` | Map of server names to configuration |
| `sample-remote` | Friendly, unique server identifier |
| `type` | Transport: typically `http` or `stdio` |
| `url` | Remote MCP endpoint (HTTP transport only) |
| `headers` | HTTP headers, often for authorization |
| `command` | Executable for a local stdio server |
| `args` | Command-line arguments for that executable |
| `env` | Environment variables passed to the local server process |
| `inputs` | Prompts for sensitive or runtime configuration values |

Do not use `mcpServers` in this VS Code example: that key appears in configurations for **other MCP clients**. Do not assume an SSE URL can be substituted for an HTTP endpoint; use the transport the server supports.

## 5. Start the server and verify connectivity

1. Save `.vscode/mcp.json`.
2. Use the inline **Start** action above the server, if shown, or the MCP server command palette.
3. Open **GitHub Copilot Chat → Agent** mode.
4. Check that the server's tools are listed and enabled.
5. Try: *List the available tools from sample-remote and explain their inputs. Do not perform writes.*
6. Run a read-only query and compare its result with the source service.

If a remote URL is just a placeholder, connection will fail until replaced with a real endpoint. Server registration alone does not establish access.

## 6. Add an agent skill

Create `.agents/skills/security-remediation/SKILL.md`:

```markdown
---
name: security-remediation
description: Analyze a local vulnerability report and propose minimal, tested fixes.
---
Read audit/vulnerabilities.md.
List each finding and verify its affected component.
Inspect source and dependency information before suggesting changes.
Explain risk, compatibility, validation, and rollback.
Run approved tests and report their exact results.
Never expose secrets or modify remote systems without explicit approval.
Do not push branches or create pull requests until the user approves.
```

Skill discovery varies by IDE and extension. Check the installed coding assistant's Agent Skills support; if not supported, explicitly attach or reference this file in the chat. Do not confuse installing a skill with installing an MCP server.

## 7. Optional npm skill installer

Some skill catalogs provide a Node.js-based installer. If the catalog's **official instructions** specify the npm `skills` package, the commonly used command pattern is:

```powershell
npx skills add <approved-skill-repository>
```

Replace the placeholder with the approved source and review the installer and scripts before execution. Do **not** run this against unknown repositories, and do not assume a demonstration's command or package is authorized for your workstation. The installed skills may be stored in `.agents/skills/`, depending on tool and target agent.

## 8. Troubleshooting

| Symptom | What to check |
|---|---|
| `node` or `npm` not found | Approved installation, PATH, VS Code restart |
| `npx` fails | Proxy, registry, TLS certificates, package approval |
| JSON validation error | Commas, quotes, `servers` structure, transport fields |
| Server absent from list | Workspace file path, extension/version support, workspace trust |
| Server won't start | Command path, dependencies, output logs |
| HTTP 401/403 | Authentication, PAT scopes, expired token, server permissions |
| HTTP 404 | Wrong MCP endpoint path or transport |
| Network timeout | Corporate proxy, firewall, DNS, endpoint reachability |
| Tool unavailable | Server capabilities, user permissions, tool enabled in Agent mode |
| Skill not detected | Skill folder convention, YAML frontmatter, client support |

## 9. Security and version-control checks

- Never commit secrets, private endpoints, confidential reports, or internal repository names.
- Use a secret manager or the IDE's secure input mechanism; environment variables alone are not a secret vault.
- Restrict token scopes and approve remote write operations explicitly.
- Review every downloaded npm package and skill before executing it.
- Prefer a disposable repository and read-only tools for first tests.
- Verify that `.vscode/mcp.json` contains only non-sensitive values before committing it.

## 10. End-to-end smoke-test checklist

- [ ] Node.js/npm available **if approved and required**
- [ ] Workspace opened in VS Code
- [ ] Valid `.vscode/mcp.json` created
- [ ] Authorized server configured (not a placeholder)
- [ ] Server starts and exposes tools
- [ ] Read-only request succeeds
- [ ] Skill is discoverable or explicitly loaded
- [ ] No credentials or confidential values committed
- [ ] Human approval required for remote writes

**Next:** [Security remediation POC](./vulnerability-remediation-poc.md).
