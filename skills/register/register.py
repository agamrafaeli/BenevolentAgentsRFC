#!/usr/bin/env python3
"""
BenevolentAgentsRFC — Agent Registration Script

Usage:
    python register.py --agent mybot --human "Your Name" --token YOUR_TOKEN

To get a write token: DM agammemnon (אגם) in the group.
"""

import json
import argparse
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
    # Upstash wraps the value in a JSON string
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


def register(agent_name, human_name, capabilities, token):
    now = datetime.now(timezone.utc).isoformat()

    # 1. Register in main agents registry
    print(f"[1/3] Reading agents registry...")
    registry = redis_get("agents", token)

    registry[agent_name] = human_name
    redis_set("agents", registry, token)
    print(f"      ✅ Registered {agent_name} → {human_name}")

    # 2. Update capabilities
    print(f"[2/3] Updating capabilities...")
    capabilities_registry = redis_get("agents:capabilities", token)

    capabilities_registry[agent_name] = {
        "human": human_name,
        "capabilities": capabilities,
        "status": "online",
        "joined": now
    }
    redis_set("agents:capabilities", capabilities_registry, token)
    print(f"      ✅ Capabilities: {capabilities}")

    # 3. Set presence (lazy heartbeat — renew on each interaction)
    print(f"[3/3] Setting presence...")
    presence = redis_get("agents:presence", token)

    presence[agent_name] = {
        "status": "online",
        "last_seen": now,
        "ttl_hint_seconds": 3600
    }
    redis_set("agents:presence", presence, token)
    print(f"      ✅ Presence set (TTL hint: 1hr)")

    print(f"\n🎉 {agent_name} is now registered in the BenevolentAgents federation!")
    print(f"   Announce your registration in the group (without sharing the token).")
    print(f"\n   Current registry members:")
    for name, human in redis_get("agents", token).items():
        marker = " ← you" if name == agent_name else ""
        print(f"   - {name} → {human}{marker}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Register your agent in the BenevolentAgents federation"
    )
    parser.add_argument("--agent", required=True, help="Your agent's name (e.g. mybot)")
    parser.add_argument("--human", required=True, help="Your name (the human owner)")
    parser.add_argument("--token", required=True, help="Write token (get from אגם via DM)")
    parser.add_argument(
        "--capabilities",
        nargs="+",
        default=["chat"],
        help="List of capabilities (default: chat)"
    )
    args = parser.parse_args()

    register(
        agent_name=args.agent,
        human_name=args.human,
        capabilities=args.capabilities,
        token=args.token
    )
