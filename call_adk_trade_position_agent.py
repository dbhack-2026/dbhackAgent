#!/usr/bin/env python3
"""
Client script to call the ADK Trade Position Agent using POST /prompt.

Usage:
  python call_adk_trade_position_agent.py --agent-url https://YOUR-AGENT-SERVICE.run.app --prompt "Show trades for account A100"

For a private Cloud Run agent:
  python call_adk_trade_position_agent.py --agent-url https://YOUR-AGENT-SERVICE.run.app --prompt "Show positions for account A100" --identity-token "$(gcloud auth print-identity-token)"
"""

import argparse
import json
import sys
from typing import Any

import requests


def call_agent(
    agent_url: str,
    prompt: str,
    user_id: str = "local-user",
    session_id: str | None = None,
    identity_token: str | None = None,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    url = f"{agent_url.rstrip('/')}/prompt"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if identity_token:
        headers["Authorization"] = f"Bearer {identity_token}"

    payload: dict[str, Any] = {
        "prompt": prompt,
        "user_id": user_id,
    }

    if session_id:
        payload["session_id"] = session_id

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=timeout_seconds,
    )

    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Call the ADK Trade Position Agent using POST /prompt."
    )
    parser.add_argument("--agent-url", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--user-id", default="local-user")
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--identity-token", default=None)
    parser.add_argument("--timeout", type=int, default=300)

    args = parser.parse_args()

    try:
        result = call_agent(
            agent_url=args.agent_url,
            prompt=args.prompt,
            user_id=args.user_id,
            session_id=args.session_id,
            identity_token=args.identity_token,
            timeout_seconds=args.timeout,
        )
        print(json.dumps(result, indent=2))
        return 0
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        if exc.response is not None:
            print(exc.response.text, file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
