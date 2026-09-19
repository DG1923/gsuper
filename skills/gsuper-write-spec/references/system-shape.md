# System shape (only `specs/system/`)

Not a feature SRS. Not layers. Reader sees **the product in the world**.

```markdown
# <Name> — System

**Kind:** system
**Status:** Draft | Approved
**Id:** …

## Job
What the whole product is for (one paragraph). Weakness if this file only lists stacks.

## Actors
| Actor | Wants |
|-------|--------|
| … | … |

## Context
C4 context. Mermaid fence. Externals (YouTube, GTX, LLM provider).

```mermaid
flowchart LR
  user[User] --> app[This product]
  app --> ext[External]
```

## Apps
| App | Runs | Live job |
|-----|------|----------|
| … | … | … |

## Surfaces
| Surface | live / đích | Spec |
|---------|-------------|------|
| … | … | feature/… |

## Load and safety
Numbers or TBD: concurrent, total, p95, security.

## Doc chain
system → architecture → algorithm → feature → plan

## Reflection
```

**Fail if:** same headings as feature (shall table, parent children); or only “FastAPI + Vite”.
