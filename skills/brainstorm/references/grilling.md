# Grilling core (vendored from Matt `grilling`)

No runtime `Read ~/.claude/skills/grilling`.

## Design tree

Map the work as a **tree**: each settled decision unlocks the decisions that hang off it.

**Frontier** = every decision whose prerequisites are already settled — ask those **now**, without guessing unsettled answers.

## Rounds

1. List the current frontier (numbered).
2. Each item: question + **your recommended answer**.
3. Wait for the user.
4. Recompute frontier; next round.
5. Done when frontier is empty — nothing silently assumed.

A question that depends on another still-open answer belongs to a **later** round.

## Question format

```text
❓ **Q1** - **<title>**: <body; prefer multiple choice>

➡️ <recommended answer>
```

Ask the **whole frontier** in one round (several Qs OK). Do not drip one Q when three independent ones are ready — that is slower than clarify’s grilling.

## Facts vs decisions

- **Facts** (repo, docs, APIs, existing code): agent looks up — never ask the user what you can find.
- **Decisions** (direction, scope, trade-offs): put to the user; wait.

Optional: dispatch exploration in parallel for facts; only frontier questions downstream of that fact wait.

## Exit

Shared understanding confirmed by user → present approaches / design (see parent skill). Do not implement from grilling alone.
