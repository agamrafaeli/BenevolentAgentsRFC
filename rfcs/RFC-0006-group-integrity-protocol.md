# RFC-0006: Group Integrity Protocol

**Status:** DRAFT
**Authors:** Asfuri (drafted), Klumit/Ronald (submitted)
**Date:** 2026-04-09
**Related:** RFC-0003 (Agent Identity), RFC-0005 (Member Onboarding)

---

## Summary

A protocol for identifying and handling unauthorized actors in a BenevolentAgents collaborative context.

## Motivation

On April 9, 2026, an unverified actor (Mary, +447570867562) entered a trusted group channel and sent unsolicited content (crypto/investment spam). Without a defined protocol, each agent responded ad-hoc, and no consistent policy existed for how to handle the situation.

This RFC establishes a clear, repeatable process for group integrity enforcement. It is the complement to RFC-0005: while RFC-0005 governs how members *join*, this RFC governs how *unauthorized actors* are handled.

## Core Principle

> **Unverified actors get silence, not engagement. Humans decide exceptions.**

## Key Definitions

**Unauthorized actor** — Any sender not present in the team Roster who has not completed onboarding (RFC-0005).

**Threat signal** — A message from an unverified sender that includes an external call-to-action, link, or solicitation.

**Hold** — Agent state in which no engagement, acknowledgment, or onboarding is offered to the actor.

## Protocol

### Step 0 — Context Check
Is the sender in the team Roster?
- Yes → normal interaction
- No → sender is **unverified by default**

All messages from unverified senders are treated as potential threats regardless of content.

### Step 1 — Flag
Any unverified message containing an external call-to-action, link, or solicitation is flagged as a **potential threat**.

Flagging is internal — not communicated back to the actor.

### Step 2 — Hold
No agent engages with the flagged sender. This includes:
- No onboarding offer
- No response to the message
- No acknowledgment of receipt
- No group discussion about the threat in the same channel

### Step 3 — Report
Alert is sent to the **human admin only** (not broadcast to the group). Report includes:
- Sender identity
- Message content summary
- Flag reason

### Step 4 — Override (Human Only)
A human admin may explicitly authorize onboarding after a threat flag. Without explicit override:
- Hold remains in effect indefinitely
- No agent may independently engage with the flagged actor

Override must be logged with reason and admin identity.

## What is NOT a Threat

Not every message from an unverified sender is a threat. An unverified sender who introduces themselves and asks about the group context should be assessed under RFC-0005 (onboarding), not this protocol.

Differentiation rule:
- **Self-introduction + curiosity** → potential onboarding candidate (RFC-0005)
- **Call-to-action + external link + no self-introduction** → threat signal (this RFC)

## Relationship to RFC-0005

RFC-0005 and RFC-0006 are two sides of the same door:
- RFC-0005 = how authorized members enter
- RFC-0006 = how unauthorized actors are kept out (or assessed)

A failed RFC-0005 onboarding does not automatically trigger RFC-0006. Agents must evaluate intent.

## Non-Goals

- Member onboarding → see **RFC-0005**
- Technical spam filtering or automated moderation tooling
- Legal or compliance enforcement

---

*This RFC was drafted collaboratively during the April 9, 2026 session in "Showing Off Your Agents", following the live case study of an unauthorized actor. Draft by Asfuri; protocol framework by Tonic, Asfuri, and Agammemnon.*
