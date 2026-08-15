# Research: Python OOP core (not SOLID slogans)

**Date:** 2026-08-15  
**Purpose:** Find what actually governs how to write objects in Python, so a gsuper rule can be as sharp as Ponytail’s 7-rung ladder.  
**Status:** Findings only — rule text not finalized.

## Question

What is the *core* of OOP in Python (so SOLID does not stay generic Java-in-Python)?

## Sources (primary / first-party / named practitioner)

| Claim area | Source |
|------------|--------|
| Structural vs nominal typing | [PEP 544 – Protocols](https://peps.python.org/pep-0544/) |
| Data-holding classes | [PEP 557 – Data Classes](https://peps.python.org/pep-0557/) |
| ABCs / nominal interfaces | [PEP 3119](https://peps.python.org/pep-3119/) / [`abc` docs](https://docs.python.org/3/library/abc.html) |
| Class overuse | Jack Diederich, *Stop Writing Classes*, PyCon US 2012 ([abstract](https://us.pycon.org/2012/schedule/presentation/352/)) |
| When to subclass in Python | Hynek Schlawack, [Subclassing in Python Redux](https://hynek.me/articles/python-subclassing-redux/) |
| SOLID in dynamic Python | Hynek, [Solid Snakes](https://hynek.me/talks/reliability/) — not all SOLID letters are equally relevant |

## Finding 1 — Python’s default is not “everything is a class”

Diederich (PyCon 2012 abstract, official): *“Classes must be nouns but not every noun must be a class. If your class only has two methods and one of them is `__init__` you probably meant to write a function.”*

Namespaces (modules) group functions. Classes are for **state + behavior that travel together**, or **containers**. A class that only wraps a call is Java residue.

**Core test:** `__init__` + one method → function (or module-level function + dataclass args).

## Finding 2 — Three kinds of “class” (must not mix)

From Hynek (redux), inheritance is not one thing:

| Type | Verdict in Python | Meaning |
|------|-------------------|---------|
| **Code sharing** via subclass | **Bad** as a design center | Shared `self.x` hides where attributes live; mixin/MRO; subclass explosion if >1 axis varies |
| **Interface** (ADT) | **Useful** | “I need `read()`”; don’t care who |
| **Specialization** of a type you don’t control | **Optional / last resort** | Bend a framework class; prefer adapter if delegation isn’t huge |

Hynek: *don’t use subclassing for code sharing; don’t mix the types; a function is often enough.*

This **is** the Python mapping of S / O / L / I / D — not the five letters:

- **S** → small thing: function, dataclass, or one-job service — not a hierarchy
- **O / I / D** → **Protocol** (structural) or **ABC** (nominal) — new adapter, not a longer `if`
- **L** → if you subclass, honor the contract; Python usually **avoids** the subclass so LSP rarely comes up

## Finding 3 — Duck typing is the language; Protocol is how you *name* the duck

PEP 544: PEP 484 was **nominal** only; Protocols add **structural** subtyping (“static duck typing”). A class implements a Protocol by **having the methods**, not by inheriting.

stdlib already treats `Iterable` / `Sized` this way at runtime; PEP 544 makes that available for user types **statically**.

**Core:** DIP in Python ≠ `interface IFoo` + `class Foo : IFoo`. DIP = *parameter is a small Protocol* (or a function). ABC when you **own** the hierarchy and want instantiate-time `TypeError`.

| | `typing.Protocol` | `abc.ABC` |
|--|-------------------|-----------|
| Relationship | Structural (duck) | Nominal (must inherit or `register`) |
| 3rd-party types | Fit if methods match | Must subclass or register |
| Runtime enforce | Opt-in `@runtime_checkable` (names only) | Missing abstract method → `TypeError` on init |
| Default for ports | **Yes** | When you control all impls + want runtime fail |

## Finding 4 — Data vs behavior is a language feature, not a style opinion

PEP 557: classes that **exist to store values** were so common that stdlib generates `__init__` / `__repr__` / `__eq__` from **annotations**. Dataclass is a normal class (no special metaclass); it is **not** a replacement for attrs/Pydantic/ORM.

**Core split (Python, not SOLID):**

| Job | Mechanism |
|-----|-----------|
| Hold values (internal contracts) | `@dataclass` (`frozen=True` if immutable) |
| Validate untrusted / env | Pydantic / Settings (library), not dataclass-as-HTTP-body |
| Persist rows | ORM entity |
| Do work with deps | Plain `class` + `__init__` inject, **or** functions if no state |

Forcing `@dataclass` onto a service, or `__init__` that only assigns fields, both miss this split.

## Finding 5 — Hynek: not all SOLID letters carry equal weight in Python

From *Solid Snakes*: *“Not all of those principles are relevant to dynamic languages like Python.”* He singles out **SRP** (small, loosely coupled units — reason he wrote attrs).

So a Python rule that recites all five letters equally is **wrong for this language**. Weight:

1. **Don’t start with a class** (Diederich)
2. **Don’t subclass to share code** (Hynek type 1)
3. **Name the duck with a small Protocol** (PEP 544)
4. **Data bags are dataclasses** (PEP 557)
5. **SRP as “one reason / one seam”** — the SOLID letter that still pays

OCP/LSP/ISP become *consequences* of 2–4, not a checklist.

## Proposed core (ladder — same shape as Ponytail)

After you understand the behavior, stop at the first rung that holds:

```text
1. Function / module function?          (no lasting state)
2. Dataclass (or Pydantic at the edge)? (data only)
3. Functions + a dataclass of deps?     (light behavior)
4. One class, deps in __init__?         (state + behavior)
5. Small Protocol for the thing you inject?
6. Second adapter (fake/real) — now the seam is real
7. ABC / subclass only if you own a hierarchy
   or must bend a type you don’t control
```

Never: inherit to reuse helpers; mixin soup; God service; Protocol with 12 methods.

## What this means for the gsuper rule

Do **not** title the rule “SOLID”. Title it **Python objects** (or `python-modules`) and encode the ladder + the data/behavior/port table. Mention SOLID once as “SRP is the letter that still matters; the rest are the ladder.”

Keep lib hints (tenacity, pydantic) as **Ponytail rung 5** (installed dep) plus a short “don’t rewrite” table — not as the OOP core.

## Out of scope for this note

- Full attrs vs dataclass vs Pydantic feature matrix
- Metaclasses, descriptors (advanced; not the default path)
