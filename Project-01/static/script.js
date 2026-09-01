const form = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("send-button");
const thinkingButton = document.getElementById("thinking-button");

function addMessage(sender, text, type) {
  const message = document.createElement("div");
  message.className = `message ${type}`;

  const name = document.createElement("div");
  name.className = "message-name";
  name.textContent = sender;

  const content = document.createElement("div");
  content.className = "message-content";
  content.textContent = text;

  message.appendChild(name);
  message.appendChild(content);

  messages.appendChild(message);

  // Scroll to newest message
  messages.parentElement.scrollTop = messages.parentElement.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const prompt = promptInput.value.trim();

  if (!prompt) {
    return;
  }

  addMessage("You", prompt, "user");

  promptInput.value = "";
  sendButton.disabled = true;
  promptInput.disabled = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: prompt,
        enable_thinking: enableThinking,
      }),
    });

    if (!response.ok) {
      throw new Error("Request failed");
    }

    const data = await response.json();

    addMessage("Qwen", data.response, "assistant");
  } catch (error) {
    addMessage(
      "System",
      "Sorry, something went wrong while contacting Qwen.",
      "assistant",
    );

    console.error(error);
  } finally {
    sendButton.disabled = false;
    promptInput.disabled = false;
    promptInput.focus();
  }
});

// Focus the input when the page loads
promptInput.focus();

let enableThinking = false;

thinkingButton.addEventListener("click", () => {
  enableThinking = !enableThinking;

  thinkingButton.classList.toggle("active", enableThinking);

  thinkingButton.setAttribute("aria-pressed", enableThinking);

  thinkingButton.title = enableThinking
    ? "Thinking mode: On"
    : "Thinking mode: Off";
});
