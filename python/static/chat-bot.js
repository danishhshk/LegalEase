const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");

let userText = null;
const API_KEY = "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"; // Paste your API key here
const legalTermsKeywords = [
    "contract",
    "law",
    "court",
    "legal",
    "attorney",
    "justice",
    "section",
    "case",
    "judgment",
    "plaintiff",
    "defendant",
    "litigation",
    "appeal",
    "witness",
    "testimony",
    "evidence",
    "judge",
    "jury",
    "verdict",
    "arbitration",
    "settlement",
    "appeal",
    "crime",
    "felony",
    "misdemeanor",
    "penalty",
    "constitution",
    "amendment",
    "rights",
    "tort",
    "damages",
    "injunction",
    "negligence",
    "liability",
    "statute",
    "regulation",
    "legal entity",
    "jurisdiction",
    "inheritance",
    "probate",
    "power of attorney",
    "discrimination",
    "intellectual property",
    "trademark",
    "patent",
    "copyright",
    "legal precedent",
    "legal aid",
    "notary",
    "affidavit",
    "deposition",
    "mediation",
    "parole",
    "probation",
    "appeal",
    "court order",
    "bail",
    "plea",
    "legal system",
    "legal advice",
    "legal rights",
    "legal responsibility",
    "legal proceedings",
    "legal document",
    "legal assistance",
    "legal counsel",
    "legal dispute",
    "legal fees",
    "legal judgment",
    "legal obligations",
    "legal opinion",
    "legal question",
    "legal representative",
    "legal status",
    "legal theory",
    "legal code",
    "legal framework",
    "legal interpretation",
    "legal issue",
    "legal analysis",
    "legal practice",
    "legal regulation",
    "legal research",
    "legal terms",
    "legal terminology",
    "legal definition",
    "legal history",
    "legal philosophy",
    "legal profession",
    "legal system",
    "legal education",
    "legal ethics",
    "legal reform",
    "legal studies",
    "legal writing",
    "legal process",
    "legal scholarship",
    "legal concept",
    "legal culture",
    "legal philosophy",
    "legal sociology",
    "legal theory",
    "legal philosophy",
    "legal research",
    "legal studies",
    "legal writing",
    "legal process",
    "legal scholarship",
    "legal concept",
    "legal culture",
    "legal philosophy",
    "legal sociology",
    "legal theory",
    "legal philosophy",
    "legal research",
    "legal studies",
    "legal writing",
    "legal process",
    "legal scholarship",
    "legal concept",
    "legal culture",
    "legal philosophy",
    "legal sociology",
    "legal theory"
  ];
  

const checkForLegalTerms = (text) => {
  const lowercasedText = text.toLowerCase();
  return legalTermsKeywords.some((keyword) => lowercasedText.includes(keyword));
};

const loadDataFromLocalstorage = () => {
  // Load saved chats and light theme from local storage and apply/add on the page
  const lightTheme = localStorage.getItem("lightTheme");

  document.body.classList.toggle("light-mode", lightTheme === "enabled");
  themeButton.innerText = document.body.classList.contains("light-mode")
    ? "light_mode"
    : "light_mode";

  const defaultText = `<div class="default-text">
                            <h1>LegalEase Support</h1>
                            <p>Engage in conversations backed by AI expertise, offering tailored legal insights and support at your fingertips.<br> Your chat history will be displayed here.</p>
                        </div>`;

  chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
  chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to the bottom of the chat container
};

const createChatElement = (content, className) => {
  const chatDiv = document.createElement("div");
  chatDiv.classList.add("chat", className);
  chatDiv.innerHTML = content;
  return chatDiv;
};

const getChatResponse = async (incomingChatDiv) => {
  const API_URL = "https://api.openai.com/v1/completions";
  const pElement = document.createElement("p");

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: "text-davinci-003",
      prompt: `Legal term: ${userText}`, // Adjust the prompt to focus on legal terms
      max_tokens: 2048,
      temperature: 0.2,
      n: 1,
      stop: null,
    }),
  };

  try {
    const response = await (await fetch(API_URL, requestOptions)).json();
    pElement.textContent = response.choices[0].text.trim();
  } catch (error) {
    pElement.classList.add("error");
    pElement.textContent =
      "Oops! Something went wrong while retrieving the response. Please try again.";
  }

  incomingChatDiv.querySelector(".typing-animation").remove();
  incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
  localStorage.setItem("all-chats", chatContainer.innerHTML);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

const copyResponse = (copyBtn) => {
  const reponseTextElement = copyBtn.parentElement.querySelector("p");
  navigator.clipboard.writeText(reponseTextElement.textContent);
  copyBtn.textContent = "done";
  setTimeout(() => (copyBtn.textContent = "content_copy"), 1000);
};

const showTypingAnimation = () => {
  const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="./robot.png" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
  const incomingChatDiv = createChatElement(html, "incoming");
  chatContainer.appendChild(incomingChatDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  getChatResponse(incomingChatDiv);
};

const handleOutgoingChat = () => {
  userText = chatInput.value.trim();
  if (!userText) return;

  chatInput.value = "";
  chatInput.style.height = `${initialInputHeight}px`;

  const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="./user_logo.png" alt="user-img">
                        <p>${userText}</p>
                    </div>
                </div>`;

  const outgoingChatDiv = createChatElement(html, "outgoing");

  // Check if the user's input contains legal terms before adding it to the chat
  if (checkForLegalTerms(userText)) {
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(showTypingAnimation, 500);
  } else {
    // Inform the user that the input doesn't contain legal terms
    const errorMessage = `<div class="chat-content">
                                <div class="chat-details error">
                                    <p>Your input doesn't seem to contain legal terms. Please provide a legal-related query.</p>
                                </div>
                            </div>`;
    const errorDiv = createChatElement(errorMessage, "error");
    chatContainer.appendChild(errorDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
  }
};

deleteButton.addEventListener("click", () => {
  if (confirm("Are you sure you want to delete all the chats?")) {
    localStorage.removeItem("all-chats");
    loadDataFromLocalstorage();
  }
});

themeButton.addEventListener("click", () => {
  // Theme is set to light only, so no need to toggle
  localStorage.setItem("lightTheme", "enabled");
  themeButton.innerText = "light_mode";
});

const initialInputHeight = chatInput.scrollHeight;

chatInput.addEventListener("input", () => {
  chatInput.style.height = `${initialInputHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleOutgoingChat();
  }
});

loadDataFromLocalstorage();
sendButton.addEventListener("click", handleOutgoingChat);
