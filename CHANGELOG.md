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
