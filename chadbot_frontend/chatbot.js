document.addEventListener("DOMContentLoaded", function () {
  const chatbotContainer = document.createElement("div");
  chatbotContainer.id = "chadbot-container";

  chatbotContainer.innerHTML = `
    <div id="chadbot-header">Chadbot AI Assistant <span id="chadbot-close" title="Close">&#10005;</span></div>
    <div id="chadbot-messages"></div>
    <form id="chadbot-form">
      <input type="text" id="chadbot-input" placeholder="Ask me about Tech Kshetra..." autocomplete="off" />
      <button type="submit">Send</button>
    </form>
  `;

  document.body.appendChild(chatbotContainer);

  const closeBtn = document.getElementById("chadbot-close");
  const messagesDiv = document.getElementById("chadbot-messages");
  const form = document.getElementById("chadbot-form");
  const input = document.getElementById("chadbot-input");

  closeBtn.addEventListener("click", () => {
    chatbotContainer.style.display = "none";
    openBtn.style.display = "block";
    chatbotContainer.style.height = "40px"; // reset height when closed
    chatbotContainer.style.fontSize = "14px"; // reset font size when closed
  });

  // Show chatbot button with custom circular style and text
  const openBtn = document.createElement("button");
  openBtn.id = "chadbot-open-btn";
  openBtn.title = "Take Don't Ride in Taxi";
  openBtn.textContent = "🚕"; // Taxi emoji as logo
  document.body.appendChild(openBtn);

  openBtn.addEventListener("click", () => {
    chatbotContainer.style.display = "flex";
    openBtn.style.display = "none";
    input.focus();
    // Increase height and font size when opened
    chatbotContainer.style.height = "500px";
    chatbotContainer.style.fontSize = "18px";
  });

  // Initial intro message
  addMessage("Chadbot AI Assistant", "Hello! I am Chadbot AI Assistant of Tech Kshetra. How can I assist you today?");

  function addMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = sender === "Chadbot AI Assistant" ? "chadbot-message bot" : "chadbot-message user";
    msgDiv.textContent = text;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const userText = input.value.trim();
    if (!userText) return;
    addMessage("You", userText);
    input.value = "";

    // Local handling for greetings and simple conversation
    const greetings = ["hi", "hello", "hey"];
    if (greetings.includes(userText.toLowerCase())) {
      addMessage("Chadbot AI Assistant", "Hello! What is your problem?");
      return;
    }

    // Otherwise, send to backend for database Q&A
    fetch("http://localhost:8000/chatbot/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: "user", message: userText }),
    })
      .then((res) => res.json())
      .then((data) => {
        addMessage("Chadbot AI Assistant", data.response);
      })
      .catch(() => {
        addMessage("Chadbot AI Assistant", "Sorry, I am having trouble responding right now.");
      });
  });
});
