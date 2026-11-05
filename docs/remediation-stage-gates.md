# Local remediation stage gates

This is an incremental extension to the demo Skill, not a replacement for the advanced corporate-local Skill shown in the screenshots.

## Implemented
- Parse issue sections from a local Markdown report.
- Preserve finding IDs and source evidence hashes.
- Consolidate identical IDs and flag conflicting duplicate descriptions.
- Initialize and resume a local JSON state file.
- Enforce ordered stage transitions, evidence requirements, and explicit approval flags.
- Unit tests for ingestion and transition gates.

## Run from repository root

```powershell
python scripts/remediation_pipeline.py --input audit/vulnerabilities.md
python -m unittest discover -s tests -v
```

State is stored under the git-ignored .agent-state directory. The controller does not run external commands, modify Java code, call Jira, or create pull requests.

## Remaining integrations

Use the existing corporate-local Jira collector, repo context scripts, Copilot Agent code remediation, Gradle validation, human review, Bitbucket PR helper and CI system. Those integrations require inspection of the actual local files and cannot be verified from this GitHub demo.

The state file is not an authentication or approval mechanism. Never use a JSON approval flag as a substitute for verified human approval. Cross-validation must inspect the code and original finding; merely recording PASSED is insufficient.

The OPUS scan and CI/deployment stages remain external. Never claim they ran based on this demo.
