# AI Agent and MCP Engineering Guide

## Overview
Model Context Protocol (MCP) is a standardized way for AI coding assistants to discover and invoke tools. Agent skills define repeatable engineering workflows; MCP connectors provide access to approved systems; local scripts perform deterministic tasks.

This guide summarizes general technical concepts and a sample development workflow. It deliberately excludes organization-specific names, internal infrastructure, endpoints, repository identifiers, credentials, and meeting details.

## Core concepts
| Component | Purpose |
|---|---|
| AI coding assistant | Interprets requests and coordinates work |
| Agent skill | Reusable instructions for an engineering task |
| MCP client | Discovers and invokes exposed tools |
| MCP server | Provides tool operations for an external service |
| REST API | Alternative direct integration mechanism |
| Local scripts | Run tests, parse reports, and validate changes |

## Typical capabilities
With approved access, MCP tools may support searching issue trackers, reading knowledge-base pages, inspecting source repositories, reviewing commits, and preparing pull requests. Capabilities depend on the specific server and the user's permissions.

## Practical applications
- Summarize assigned issues and retrieve relevant documentation.
- Investigate production incidents by correlating issue details and source changes.
- Review pull requests against engineering standards.
- Analyze security findings, propose minimal fixes, and validate them.
- Generate release notes from approved issue and commit data.

## Security
- Use only approved tools, extensions, and execution environments.
- Prefer least-privilege credentials and enterprise-approved secret management.
- Never commit access tokens, internal URLs, proprietary documentation, or sensitive reports.
- Inspect agent skills and tool permissions before execution.
- Require human approval for writes, pushes, pull requests, and destructive operations.
- Do not assume a local AI-generated security report replaces official compliance scanning.

## Architecture
`IDE coding assistant → project skill → approved MCP tools / scripts → tests → human review → pull request`

MCP and direct REST API integration are both viable. Choose based on supported functionality, maintenance, security, and reliability.

## Guides
- [VS Code setup](./vscode-setup.md)
- [Security remediation proof of concept](./vulnerability-remediation-poc.md)

## Scope
These are generic implementation notes, not a statement of any organization's current policy, tool availability, or approvals.
