# Material shape

Implement never uses this file as AC. Pack (`gsuper-learn-pack`) stays the system overview.

## Files

```text
.agent-workflow/learn/gsuper-material-<repo>-<ticket-id>-<concept-slug>.md
.agent-workflow/learn/samples/<concept-slug>/*.py
```

One concept → one MD + one sample dir. Overwrite the same slug if regenerated.

## Lesson header

```markdown
# Material: <repo> / <ticket> / <concept>

- stage: after-implement
- generated: YYYY-MM-DD
- sources: path:line …
- sample: .agent-workflow/learn/samples/<concept>/…
- run: python …
```

Then, in this order:

1. How to use tonight (15 min)
2. Sibling concepts listed, not written
3. **Part A — mental model** (one mermaid, name table, must/must-not, drift)
4. **Part B — sample** (I/O, numbers, run command)
5. Production excerpts + **sample name → live name**
6. Quiz (no answer key)
7. **Validate** checklist (filled, not left blank)

## Part A

One concept. Not the E2E pack map.

Must include:

- What production **does** (verbs, numbers, types)
- What the name **lies** about (if it does)
- One trap / miss / boundary from the real code

## Part B — sample

| Allowed | Forbidden |
|---|---|
| 1 `.py` + a few local files | `import` of `backend/` / app packages |
| Stdlib; print a table | GPU, network, Postgres, video decode |
| Same thresholds / buckets / types as live | “Cleaner” math that changes the answer |
| Semantic names + mapping table | Silent rename with no mapping |

`python <file>.py` must exit 0 without extra setup.

## Production mapping (required)

```markdown
| Sample | Production | File |
|--------|------------|------|
| `speed_bucket` | `acceleration` | `tracknet_service.py` `_compute_kinematics` |
```

## Quiz

3–6 open questions. Gradable **only** from this lesson + the sample stdout. Cover the taught behavior and the trap — not vocabulary.

## Validate (mandatory — do not skip)

Agent must **run** the sample and answer yes to every line, or rewrite:

- [ ] Every Part A claim has a `path:line` (or a verbatim excerpt) in live code
- [ ] Sample output matches that claim (same label / number / miss rule)
- [ ] No taught rule was replaced with a textbook version
- [ ] Misleading production names are named, not “fixed”
- [ ] Quiz is answerable from sample + excerpts only
- [ ] `python …` ran this turn, exit 0

If any box is no → the lesson is not done.

## Anti-patterns (seen)

| Invented / simplified wrong | Live | Why it fails Validate |
|---|---|---|
| Teach `acceleration` as Δv | String speed bucket | Invented behavior |
| Bbox of **all** cells `> 0.5` | Largest **contour** bbox | Lost the taught selection rule |
| Skip miss frames in the toy | Miss → `speed=-1`, `unknown` | Dropped the edge case |
