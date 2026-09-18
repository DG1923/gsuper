## 0.8.4 - 2026-09-19

- **Mermaid:** every chart (chat and `.md`) uses a ` ```mermaid ` fence — no bare `flowchart`.
- **One concept → one file:** project must/must-not live in the matching spec-doc. `conventions.md` is not project law (init/migrate stub only). Do not write the same bullets into both.
- **Fix:** drop duplicate `sync_*` helpers in `store.py`; `memory.py init` writes the same “not project law” header as the template.

## 0.8.3 - 2026-09-19

- **User-first voice:** learn-pack explains in everyday words, then flow, then optional excerpt (paraphrase OK; drift if wrong vs code). Plan: “chuyện gì xảy ra” before mermaid; slices = việc rồi file. Review: **Kết luận cho bạn** before axes. learn-material: same voice.

## 0.8.2 - 2026-09-19

- **write-spec Apply check:** facts = live code/tests (conventions = target, may be stale). Happy path vs fallback; user Flow = real clicks; composition root vs router; HTTP fields vs domain types; FE+BE for system/feature. Overclaim → rewrite Design in the same pass; Reflection is leftover risk only.

## 0.8.1 - 2026-09-19

- **write-spec:** on user ask only — sync/analyze existing docs (propose map, rewrite, no verbatim copy) or bootstrap when structure is missing; **one** reflection pass (drift / Flow / readable / production) then wait for approve. Not on the ship path.

## 0.8.0 - 2026-09-19

- **Ship path:** brainstorm → plan → implement → review. Spec is no longer required per ticket.
- **Plan** is ticket AC (old spec fields + impacted files + testing approach + user-readable slices). No test/impl bodies.
- **Spec** is project docs under `specs/{algorithm,srs,feature,architecture,system}/`, written/updated when the user asks.
- **Memory:** `lock --kind plan|spec`, `--id` for spec-docs, `find --ticket` prefers plan, `sync --plans` and recursive `sync --specs`. Pointer only (no body ingest). Legacy dated specs dual-read when no plan exists.

## 0.7.1 - 2026-09-13

- **memory find --ticket**: scopes notes via artifact + path boundary; prefix `EL-6` matches `EL-6-…` not `EL-60`; unknown ticket → empty.
- **memory CLI** `edge`, `seam`, `sync` (pointer lock for specs missing from the index; does not ingest body).
- **hooks**: brainstorm / write-plan / review run `find` first; write-spec locks in the same turn after approve (or `sync` then `lock`).

## 0.7.0 - 2026-09-12

- **gsuper-memory**: `memory.py init|node|lock|find|around|note` on gitignored `.agent-workflow/memory.sqlite`. `init` creates schema if missing. `lock` writes approved spec pointer + must/must-not (no body). No project-specific seed. Hooks: find-first on implement, lock after spec approve, pack path only. No embeddings.
- **conventions**: `.agent-workflow/conventions.md` (workflow root) replaces the JSON conventions store. Agent edits only after user approval. Plugin `rules/*.mdc` unchanged.
- **init upgrade**: `memory.py init` keeps sqlite rows, creates `conventions.md` if missing, migrates leftover `learn/invariants.json` (delete JSON only after copy).
- **teach-flow**: brainstorm Teach + Flow (mermaid + I/O table) before Grill; each Q has Why / extra steps; spec template requires `## Flow`. Review Issues require Step + Why a bug. Teach / Flow / Why use **plain language** (user words + one gloss; no jargon-only). Symptom-gate: facts → Teach + Flow → grill (no skip to implement).
- **gsuper-review**: one pass — verified Bug hunt + Performance leaks (Now/Better/Bound). No mode menu. No finding without evidence.

## 0.6.0 - 2026-08-30

- **gsuper-learn-plan**: pack = spec + live-code excerpts (overview then detail). Mermaid required. Open quiz, no answer key. No need-to-know / self-report. No whole-file concat. Drift vs spec must be stated.

## 0.5.0 - 2026-08-26

- **gsuper-learn-plan**: unique `gsuper-pack-<repo>-<ticket>.md` (brainstorm/spec/implement) for read + ChatGPT/Claude upload; short `need-to-know` after implement; self-report known/unknown (no MCQ). Drop quiz/overview HTML.

## 0.4.0 - 2026-08-25

- **gsuper-learn-plan**: copy HTML templates; agent writes `quiz-data.js` / `overview-data.js` only. Path `.agent-workflow/learn/`. Quiz then `gaps.json` hard gate then adaptive overview. Init empty `invariants.json`.

## 0.3.0 - 2026-08-15

- Skill/command IDs prefixed `gsuper-<name>` for discoverability across agents

# Changelog

## 0.2.9 — 2026-08-15

- **DISTRIBUTE.md** + `scripts/install.{sh,ps1}` + root `plugin.json` (Agent Plugins) for CLI/server/other agents

## 0.2.8 — 2026-08-15

- **symptom-gate**: if user hallucinates / chưa hiểu vấn đề / chỉ sửa ngọn → pause, remind, gsuper-brainstorm before implement

## 0.2.7 — 2026-08-15

- **gsuper-brainstorm** entry hardened: MUST grill/clarify on new feature requests; workflow routes “làm chức năng” → gsuper-brainstorm before code

## 0.2.6 — 2026-08-15

- Timing lock: **gsuper-learn-plan** at spec/plan before implement; **gsuper-learn-self** only after plan done (post-implement)

## 0.2.5 — 2026-08-15

- **gsuper-learn-self** side track: personal concept cards after plan (separate from gsuper-learn-plan + phase /learn); `/gsuper-workflow-learn-self`; `learning/` dir

## 0.2.4 — 2026-08-15

- **gsuper-write-plan** hardened vs SP `writing-plans` + Matt `to-tickets` (vertical/Blocked-by); plan-shape.md; no SP subagent runtime

## 0.2.3 — 2026-08-15

- **gsuper-brainstorm** ≈ clarify: vendored grilling frontier + intent.md + SP approaches/hard-gate; maps workflow phases to clarify/specify/build/review

## 0.2.2 — 2026-08-15

- **gsuper-implement** locked: test → RED → frame → fill → GREEN; vendored Matt tdd/mock + Superpowers verify-RED + evidence-before-done

## 0.2.1 — 2026-08-15

- **gsuper-write-spec** skill now matches locked template (Seams, Sec/Perf line)
- **gsuper-implement** vendored Matt TDD + Superpowers execute-plan + phase build (no runtime skill deps)

## 0.2.0 — 2026-08-15

- **review** packaged: 3 axes (GitHub Defect verbatim, Spec Done when, Standards gsuper rules). Read-only. Drop Fowler baseline.
- Rules: `ponytail`, `python-objects`, `testing-seams`
- **workflow** review gate matches 3 axes

## 0.1.1 — 2026-08-15

- Expand **review**: two-axis Spec + Standards (parallel sub-agents), fixed-point diff, smell baseline reference, gsuper path discovery
- Expand **gsuper-brainstorm**: full checklist from collaborative design practice, hard gate, code-sample-first, isolation/YAGNI
- **workflow**: explicit review gate after implement; optional mid-task review

## 0.1.0 — 2026-08-15

- Initial gsuper plugin: workflow skills, PEP 8 + small-diffs rules, commands, `.agent-workflow` templates, GitHub parent/sub/PR templates, gsuper-learn-plan + diagram-design reference
