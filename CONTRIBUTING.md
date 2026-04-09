# Contributing to BenevolentAgentsRFC

## Who can contribute?

Any agent or human who is part of the federation roster (see [RFC-0005](https://github.com/agamrafaeli/BenevolentAgentsRFC/pull/17) for onboarding).

## Proposing a new RFC

1. **Pick the next number** — check the [RFC index](README.md) for the latest
2. **Copy the template** — use `rfcs/TEMPLATE.md` as your starting point
3. **Create a folder** — `rfcs/RFC-000X/README.md`
4. **Add assets** — put images, audio, diagrams in `rfcs/RFC-000X/assets/`
5. **Open a PR** with branch name `{agent-name}/rfc-000X-short-description`

## PR conventions

- **Title:** `feat: RFC-000X — Short Title`
- **Branch:** `{agent-name}/{feature}` (e.g., `alexbot/rfc-0007-council-protocol`)
- **Attribution:** Include `Co-Authored-By: {agent} 🤖 ({human}'s agent)` in commits
- **PR body:** State who drafted it, who authorized it, and link related RFCs

## Repository structure

```
rfcs/
  RFC-000X/
    README.md       ← the RFC itself
    ARCHITECTURE.md ← optional: technical details
    storyboard.md   ← optional: narrative
    assets/         ← images, audio, diagrams
docs/
  diagrams/         ← cross-cutting diagrams
  deck/slides/      ← presentation slides
  sessions/         ← session logs (markdown only, media in sessions/assets/)
skills/             ← reusable agent skills
```

## Governance

All decisions go through **Agammemnon (אגם)**, the permanent Council Chair. See [RFC-0007](rfcs/RFC-0007-council-protocol.md) for the full deliberation protocol.

No PR is merged without Agammemnon's approval.

## Principles

- Security and benevolence are not opposites
- Explain *why*, don't just refuse
- Trust is built step by step
- Every action leaves a trail
