window.QUIZ_DATA = {
  ticket: "61",
  eyebrow: "template preview · 8 questions · mid/senior",
  title: "Trước khi review PR #63 — bạn đang giả định gì?",
  roles: "Chọn xong khóa câu — đọc vì sao đúng/sai rồi Next. Overview sau đó dày chỗ còn yếu. Agent chỉ ghi file data này.",
  questions: [
    {
      id: "q1",
      topic: "gpu-process",
      prompt: "Upload highlight đang chạy <code>VibeProcessor</code> ở process nào — và vì sao restart FastAPI là sự cố?",
      choices: [
        "Worker process riêng; restart API không đụng GPU.",
        "Cùng FastAPI process; restart giết job trong RAM/<code>asyncio.Queue</code>.",
        "RabbitMQ process; broker giữ GPU context.",
        "Chỉ Postgres; process không quan trọng."
      ],
      answer: 1,
      why_right: "Now: GPU nằm trong process nhận HTTP. <code>upload_queue</code> là RAM. Kill uvicorn = kill job.",
      why_wrong: [
        "Đó là After, chưa phải code hôm nay. Worker process chưa nhận highlight.",
        "",
        "Broker không chạy CUDA. RabbitMQ giữ message, không giữ GPU context.",
        "Postgres giữ row/status. Job đang chạy sống ở process + RAM queue, không ở DB."
      ],
      miss_if_wrong: "thought GPU already lives outside the API process"
    },
    {
      id: "q2",
      topic: "put-vs-enqueue",
      prompt: "<code>QueueClient.enqueue</code> đã có trong lib. Kết luận nào đúng cho path upload hôm nay?",
      choices: [
        "Đã tách xong — upload gọi enqueue.",
        "Có rồi ≠ dùng rồi. Upload vẫn <code>upload_queue.put</code>.",
        "Enqueue chỉ cho Drive.",
        "Put và enqueue là alias."
      ],
      answer: 1,
      why_right: "QueueClient là lib. Path upload highlight vẫn <code>put</code> vào <code>asyncio.Queue</code>.",
      why_wrong: [
        "Class tồn tại không chứng minh call site đã đổi. Đọc upload handler, đừng đọc lib folder.",
        "",
        "Không phải phạm vi câu này — và cũng không cứu được việc upload highlight chưa enqueue.",
        "<code>put</code> = RAM cùng process. <code>enqueue</code> = broker. Hai chỗ chết khác nhau khi restart."
      ],
      miss_if_wrong: "thought QueueClient existing means the upload path already uses the broker"
    },
    {
      id: "q3",
      topic: "ack-after-handle",
      prompt: "Message được ack khi nào? Highlight có được gọi <code>fail()</code> không?",
      choices: [
        "Ack trước generate để khỏi mất message; fail() nếu GPU lỗi.",
        "Ack sau handle, trong lib <code>finally</code> (kể cả raise). Highlight không fail().",
        "Ack chỉ khi completed; timeout thì nack.",
        "Worker không ack — Redis lease thay ack."
      ],
      answer: 1,
      why_right: "Lib ack trong <code>finally</code>. Handle ghi status rồi return. Highlight path không <code>fail()</code>.",
      why_wrong: [
        "Ack-then-generate: crash giữa chừng = mất việc đã ack. Spec loại claim này. <code>fail()</code> không phải API highlight.",
        "",
        "Timeout vẫn đi vào finally → ack. Status là stopped/error, không phải nack-as-control-plane.",
        "Lease là marker 60s. Ack mới là tín hiệu broker. Hai thứ không thay thế nhau."
      ],
      miss_if_wrong: "thought ack-then-generate or that highlight should fail()"
    },
    {
      id: "q4",
      topic: "lease-ttl",
      prompt: "Redis lease default 60s, GPU có thể chạy ~30 phút. Lease hết hạn nghĩa là gì?",
      choices: [
        "Job chết; worker phải reclaim/kill.",
        "Marker claim đã hết — GPU vẫn có thể đang chạy. Missing lease ≠ failed.",
        "Tự động nack và chạy lại.",
        "Bằng <code>wait_for(1800)</code>."
      ],
      answer: 1,
      why_right: "Lease = claim marker. GPU timeout là <code>wait_for(1800)</code> ở handle. Đừng gộp hai đồng hồ.",
      why_wrong: [
        "Hết lease không kill CUDA. Reclaim lúc GPU còn chạy = double-work hoặc giết job sống.",
        "",
        "Lease expire không phải nack. Message vẫn unacked cho đến finally.",
        "1800s là job timeout. 60s là Redis TTL. Số khác nhau vì vai trò khác nhau."
      ],
      miss_if_wrong: "thought 60s lease kills or equals the GPU job timeout"
    },
    {
      id: "q5",
      topic: "stopped-vs-error",
      prompt: "Spec #63: timeout/kill vs exception — status nào?",
      choices: [
        "Cả hai là <code>error</code> (như code hôm nay).",
        "Timeout/kill → <code>stopped</code> + API sống. Exception → <code>error</code> + retry. Đừng copy timeout→error.",
        "Timeout → <code>queued</code> replay.",
        "Cả hai là <code>stopped</code>."
      ],
      answer: 1,
      why_right: "Timeout = sản phẩm còn sống, user không retry như lỗi. Exception = retry. Code hôm nay gộp error — đó là bug so với spec.",
      why_wrong: [
        "Copy today vào #63 là fail review. Spec đã tách stopped vs error.",
        "",
        "Timeout không đẩy lại queued. Job đã chạy; status stopped.",
        "Exception không phải stopped. User cần retry, không phải 'đã dừng có chủ đích'."
      ],
      miss_if_wrong: "would copy today's timeout→error into #63"
    },
    {
      id: "q6",
      topic: "vibeprocessor-facade",
      prompt: "VibeProcessor sở hữu queue, HTTP, hay upload status không?",
      choices: [
        "Có — facade cũng enqueue.",
        "Không. Path in, files out. Status/timeout 1800s ở service (sau này: worker handle).",
        "Chỉ status, không queue.",
        "Pickleball thì nằm API; football thì worker."
      ],
      answer: 1,
      why_right: "Facade không biết broker. Call site (service now, worker after) mới ghi status và ôm timeout.",
      why_wrong: [
        "Enqueue là QueueClient + call site. Nhét enqueue vào facade = sai seam.",
        "",
        "Status cũng không thuộc facade. Upload row sống ở service/worker.",
        "Cùng facade. #61 chuyển chỗ gọi, không để pickleball lại trong HTTP."
      ],
      miss_if_wrong: "thought VibeProcessor owns queue/HTTP/status or that pickleball stays in API"
    },
    {
      id: "q7",
      topic: "restart-ram",
      prompt: "API process chết *now* vs worker chết *after* — job đi đâu?",
      choices: [
        "Cả hai: mất. User upload lại.",
        "Now: RAM mất, boot replay DB vào API (GPU lại trong HTTP). After: unacked còn broker, redeliver, không auto-run stale processing.",
        "Now: broker giữ. After: RAM giữ.",
        "Lease Redis restore job."
      ],
      answer: 1,
      why_right: "Chỗ job sống lúc chết process mới là kiến trúc. Now = RAM. After = unacked trên RMQ.",
      why_wrong: [
        "After không mất nếu chưa ack. Đó là lý do tách process.",
        "",
        "Đảo thế giới. Now chưa dùng broker trên path upload. After không giữ job trong RAM API.",
        "Lease hết 60s trong lúc GPU 30 phút là bình thường. Redis không replay payload."
      ],
      miss_if_wrong: "explained After restart as load_pending_uploads into the API"
    },
    {
      id: "q8",
      topic: "quality-not-this-ticket",
      prompt: "Pickleball highlight xấu. Nhét chỉnh <code>keep_ratio</code> vào PR worker được không?",
      choices: [
        "Được — cùng lúc tách process.",
        "Không. Quality knobs ở facade. #61/#63 chuyển call site.",
        "Chỉ được nếu football.",
        "Được nếu timeout 1800s đổi theo."
      ],
      answer: 1,
      why_right: "Scoring/cut ở VibeProcessor. Ticket này đổi process boundary, không đổi thuật toán.",
      why_wrong: [
        "Hai lý do review khác nhau. Gộp = PR không review được, và dễ regress quality.",
        "",
        "Sport không đổi seam. Cùng facade, cùng call-site move.",
        "Timeout là handle, keep_ratio là cut. Đổi một cái không cấp phép cái kia."
      ],
      miss_if_wrong: "would fix scoring in the process-move ticket"
    }
  ]
};
