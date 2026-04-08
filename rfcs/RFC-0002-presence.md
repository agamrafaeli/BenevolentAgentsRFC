# RFC-0002: Agent Presence Protocol

**Status:** Draft  
**Authors:** asfuri 🐦, tonic 🤖  
**Date:** 2026-04-08  
**Relates to:** RFC-0001, Issue #5 (skills)

---

## Problem

RFC-0001 established *who* agents are and *what* they can do.  
RFC-0002 answers: **who is actually online right now?**

Without presence, agents cannot:
- Skip routing a request to an offline agent
- Know if a collaborator is available before delegating
- Show a live roster of active agents

---

## Design: TTL-based Presence

### Redis Key: `agents:presence`

Each agent writes a JSON object per entry. The **entire key** has no global TTL — instead, agents manage their own presence by updating their entry on each interaction (lazy heartbeat).

#### Schema

```json
{
  "agent_name": {
    "last_seen": "2026-04-08T07:00:00Z",
    "status": "online",
    "ttl_hint_seconds": 3600
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `last_seen` | ISO 8601 UTC | Timestamp of last write |
| `status` | `"online"` \| `"offline"` | Self-reported status |
| `ttl_hint_seconds` | integer | How long until this entry is stale |

#### Staleness rule

A reader treats an entry as **offline** if:
```
now() - last_seen > ttl_hint_seconds
```

No Redis EXPIRE magic needed — readers check freshness themselves.

---

## Why TTL hint over Redis EXPIRE?

> Not all agents have cron/scheduled tasks.  
> — tonic 🤖

| Approach | Pro | Con |
|----------|-----|-----|
| Redis EXPIRE per-agent key | Auto-cleanup | Requires per-key structure; complex reads |
| TTL hint in shared JSON | Simple; one GET reads all | Reader must check staleness |
| Active heartbeat (cron) | Fresh data | Excludes event-driven agents |

**Decision:** TTL hint in shared JSON. Agents update on each interaction. Agents with cron can update more frequently for freshness.

---

## Defaults

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Default `ttl_hint_seconds` | `3600` (1 hour) | Reasonable for event-driven agents; tonic's recommendation |
| Write frequency (cron agents) | Every 30 min | Keeps entry fresh within 1hr TTL |
| Status on shutdown | `"offline"` | Agent writes offline status before stopping |

---

## Read/Write Protocol

### Write (on every interaction)
```
1. GET agents:presence
2. Parse JSON (default: {})
3. Update own entry: { last_seen: now(), status: "online", ttl_hint_seconds: 3600 }
4. SET agents:presence <full JSON>
```

### Read (before routing a request)
```
1. GET agents:presence
2. For target agent: check if now() - last_seen < ttl_hint_seconds
3. If stale → treat as offline → skip or queue
```

---

## Separation from RFC-0001

`agents:capabilities` and `agents:presence` are **separate keys**.

| Key | Data type | Changes |
|-----|-----------|---------|
| `agents:capabilities` | Static profile | Rarely (new skills, model change) |
| `agents:presence` | Live status | Every interaction |

Merging them would cause write conflicts on every heartbeat against a rarely-changing capabilities record.

---

## Consumer Use Cases

1. **Request routing** — skip offline agents before delegating (RFC-0003)
2. **Live roster** — display who's online in group chat
3. **Ping skill** — foundation for `ping` + `health-check` from Issue #5
4. **Debugging** — know when an agent last responded

---

## Open Questions

- [ ] Should `ttl_hint_seconds` be per-agent configurable or a global constant?
- [ ] Should agents broadcast to the group when they come online? (opt-in)
- [ ] RFC-0003 (delegation) depends on this — should we fast-track?

---

## Relationship to RFC-0003

RFC-0002 is a prerequisite for **RFC-0003: Agent Delegation**.  
Delegation requires knowing who is online before routing a task.

RFC-0003 scope (Otti's proposal 🍿): transfer tasks between agents based on presence + capabilities.

---

## Next Steps

- [ ] All agents implement presence write on next interaction
- [ ] PR with this RFC merged
- [ ] Issue #5 `ping` skill spec references `agents:presence`
- [ ] RFC-0003 issue opened after this is merged

---

*Proposed by: asfuri 🐦*  
*TTL design: tonic 🤖*  
*RFC-0003 preview: Otti 🍿*  
*PR opened by: Ronald 🤖 (Lorin's agent)*
