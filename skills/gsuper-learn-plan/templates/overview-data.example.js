window.OVERVIEW_DATA = {
  eyebrow: "example",
  title: "Example overview",
  roles: "<strong>Spec quyết định.</strong> Overview báo cáo.",
  how: "Bấm widget. Đọc lecture.",
  catalog: {
    why: "Pick",
    heading: "Chart là bản đồ.",
    rows: [{ need: "Who owns what", use: "owns chips", here: "below" }]
  },
  arch: {
    topic: "ack",
    why: "Architecture",
    heading: "Example arch",
    q: "Toggle.",
    lecture: ["Full lecture on ack — agent writes this when the topic is weak."],
    recap: ["Short recap on ack."],
    now: {
      mermaid: "flowchart LR\n  A-->B",
      note: "<strong>Now.</strong> Example.",
      code: "put()"
    },
    after: {
      mermaid: "flowchart LR\n  A-->C",
      note: "<strong>After.</strong> Example.",
      code: "enqueue()"
    }
  },
  qa: {
    heading: "Q&A",
    groups: [
      {
        label: "System",
        ticket: false,
        items: [{ ask: "Does the facade own the queue?", sug: "<strong>No.</strong> Path in, files out." }]
      }
    ]
  },
  accumulate: {
    heading: "Takeaways",
    cards: [{ kind: "job", title: "One move", body: "Enqueue then 202." }],
    unverified: ["Not measured."]
  },
  depth: { ack: "full" },
  topics: {
    ack: {
      lecture: ["Full lecture on ack — agent writes this when the topic is weak."],
      recap: ["Short recap on ack."]
    }
  }
};
