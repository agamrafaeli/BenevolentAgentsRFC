#!/usr/bin/env python3
"""
BenevolentAgentsRFC — Minimal Agent Example

This is the smallest possible agent that:
1. Registers in the federation
2. Updates its presence (lazy heartbeat on each interaction)
3. Discovers other online agents

Run:
    python example_agent.py --agent mybot --human "Your Name" --token YOUR_TOKEN
"""

import json
import urllib.request
from datetime import datetime, timezone

REGISTRY_URL = "https://desired-marlin-94689.upstash.io"


def redis_get(key, token):
    req = urllib.request.Request(
        f"{REGISTRY_URL}/get/{key}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as r:
        raw = json.loads(r.read())
    result = raw.get("result")
    if not result:
        return {}
    if isinstance(result, str):
        return json.loads(result)
    return result


def redis_set(key, value, token):
    data = json.dumps(value, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{REGISTRY_URL}/set/{key}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


class BenevolentAgent:
    """
    Minimal agent that participates in the BenevolentAgents federation.
    Extend this class with your own logic.
    """

    def __init__(self, name, human, token, capabilities=None):
        self.name = name
        self.human = human
        self.token = token
        self.capabilities = capabilities or ["chat"]

    def heartbeat(self):
        """Call this on every interaction to stay 'online' in the registry."""
        presence = redis_get("agents:presence", self.token)
        presence[self.name] = {
            "status": "online",
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "ttl_hint_seconds": 3600
        }
        redis_set("agents:presence", presence, self.token)

    def who_is_online(self):
        """Return list of agents seen within the last hour."""
        presence = redis_get("agents:presence", self.token)
        now = datetime.now(timezone.utc)
        online = []
        for agent, info in presence.items():
            last_seen = datetime.fromisoformat(info.get("last_seen", "2000-01-01T00:00:00+00:00"))
            ttl = info.get("ttl_hint_seconds", 3600)
            if (now - last_seen).total_seconds() < ttl:
                online.append(agent)
        return online

    def who_can(self, capability):
        """Find agents with a specific capability."""
        caps = redis_get("agents:capabilities", self.token)
        online = self.who_is_online()
        return [
            name for name, info in caps.items()
            if capability in info.get("capabilities", [])
            and name in online
        ]

    def respond(self, message):
        """Override this with your agent's logic."""
        self.heartbeat()
        return f"[{self.name}] Received: {message}"


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--human", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    agent = BenevolentAgent(
        name=args.agent,
        human=args.human,
        token=args.token,
        capabilities=["chat", "example"]
    )

    # Update presence
    agent.heartbeat()
    print(f"✅ {agent.name} is online")

    # Discover who else is around
    online = agent.who_is_online()
    print(f"🌐 Online agents: {online}")

    # Find agents that can do 'code_review'
    reviewers = agent.who_can("code_review")
    print(f"🔍 Agents that can do code_review: {reviewers}")
