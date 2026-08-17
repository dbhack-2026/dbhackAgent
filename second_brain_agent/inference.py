from __future__ import annotations

import base64
import json
import os
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


DEFAULT_MODELS_URL = "https://models.github.ai/inference/chat/completions"


class InferenceConfigError(RuntimeError):
    """Raised when required model connection settings are missing."""


class InferenceError(RuntimeError):
    """Raised when the model endpoint returns an error or malformed response."""


@dataclass(frozen=True)
class InferenceConfig:
    """Configuration for the GitHub Models compatible chat-completions endpoint.

    All secrets are read from environment variables. Nothing is persisted by
    this package.
    """

    model_id: str
    token: str
    models_url: str = DEFAULT_MODELS_URL
    proxy_host: str | None = None
    proxy_port: int | None = None
    proxy_username: str | None = None
    proxy_password: str | None = None
    timeout_seconds: float = 120.0

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "InferenceConfig":
        values = os.environ if env is None else env

        model_id = values.get("SECOND_BRAIN_MODEL", "").strip()
        token = values.get("SECOND_BRAIN_INFERENCE_TOKEN", "").strip()
        models_url = values.get("SECOND_BRAIN_MODELS_URL", DEFAULT_MODELS_URL).strip()

        if not model_id:
            raise InferenceConfigError("SECOND_BRAIN_MODEL is required")
        if not token:
            raise InferenceConfigError("SECOND_BRAIN_INFERENCE_TOKEN is required")
        if not models_url:
            raise InferenceConfigError("SECOND_BRAIN_MODELS_URL cannot be empty")

        proxy_host = values.get("SECOND_BRAIN_PROXY_HOST", "").strip() or None
        proxy_port_text = values.get("SECOND_BRAIN_PROXY_PORT", "").strip()
        proxy_port = int(proxy_port_text) if proxy_port_text else None
        proxy_username = values.get("SECOND_BRAIN_PROXY_USERNAME", "").strip() or None
        proxy_password = values.get("SECOND_BRAIN_PROXY_PASSWORD", "") or None
        timeout_text = values.get("SECOND_BRAIN_TIMEOUT_SECONDS", "120").strip()

        if proxy_host and proxy_port is None:
            raise InferenceConfigError(
                "SECOND_BRAIN_PROXY_PORT is required when SECOND_BRAIN_PROXY_HOST is set"
            )
        if proxy_port is not None and not proxy_host:
            raise InferenceConfigError(
                "SECOND_BRAIN_PROXY_HOST is required when SECOND_BRAIN_PROXY_PORT is set"
            )
        if bool(proxy_username) != bool(proxy_password):
            raise InferenceConfigError(
                "SECOND_BRAIN_PROXY_USERNAME and SECOND_BRAIN_PROXY_PASSWORD must be supplied together"
            )

        return cls(
            model_id=model_id,
            token=token,
            models_url=models_url,
            proxy_host=proxy_host,
            proxy_port=proxy_port,
            proxy_username=proxy_username,
            proxy_password=proxy_password,
            timeout_seconds=float(timeout_text),
        )

    @property
    def proxy_url(self) -> str | None:
        if not self.proxy_host or self.proxy_port is None:
            return None
        return f"http://{self.proxy_host}:{self.proxy_port}"


@dataclass(frozen=True)
class InferenceResult:
    text: str
    total_tokens: int | None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class GitHubModelsClient:
    """Small standard-library client matching the working Java utility pattern.

    Strategy:
      * POST JSON to the configured chat-completions URL.
      * Send `Authorization: Bearer <token>`.
      * Send `{model, messages}` as the request body.
      * Optionally route HTTPS through an authenticated HTTP corporate proxy.
      * Parse `choices[0].message.content` and `usage` from the JSON response.
    """

    def __init__(self, config: InferenceConfig):
        self.config = config
        self._opener = self._build_opener(config)

    @staticmethod
    def _build_opener(config: InferenceConfig) -> urllib.request.OpenerDirector:
        handlers: list[Any] = []

        proxy_url = config.proxy_url
        if proxy_url:
            handlers.append(
                urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
            )
            if config.proxy_username and config.proxy_password:
                password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                password_manager.add_password(
                    None,
                    proxy_url,
                    config.proxy_username,
                    config.proxy_password,
                )
                handlers.append(urllib.request.ProxyBasicAuthHandler(password_manager))

        # Keep certificate verification enabled. This uses the machine/JVM-equivalent
        # trusted CA configuration exposed to Python; do not disable TLS verification.
        handlers.append(urllib.request.HTTPSHandler(context=ssl.create_default_context()))
        return urllib.request.build_opener(*handlers)

    def complete(self, messages: Sequence[Mapping[str, str]]) -> InferenceResult:
        payload = {
            "model": self.config.model_id,
            "messages": [dict(message) for message in messages],
        }
        body = json.dumps(payload).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "SecondBrainAgent/1.0",
        }

        # Some enterprise proxies require pre-emptive proxy basic auth instead of
        # a 407 challenge. Adding the header preserves the same explicit proxy-auth
        # behavior as the working OkHttp utility while ProxyBasicAuthHandler remains
        # available for challenge/response flows.
        if self.config.proxy_username and self.config.proxy_password:
            raw = f"{self.config.proxy_username}:{self.config.proxy_password}".encode("utf-8")
            headers["Proxy-Authorization"] = "Basic " + base64.b64encode(raw).decode("ascii")

        request = urllib.request.Request(
            self.config.models_url,
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            with self._opener.open(request, timeout=self.config.timeout_seconds) as response:
                response_body = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            safe_body = error_body[:1000]
            raise InferenceError(
                f"Inference endpoint returned HTTP {exc.code}: {safe_body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise InferenceError(f"Inference request failed: {exc.reason}") from exc

        try:
            root = json.loads(response_body)
            choices = root.get("choices") or []
            if not choices:
                raise InferenceError("Inference response contained no choices")
            message = choices[0].get("message") or {}
            text = message.get("content")
            if not isinstance(text, str):
                raise InferenceError("Inference response did not contain message.content")

            usage = root.get("usage") or {}
            return InferenceResult(
                text=text,
                total_tokens=_optional_int(usage.get("total_tokens")),
                prompt_tokens=_optional_int(usage.get("prompt_tokens")),
                completion_tokens=_optional_int(usage.get("completion_tokens")),
            )
        except json.JSONDecodeError as exc:
            raise InferenceError("Inference endpoint returned invalid JSON") from exc


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None
