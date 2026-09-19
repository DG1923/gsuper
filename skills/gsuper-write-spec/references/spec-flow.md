# Spec doc flow (not the ship path)

Ship remains: brainstorm → **plan** → implement → review.

When the user asks for **project docs**, write **one kind per pass** (this increment). Do not fill every folder in one sitting.

**Existing large repo** (code already there; `specs/` empty or stale) → **gsuper-write-spec-sync** first: inventory → map → wait → then this chain from the chosen kind.

```text
intent (brainstorm)
  → system        bài toán cả app, C4 context, NFR chung
  → architecture  core: layers, composition, DB, AI wiring
  → algorithm     recipe khó (json3, chunk/FTS, two-pass) — skip if How already locked
  → feature       feature/<feature>/index.md + child (một increment)
  → plan          ticket AC

`srs/` chỉ khi có shall **cả product** không thuộc một feature — không tạo file một mình để làm mục lục.
```

```mermaid
flowchart LR
  I[Intent] --> Sys[system]
  Sys --> Arch[architecture / core]
  Arch --> Alg[algorithm]
  Alg --> Feat[feature]
  Feat --> Plan[plan]
```

| Kind | User said | Sub-skill |
|------|-----------|-----------|
| sync | project có sẵn, phân tích, specs thiếu/lệch | `gsuper-write-spec-sync` |
| system | hệ thống, context, NFR cả app | `gsuper-write-spec-system` |
| architecture | lớp, core, DB, composition | `gsuper-write-spec-architecture` |
| algorithm | thuật toán, recipe, How | `gsuper-write-spec-algorithm` |
| feature | tính năng, shall, parent folder + index | `gsuper-write-spec-feature` |
| srs | hiếm — shall cả product, không trùng system | `gsuper-write-spec-feature` |

**Core** = `architecture/<feature>/` (thường `custom-course/core.md`). Không invent `specs/core/`.

Cùng slug tính năng: `plans/<feature>/`, `learn/<feature>/`, `algorithm/<feature>/`.

A later increment (user đang làm feature mới): write **that** kind only. Do **not** auto-update system / architecture / algorithm.

**Suggest, then wait** — one line per drifted sibling, then stop:

| Sibling | Suggest when | Skip when |
|---------|--------------|-----------|
| system | Surfaces / NFR / actors đổi (thêm `/courses`, số job) | Chỉ shall trong một feature |
| architecture | Thêm façade, bảng, store | HTTP cũ không đổi |
| algorithm | How mới (recipe dễ sai) | How đã lock (`captions`) hoặc lát chỉ fixture/HTTP |
| feature child / parent | Shall hoặc bảng children đổi | File không đụng increment |
| plan | User bắt đầu ticket | Chỉ đang viết docs |

Live `shadowing` / `captions` stay unless this increment changes them. Example: lát store+HTTP fixture → **feature** (or plan) now; **suggest** one line on `architecture/core` (bảng `courses`); **skip** `chunk-fts`. User picks. No silent four-file rewrite. After implement: specs stay until the user asks.
