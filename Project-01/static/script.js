const form = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const messages = document.getElementById("messages");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const prompt = promptInput.value.trim();

  if (!prompt) {
    return;
  }

  messages.innerHTML += `<p><strong>You:</strong> ${prompt}</p>`;

  promptInput.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: prompt,
    }),
  });

  const data = await response.json();

  messages.innerHTML += `<p><strong>Qwen:</strong> ${data.response}</p>`;
});
