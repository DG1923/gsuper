---
name: gsuper-write-spec-feature
description: >
  Write specs/feature/ using feature-shape (problem, shall, contract).
  Not system context. Not core wiring.
---

# Write spec — feature

Fill [../gsuper-write-spec/references/feature-shape.md](../gsuper-write-spec/references/feature-shape.md).

**Job:** increment job + shall + Verify.

**Layout (theo tính năng, mọi kind):**

```text
specs/feature/<feature>/index.md
specs/feature/<feature>/<child>.md
specs/algorithm/<feature>/<id>.md
specs/architecture/<feature>/<id>.md
plans/<feature>/YYYY-MM-DD-<ticket>.md
learn/<feature>/gsuper-pack-….md
```

`system/` một file cả app — không nest. Feature luôn là **folder + index.md** (kể cả không con). Child nằm **cùng folder** parent. Child / algorithm / plan / pack **không** cùng cấp root kind.

`srs/` **optional**. Một file chỉ lặp Surfaces/system → gộp vào `system/`, không mở `srs/product.md`.

## Apply

- [ ] ## Problem, ## Flow (what + why), ## Requirements, ## Contract
- [ ] Shall user + BE/AI/data
- [ ] Parent → children table; no override locked child
- [ ] NFR numbers or pointer to system
- [ ] No C4-only file; no import-law-only file

Next: **suggest** drifted siblings (system / architecture / algorithm) — one line + why — then **wait**. Do **not** auto-update them. User picks a row or none. Ticket → **gsuper-write-plan**.
