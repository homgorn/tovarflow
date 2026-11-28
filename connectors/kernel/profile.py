"""Capability profile loader: channels are data, not code branches."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CapabilityProfile:
    id: str
    layer: str
    role: str
    auth: dict
    api: dict
    capabilities: dict
    endpoints: dict
    limits: dict
    requirements: dict
    content: dict
    maturity: str

    def supports(self, name: str) -> bool:
        return bool(self.capabilities.get(name))


def load(path: str | Path) -> CapabilityProfile:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return CapabilityProfile(
        id=data["id"], layer=data["layer"], role=data["role"], auth=data["auth"],
        api=data["api"], capabilities=data["capabilities"],
        endpoints=data.get("endpoints", {}), limits=data["limits"],
        requirements=data["requirements"], content=data["content"],
        maturity=data.get("maturity", "research"),
    )
