# DWS MCP Fundamentals — meeting takeaways and implementation guide

**Session:** 30 October 2026 | **Presenter:** Matthias Roth | **Source:** User-provided meeting transcript and screenshots.  
**Audience:** Java/Spring Boot engineering teams using GitHub Copilot, Jira, Confluence, Bitbucket and SAGA.

## Executive summary
MCP (Model Context Protocol) lets coding agents discover and invoke tools exposed by enterprise systems. DWS's AI Library provides reusable skills and MCP configuration for Atlassian and GitHub. The session demonstrated installation into an empty project, registering MCP servers in VS Code, querying Jira and Confluence, inspecting GitHub, cloning a Bitbucket repository, and running a local DWS SAGA analysis skill.

**Key caveats:** DWS Bitbucket MCP was demonstrated for Data Center 2, **not Data Center 1**. The SAGA skill's local output is **not** automatically uploaded to Jira and was not established as a replacement for central compliance scanning. Local Gemini/Copilot CLI tools are **not recommended on corporate laptops**; request the approved Coder environment for CLI use. IDE-integrated Copilot is the recommended day-to-day route.

## Confirmed findings
| Area | Observed in session | Qualification |
|---|---|---|
| AI Library | Skills installer discovered 21 skills; installed `atlassian-mcp`, `dws-saga-analysis`, `github-mcp` | Review skill instructions before running |
| Install scope | Project or global | Project scope is best for version-controlled demos |
| Project structure | `.agents/skills/<skill-name>/` | Paths may vary by client/installer version |
| VS Code | Copilot generated `.vscode/mcp.json`; Browse MCP Servers showed seven registrations | Registration is distinct from authentication and successful invocation |
| MCP endpoints | Atlassian, Jira, Confluence, Bitbucket, Bitbucket Dev, GitHub, GitHub Internal | Permissions and available tools differ |
| Authentication | Personal access tokens referenced through environment variables | Tokens act with user's permissions; do not commit or print |
| Jira | Queried assigned tickets in a project | Requires access |
| Confluence | Searched and summarized architecture pages | Review selected source page |
| Bitbucket | Cloned repository and checked out `develop` | DC2 supported; DC1 unsupported in demonstration |
| SAGA | Local analysis produced findings, risk summary and remediation suggestions | Token cost; not a central compliance report |
| Cross-system | Presenter reported no encountered limitation combining Jira/Confluence/Bitbucket | Not a guarantee of all workflow or access combinations |
| Hosting | Presenter described centrally provided enterprise MCP services | Exact hosting may vary by endpoint |
| Custom servers | Spring Boot templates and Apigee mentioned as avenues | No finalized DWS boilerplate confirmed |

## Day-to-day applications
- **Ticket triage:** Ask Copilot to find assigned Jira issues, read linked Confluence architecture and summarize relevant code.
- **Code review:** Use approved GitHub/Bitbucket tools to inspect commits, branches and PRs; request a review summary.
- **Pre-scan security:** Run `dws-saga-analysis` locally on a test repository, prioritize findings and fix dependencies or code before central scans.
- **Incident investigation:** Correlate Jira symptoms, Confluence runbooks and relevant repository files, checking all retrieved facts.
- **Vulnerability remediation:** Use a dedicated skill to parse `audit/vulnerabilities.md`, propose one change per finding, run Gradle tests, and prepare a human-reviewed PR.

## Recommended architecture
`Copilot in VS Code → project-level Agent Skill → approved MCP tools (Jira/Confluence/Bitbucket/GitHub) + local Gradle/scripts → review → PR`

Use MCP for discovery and remote integrations, skills for reusable workflow instructions, and deterministic scripts for parsing and validation. Direct REST APIs remain a viable fallback; MCP is not inherently required for every action.

## Action items
1. Confirm whether your target Bitbucket repository is on Data Center 2.
2. Obtain the DWS AI Library URL and the approved VS Code MCP setup guidance from the presentation/SharePoint recording.
3. Follow [VS Code setup](./vscode-setup.md), beginning with read-only tools.
4. Follow [remediation proof of concept](./vulnerability-remediation-poc.md).
5. Verify IntelliJ support, ADAP/Jenkins noninteractive access, SAGA compliance acceptance and Data Center 1 roadmap with platform owners.

**Evidence status:** These are notes from the supplied session, not a current enterprise policy document. Follow the latest DWS security and platform documentation if it differs.
