# VS Code — Agent Skills and MCP Setup

This guide is vendor-neutral and does not contain private endpoints or internal installation commands.

## Prerequisites
Use an approved version of VS Code, a supported AI coding assistant extension, and an account authorized for the relevant external services. Confirm any command-line tool is allowed in your environment before installing it.

## Step 1: Create a demo project
```text
demo-project/
  .agents/
    skills/
      security-remediation/
        SKILL.md
  audit/
    vulnerabilities.md
  .vscode/
    mcp.json
```

## Step 2: Add a reviewed skill
Create a `SKILL.md` that describes the task, allowed tools, validation steps, and actions requiring approval. Use the format supported by your assistant; skill discovery varies by client and version.

## Step 3: Configure approved MCP servers
Obtain the server configuration from the provider's official documentation. In VS Code, use the command palette's MCP configuration commands, where supported, or edit the workspace MCP configuration according to the installed extension's documented schema.

Do not paste internal endpoint URLs or secrets into a public repository. A server being listed in the IDE does not mean it is connected or authenticated.

## Step 4: Authenticate safely
Use an approved credential manager or secret-injection mechanism. If environment variables are required, follow your organization's guidance. Avoid exposing secrets in shell history, files, logs, screenshots, or prompts. Use minimum necessary scopes.

## Step 5: Test read-only capabilities
Ask your assistant to:
1. List available tools.
2. Search a permitted sample issue.
3. Read a non-sensitive documentation page.
4. Retrieve repository metadata from a test repository.

Verify the answers against the original systems before enabling write operations.

## Step 6: Validate a safe workflow
Have the assistant inspect a test repository, propose a change, and run local tests. Review the diff before approving any remote action.

## Troubleshooting
- **No servers listed:** Check the MCP configuration location and schema.
- **Authentication failure:** Verify approved credentials, scopes, expiry, and process environment.
- **Connection failure:** Check TLS, proxy, network access, and server availability.
- **Tools missing:** Check server capability declarations and client support.
- **CLI blocked:** Use the approved IDE workflow or request an authorized isolated environment.

## Completion checklist
- [ ] Approved software and MCP endpoints
- [ ] Reviewed skill instructions
- [ ] Credentials secured and least-privileged
- [ ] Read-only smoke tests successful
- [ ] Write operations require approval
