# VS Code setup — DWS AI Library skills and MCP

> **Security first:** The session's guidance favored IDE-integrated GitHub Copilot for day-to-day work. Gemini CLI and GitHub Copilot CLI are **not recommended on corporate laptops**. If a CLI is required, request the approved Coder environment. Do not infer that an npm skill installer or other CLI is approved merely because it was demonstrated.

## Prerequisites
- Corporate-approved VS Code and GitHub Copilot extension, signed in with your authorized account.
- Access to the DWS AI Library repository and relevant enterprise MCP endpoints.
- Permission to access Jira, Confluence and the target Bitbucket/GitHub repositories.
- Approved personal access tokens (PATs), with minimum necessary scopes.
- A disposable demo repository; do not begin with production data.

## 1. Install the relevant skills
In the session, an AI Library skill installer listed 21 skills and allowed selecting:
- `atlassian-mcp`
- `dws-saga-analysis`
- `github-mcp`

Choose **Project** scope and GitHub Copilot as the agent target. The observed layout was:

```text
my-mcp-project/
  .agents/
    skills/
      atlassian-mcp/
      dws-saga-analysis/
      github-mcp/
```

**Important:** The precise installer command and approved internal repository URL were not reliably captured in the transcript. Copy them from the official AI Library documentation or recording; do not substitute an unverified public package.

## 2. Register MCP servers in VS Code
1. Inspect the installed skill's MCP template, shown in the session under `.agents/skills/.../assets/mcp.json`.
2. Open Copilot Chat in **Agent** mode and ask: *Configure the approved MCP servers from the installed DWS skill assets for this VS Code workspace. Show the changes before applying them.*
3. Review the generated `.vscode/mcp.json` against official enterprise endpoints and approved headers.
4. Open the VS Code command palette and choose **MCP: Browse MCP Servers**.
5. The session showed registrations for Atlassian, Bitbucket, Bitbucket Dev, Confluence, GitHub, GitHub Internal and Jira.
6. Start only the needed servers; verify connection and tool availability.

**Registration does not prove authentication.** Avoid copying example endpoint URLs or token values from screenshots.

## 3. Set up credentials safely
The presenter confirmed PATs are provided through local environment variables rather than embedded in repository files. The exact variable names depend on the official MCP template.

Example *pattern* for a PowerShell process (replace the name with the actual approved name):

```powershell
$env:JIRA_PAT = "<token-entered-securely>"
code .
```

The command above is illustrative only; entering secrets into shell history can expose them. Prefer your enterprise-approved secret manager or credential injection method. Never put real PATs in `mcp.json`, source control, screenshots, Copilot prompts, or logs. An environment variable is not itself a secure secret store.

## 4. Smoke tests (read-only)
Ask Copilot one question at a time:
1. *Which Jira tools are available through the approved MCP server?*
2. *List my assigned Jira issues for project [PROJECT], with issue keys and links.*
3. *Find the Confluence page about [TOPIC], show the source link and summarize it.*
4. *List branches or recent commits for repository [REPO] on the supported Bitbucket instance.*

Confirm results against the source applications. Do not enable write operations until permissions and audit controls are reviewed.

## 5. Troubleshooting
- **No servers listed:** Verify the workspace `.vscode/mcp.json` exists, is valid and matches the installed VS Code MCP schema.
- **Unauthorized:** Check PAT scopes, expiration, variable name and whether VS Code inherited the environment.
- **Server registered but unavailable:** Check enterprise proxy, TLS, endpoint accessibility and client logs; escalate to the platform team.
- **Bitbucket Data Center 1:** Not supported by the demonstrated integration; use approved Git/REST workflows or request platform guidance.
- **CLI restriction:** Do not install a prohibited local CLI as a workaround; request Coder access.
- **IntelliJ:** The session demonstrated VS Code, not verified IntelliJ compatibility.

## 6. Optional Python fallback
The session showed an Atlassian skill dependency installation pattern:

```powershell
python -m pip install -r .agents\skills\atlassian-mcp\scripts\requirements.txt
```

Use only in an approved Python environment, after reviewing the skill and dependencies. The Python fallback is not necessary if direct MCP works and is approved.

## Completion checklist
- [ ] DWS skill source and instructions reviewed
- [ ] IDE/client approved by enterprise policy
- [ ] MCP endpoints verified against official documentation
- [ ] Credentials supplied securely with least privilege
- [ ] Read-only Jira, Confluence and repository queries succeed
- [ ] Write operations gated by explicit approval
