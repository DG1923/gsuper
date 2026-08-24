window.QUIZ_DATA = {
  ticket: "example",
  eyebrow: "example · 2 questions",
  title: "Example quiz",
  roles: "Chọn xong khóa câu — đọc vì sao đúng/sai rồi Next.",
  questions: [
    {
      id: "q1",
      topic: "ack",
      prompt: "When is the message acked?",
      choices: ["Before handle", "After handle, in finally"],
      answer: 1,
      why_right: "Lib acks in finally even if handle raises.",
      why_wrong: ["Ack-then-generate loses work if the process dies mid-GPU.", ""],
      miss_if_wrong: "thought ack-then-generate"
    },
    {
      id: "q2",
      topic: "lease",
      prompt: "Redis lease 60s vs GPU 30 min means?",
      choices: ["Lease kill switch", "Marker; missing lease is not failed"],
      answer: 1,
      why_right: "Lease is a claim marker, not job TTL.",
      why_wrong: ["Reclaim while GPU runs is double-work.", ""],
      miss_if_wrong: "thought lease kills GPU"
    }
  ]
};
