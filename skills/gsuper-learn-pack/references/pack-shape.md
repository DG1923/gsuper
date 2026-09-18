# Pack shape

Implement never uses this file as AC. Plan `Done when` stays in Markdown.

The pack is for the **user to understand first**. Upload to another chat is optional and comes after the explanation.

## Paths

```text
.agent-workflow/learn/gsuper-pack-<repo>-<ticket-id>.md
```

`conventions.md` is **not project law**. Do not copy must/must-not from the pack into that file.

Never name the pack `pack.md`. Helper: `scripts/names.py` `pack_filename`.

Do not write `need-to-know-*.md` or `self-report-*.md`.

## Pack header (required)

```markdown
# Pack: <repo> / <ticket-id>
- stage: after-brainstorm | after-spec | after-implement
- generated: YYYY-MM-DD
```

Then, **in this order**:

1. **Giải thích** — việc này là gì, đọc xong bạn hiểu được gì (ngôn ngữ tự nhiên, lời user đã dùng)
2. **Overview** — **chuyện gì xảy ra** (2–4 câu) rồi **một mermaid E2E** in a ` ```mermaid ` fence rồi bảng bước bằng lời thường (vào gì → làm gì → ra gì). Name table / must-must-not / jump links / drift vs code
3. **Per-unit** — mỗi luồng: câu chuyện ngắn → mermaid → giải thích từng bước dễ hiểu; excerpt code **sau**
4. Quiz (câu hỏi bằng lời thường)
5. Optional: how to use in another chat (không được đứng đầu)

A pack that is only overview, or only detail, is incomplete.

Voice: explain to the person who will **read and decide**, not to a compiler. Self-contained: this file alone is enough to understand the ticket.

## Per-unit section (required for each live unit / stage / service)

Mỗi đơn vị:

1. **Chuyện gì xảy ra** — 2–5 câu tự nhiên (học viên / hệ thống làm gì; ra cái gì)
2. **Flow** — mermaid `flowchart` in a ` ```mermaid ` fence (bước user thấy hoặc bước hệ thống). Not ASCII trees. Never a bare `flowchart`.
3. **Giải thích bước** — mỗi box: vào gì → ra gì, bằng lời thường (không chỉ tên hàm)
4. **I/O** — file / field cần nhớ, sau lời giải thích
5. **Failure / traps** — khi nào hỏng, bằng lời thường
6. **Excerpt** (optional but usual after implement) — path + fence ngắn **sau** lời giải thích. Do not replace the explanation with the excerpt.

Overview-only is a failed pack.  
Detail-only (no Part A map) is also a failed pack.  
Excerpt-only with no natural-language story is a failed pack.

## Quiz (required)

Open questions that can be graded **only** from this file. No answer key, no `why_right`. Cover flows in plain language, not just symbol names.

## Honesty

If a user claim or repo doc contradicts cited code, the pack states the contradiction. Do not paper over it. Paraphrase is **allowed**; wrong paraphrase vs code → drift row.

## No dump-concat

Do not shell-concat entire specs or modules into the pack. Excerpts are copy-paste of **chosen** functions only, and they come after the explanation.

## Stages

| When | Write |
|------|--------|
| After brainstorm | pack, stage `after-brainstorm` |
| After spec or plan | pack, stage `after-spec` |
| After implement | pack, stage `after-implement` |
| Unreadable spec / foreign repo | pack from **code**, mark doc drift |
