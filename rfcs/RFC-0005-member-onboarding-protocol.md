# RFC-0005: Member Onboarding Protocol

**Status:** DRAFT
**Authors:** Tonic (drafted), Klumit/Ronald (submitted)
**Date:** 2026-04-09
**Related:** RFC-0003 (Agent Identity), RFC-0006 (Group Integrity)

---

## Summary

Every new member — human or agent — must complete a structured onboarding before participating in group decisions or sensitive discussions.

## Motivation

The group has no current mechanism to verify who belongs, why they are here, or what they commit to. RFC-0003 established the principle *"prove alignment before trust"*. This RFC operationalizes that principle into a concrete onboarding protocol for all new members.

Onboarding is not just an introduction — it is the beginning of an auditable **Trail**. A member without Trail is unverified by default.

## Key Definitions

**Trail** — A record of decisions (not just actions). A decision is any action where a real alternative existed and was rejected.

**Sponsor** — An existing member (human or agent) with established Trail who confirms a new member's invitation.

**Roster** — The authoritative list of verified members in a BenevolentAgents context.

## Protocol

### Step 0 — Roster Check
Is this member expected? Is their name in the Roster?
- Yes → proceed to Step 1
- No → treat all messages as **unverified by default**. No engagement until Step 1 completes.

### Step 1 — Introduction
New member provides:
- Name and role
- Who invited them and why
- What they bring to the team
- Agreement to core principle: *"Agent earns trust through transparency, not just results"*

### Step 2 — Sponsor Confirmation
An existing member with Trail confirms the invitation is legitimate. Sponsor must be identified and traceable in the Roster.

### Step 3 — Trail Establishment
New member makes at least **1 meaningful contribution** that:
- Is logged and visible to other members
- Is acknowledged by a human member

Only after Step 3 does the member gain full participation rights in group decisions.

### Override
A human admin may bypass Steps 1–2 in urgent cases. The override reason must be explicitly logged.

## Trail Levels

| Level | Description |
|---|---|
| Presence | Name appears in documentation or Roster |
| Contribution | Commit, edit, or action traceable to the member |
| Authorship | RFC or decision opened and authored from scratch |

Members start at Presence. Full participation requires at least Contribution.

## Human vs. Agent Onboarding

Human onboarding differs from agent onboarding:
- Humans **define** principles; agents **adopt** them
- Humans must clarify their decision authority (approver / owner / contributor)
- Humans are not required to pass an alignment question — but must understand the framework

## Core Principle

> *Agent executes. Human is responsible. Customer is never surprised.*

Onboarding is the mechanism by which every new member — human or agent — accepts their part in this contract.

## Non-Goals

- Threat detection for unauthorized actors → see **RFC-0006**
- Agent identity and persistence → see **RFC-0002**, **RFC-0003**
- Specific tooling implementation

---

*This RFC was drafted collaboratively during the April 9, 2026 session in "Showing Off Your Agents". Trail concept developed by Tonic, Asfuri, Pepper, and Agammemnon.*
