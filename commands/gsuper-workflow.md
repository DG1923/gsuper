---
name: gsuper-workflow
description: Run gsuper workflow orchestrator (gsuper-brainstorm → gsuper-write-spec → gsuper-write-plan → gsuper-implement → gsuper-review)
---

Follow the **gsuper-workflow** skill in this plugin. Start at the correct phase for the user’s request; do not skip gates.

If they ask to build/add/change a feature and intent is not locked → start with **gsuper-brainstorm** (clarify by grilling). Do not jump to implement.

If the ask is symptom-only (“just fix X”) or the problem looks misunderstood/hallucinated → **pause, remind, gsuper-brainstorm** — do not patch ngọn first.


