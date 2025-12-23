async function upload() {
  const file = document.getElementById("fileInput").files[0];
  if (!file) return alert("Please select a PDF");

  const loading = document.getElementById("loading");
  const analyzeBtn = event.target;

  loading.classList.remove("hidden");
  analyzeBtn.disabled = true;

  document.getElementById("analysis").classList.add("hidden");
  document.getElementById("chatSection").classList.add("hidden");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    renderAnalysis(data);

    document.getElementById("analysis").classList.remove("hidden");
    document.getElementById("chatSection").classList.remove("hidden");

  } catch (e) {
    alert("Failed to analyze report");
  } finally {
    loading.classList.add("hidden");
    analyzeBtn.disabled = false;
  }
}

function fillList(id, items) {
  const ul = document.getElementById(id);
  ul.innerHTML = "";
  items.forEach(i => {
    const li = document.createElement("li");
    li.innerText = i;
    ul.appendChild(li);
  });
}

async function ask() {
  const qInput = document.getElementById("question");
  const question = qInput.value.trim();
  if (!question) return;

  addMessage(question, "user");
  qInput.value = "";

  const res = await fetch(`/ask?question=${encodeURIComponent(question)}`, {
    method: "POST"
  });

  const data = await res.json();
  addMessage(data.answer, "ai");
}

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerText = text;

  const chatBox = document.getElementById("chatBox");
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function renderAnalysis(data) {
  document.getElementById("summary").innerText =
    data.executive_summary.join(" ");

  fillList("observations",
    data.financial_highlights.concat(data.risks_red_flags)
  );

  fillList("actions", data.recommended_actions);
}
