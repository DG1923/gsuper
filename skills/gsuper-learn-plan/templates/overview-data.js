window.OVERVIEW_DATA = {
  lang: "vi",
  eyebrow: "template preview · #61 sample data",
  title: "GPU trong process nhận HTTP thì restart API là giết job.",
  roles: "<strong>Spec quyết định.</strong> Code là sự thật lúc này. Overview báo cáo — không phải AC. Agent chỉ sửa file data này, không sửa HTML.",
  how: "Bấm widget. Đọc lecture. Q&A tự trả lời trước. Tích lũy ở cuối.",
  catalog: {
    why: "Chọn theo câu hỏi",
    heading: "Chart là bản đồ. Lecture mới là bài.",
    q: "Mermaid đủ. Bỏ loại không có câu hỏi.",
    rows: [
      { need: "Who owns what", use: "owns chips", here: "<span class='here'>bấm box ngay dưới</span>" },
      { need: "What talks to what", use: "flowchart", here: "<span class='here'>Now / After</span>" },
      { need: "Time order", use: "sequence + stepper", here: "<span class='here'>Next — đủ tới ack</span>" },
      { need: "Allowed events", use: "state + fire", here: "<span class='here'>Timeout vs Exception</span>" }
    ]
  },
  owns: {
    why: "Owns",
    heading: "Mỗi box một việc. Đừng đổ queue vào facade.",
    q: "Bấm theo chiều request. Cột đỏ là assumption hay sai khi review PR.",
    prompt: "FastAPI → queue/broker → worker → VibeProcessor. Postgres ghi status. Lease chỉ là marker.",
    lecture: [
      "Now: FastAPI vừa nhận HTTP vừa giữ GPU. After: FastAPI enqueue rồi 202; GPU ở worker."
    ],
    items: [
      {
        label: "FastAPI",
        owns: "HTTP: nhận file, persist upload row, trả 202. After: gọi enqueue rồi xong request.",
        not: "Không chạy GPU. Không ack message. Không cắt highlight.",
        miss: "Tưởng restart API không đụng job — đúng After, sai Now (GPU + asyncio.Queue cùng process)."
      },
      {
        label: "asyncio.Queue",
        owns: "Now: RAM buffer giữa upload handler và background task cùng process.",
        not: "Không survive restart. Không phải broker. Không phải QueueClient.",
        miss: "Tưởng put() = enqueue(). Path upload hôm nay vẫn put."
      },
      {
        label: "QueueClient",
        owns: "Lib: enqueue / consume / ack. Có trong repo.",
        not: "Không tự gắn vào upload. Có rồi ≠ path đã dùng.",
        miss: "Thấy class trong lib rồi kết luận đã tách process."
      },
      {
        label: "RabbitMQ",
        owns: "After: giữ unacked message. Redeliver khi worker chết trước ack.",
        not: "Không giữ CUDA context. Không ghi upload status. Không thay lease.",
        miss: "Tưởng broker chạy GPU, hoặc Now cũng đã nằm trên RMQ."
      },
      {
        label: "Worker",
        owns: "After: consume, gọi VibeProcessor, ghi status, ack trong finally (kể cả raise).",
        not: "Không nhận HTTP. Không sở hữu pickleball scoring.",
        miss: "Ack trước generate, hoặc quên finally → mất/double-run."
      },
      {
        label: "VibeProcessor",
        owns: "Facade: path in, files out. Detectors → rounds → score → cut.",
        not: "Không queue, không HTTP, không upload status, không timeout 1800s.",
        miss: "Nhét keep_ratio / scoring vào PR tách process, hoặc pickleball ở lại API."
      },
      {
        label: "Postgres",
        owns: "Upload row + status (queued / processing / completed / stopped / error).",
        not: "Không phải hàng đợi job. Boot replay DB ≠ job còn trên broker.",
        miss: "Now: load_pending_uploads nhét GPU lại vào HTTP. After: đừng auto-run stale processing."
      },
      {
        label: "Redis lease",
        owns: "Marker claim ~60s. Hết hạn ≠ job chết.",
        not: "Không phải GPU TTL. Không thay ack. Không bằng wait_for(1800).",
        miss: "Lease expire → reclaim/kill GPU. Missing lease ≠ failed."
      }
    ]
  },
  arch: {
    topic: "gpu-process",
    why: "Architecture",
    heading: "GPU đang ở process nào?",
    q: "Một nước đi. Toggle rồi đọc lecture.",
    now: {
      mermaid: "flowchart LR\n  Browser --> FastAPI\n  FastAPI --> GPU[VibeProcessor GPU]\n  FastAPI --> Postgres\n  FastAPI -.-> QC[QueueClient unused]\n  QC -.-> RMQ[RabbitMQ]",
      note: "<strong>Now.</strong> GPU trong API process. <code>QueueClient</code> có mà path upload không gọi.",
      code: "<span class='c'># RAM — dies with the process</span>\nawait self.upload_queue.put({\"upload_id\": upload.id})"
    },
    after: {
      mermaid: "flowchart LR\n  subgraph api [API process]\n    FastAPI\n  end\n  subgraph wk [Worker process]\n    GPU[VibeProcessor GPU]\n  end\n  FastAPI --> RMQ[RabbitMQ]\n  RMQ --> GPU",
      note: "<strong>After.</strong> FastAPI enqueue. Worker chạy VibeProcessor. Ack trong <code>finally</code>.",
      code: "<span class='c'># broker</span>\nawait client.enqueue(\"video.highlight\", payload)"
    },
    lecture: [
      "<code>QueueClient</code> đã có ≠ đã tách xong. Path upload vẫn <code>put</code> vào RAM. Restart FastAPI giết GPU job.",
      "Nước đi: persist + enqueue ở API. Facade sang worker. Highlight không gọi <code>fail()</code>."
    ],
    recap: [
      "GPU cùng API process. Upload vẫn <code>put</code>."
    ]
  },
  seq: {
    topic: "ack-after-handle",
    why: "Sequence",
    heading: "HTTP xong trước GPU",
    q: "Bấm Next. Điểm ticket là mũi tên 202, không phải GPU nhanh hơn.",
    code: "<span class='k'>try</span>:\n    await self._handle(msg)\n<span class='k'>finally</span>:\n    await self._client.ack(msg)",
    lecture: [
      "Ack sau handle, trong <code>finally</code>. Claim ack-then-generate đã bị spec loại."
    ],
    recap: ["Ack trong <code>finally</code>. Không <code>fail()</code>."],
    steps: [
      { mermaid: "sequenceDiagram\n  participant B as Browser\n  participant A as API\n  B->>A: POST file", note: "<strong>1 · FastAPI.</strong> Bytes vào. GPU chưa chạy." },
      { mermaid: "sequenceDiagram\n  participant B as Browser\n  participant A as API\n  participant Q as RabbitMQ\n  B->>A: POST file\n  A->>Q: enqueue", note: "<strong>2 · QueueClient → RMQ.</strong> Message trên broker. Không phải <code>asyncio.Queue</code>." },
      { mermaid: "sequenceDiagram\n  participant B as Browser\n  participant A as API\n  participant Q as RabbitMQ\n  B->>A: POST file\n  A->>Q: enqueue\n  A-->>B: 202", note: "<strong>3 · 202.</strong> HTTP xong. API process trống. Đây là nước đi của ticket." },
      { mermaid: "sequenceDiagram\n  participant Q as RabbitMQ\n  participant W as Worker\n  Q->>W: consume", note: "<strong>4 · Worker.</strong> Claim message. Unacked cho đến <code>finally</code>. GPU vẫn chưa chạy." },
      { mermaid: "sequenceDiagram\n  participant W as Worker\n  participant G as VibeProcessor\n  W->>G: process_video", note: "<strong>5 · Facade.</strong> Path in, files out. Timeout 1800s ở handle, không trong VibeProcessor." },
      { mermaid: "sequenceDiagram\n  participant W as Worker\n  participant Q as RabbitMQ\n  W->>Q: ack", note: "<strong>6 · Ack.</strong> Trong <code>finally</code> — completed, error, hay raise. Highlight không <code>fail()</code>." }
    ]
  },
  state: {
    topic: "stopped-vs-error",
    why: "State",
    heading: "stopped không bán chung kệ với error",
    q: "Từ processing: Timeout vs Exception.",
    mermaid: "stateDiagram-v2\n  [*] --> queued\n  queued --> processing: consume\n  processing --> completed: ok\n  processing --> stopped: timeout\n  processing --> error: exception",
    start: "queued",
    resetNote: "<strong>queued.</strong> Bấm Consume.",
    chips: ["queued", "processing", "completed", "stopped", "error"],
    trans: {
      queued: { consume: ["processing", "Claimed. Unacked until finally."] },
      processing: {
        ok: ["completed", "Handle xong rồi ack."],
        timeout: ["stopped", "#63: timeout → stopped. Code hôm nay ghi error — đừng copy."],
        exc: ["error", "User retry. Không fail()."]
      }
    },
    code: "except asyncio.TimeoutError:\n    update_status(..., \"error\")  <span class='c'># today — wrong for #63</span>",
    lecture: [
      "Timeout là sản phẩm còn sống. Exception là retry. Một status cho cả hai thì reject PR."
    ],
    recap: ["Timeout → stopped. Exception → error."],
  },
  die: {
    topic: "restart-ram",
    why: "What-if",
    heading: "Process chết — job còn không?",
    q: "Chọn một thế giới.",
    prompt: "Chọn Now hoặc After.",
    now: "<strong>Now.</strong> Job trong RAM. Boot <code>load_pending_uploads</code> — GPU lại trong HTTP.",
    after: "<strong>After.</strong> Unacked còn trên broker. Redeliver. Không auto-run stale <code>processing</code>.",
    code: "self._r.set(lease_key(id), \"1\", ex=60)  <span class='c'># marker, not job TTL</span>",
    lecture: [
      "Lease 60s hết hạn lúc GPU còn chạy là bình thường. Missing lease ≠ dead job."
    ],
    recap: ["Now job ở RAM. After unacked trên broker."],
  },
  process: {
    topic: "vibeprocessor-facade",
    why: "Process",
    heading: "Hộp coral không phải hàng đợi",
    q: "Nút Not this class quan trọng hơn Cut.",
    mermaid: "flowchart LR\n  Det[detectors] --> Rounds --> Score --> Cut",
    prompt: "Bấm một stage.",
    labels: { det: "Detectors", round: "Rounds", score: "Score", cut: "Cut", not: "Not this class" },
    stages: {
      det: "<strong>Detectors.</strong> Ball + Event + Audio. Không HTTP, không queue.",
      round: "<strong>Rounds.</strong> XGBoost 5–22s. Vẫn trong facade.",
      score: "<strong>Score.</strong> Highlight xấu ≠ ticket #61.",
      cut: "<strong>Cut.</strong> <code>keep_ratio</code> từ upload row. Files out.",
      not: "<strong>Not this class.</strong> Không enqueue / ack / status. Cap 1800s ở service."
    },
    code: "result = await asyncio.wait_for(processor.process_video(...), timeout=1800)",
    lecture: [
      "#61 chuyển chỗ gọi VibeProcessor, không viết lại pickleball."
    ],
    recap: ["Facade: path in, files out."],
  },
  qa: {
    why: "80 / 20",
    heading: "Tự trả lời. Không được thì mở.",
    q: "Cho bạn — không phải checklist implement.",
    groups: [
      {
        label: "System",
        ticket: false,
        items: [
          { ask: "VibeProcessor có sở hữu queue / HTTP / status không?", sug: "<strong>Không.</strong> Facade: path in, files out. Service hoặc worker handle mới ghi status." }
        ]
      },
      {
        label: "Ticket",
        ticket: true,
        items: [
          { ask: "Handle raise thì vẫn ack?", sug: "<strong>Có.</strong> <code>finally</code> ack. Handle nên ghi <code>error</code> rồi return khi được." }
        ]
      }
    ]
  },
  accumulate: {
    why: "Tích lũy",
    heading: "Mang sang ticket sau — không phải AC",
    q: "Implement lấy Done when ở spec MD.",
    cards: [
      { kind: "job", title: "GPU ra khỏi API", body: "After: FastAPI enqueue; worker gọi VibeProcessor." },
      { kind: "job", title: "Ack sau handle", body: "finally. Highlight không fail()." },
      { kind: "base", title: "RAM queue chết theo process", body: "Survive restart → không asyncio.Queue." },
      { kind: "bug", title: "Lease 60s ≠ GPU 30 phút", body: "Marker, không phải kill switch." }
    ],
    unverified: [
      "Tần suất outage prod — chưa đo.",
      "Không thấy vòng reclaim-on-lease-expire trên highlight path."
    ]
  }
};
