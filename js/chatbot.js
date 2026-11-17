// Use "/chat" when the page is served by FastAPI (http://127.0.0.1:8000/...).
// If you open the page with Live Server instead, use "http://127.0.0.1:8000/chat".
const API_URL = location.hostname.endsWith("github.io")
  ? "https://YOUR-SPACE.hf.space/chat"
  : (location.port === "8000"
      ? "/chat"
      : "http://127.0.0.1:8000/chat");

const chat = document.getElementById('chat');
const scroller = document.getElementById('messages');
const form = document.getElementById('form');
const input = document.getElementById('msg');
const chips = document.getElementById('chips');
const heroHTML = chat.innerHTML;

const BOT_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.5 7.2L4 20l1-4.5A8 8 0 1 1 21 12z"/></svg>';

function addMessage(role, text) {
  const row = document.createElement('div');
  row.className = 'row ' + role;
  if (role === 'bot') {
    const av = document.createElement('div');
    av.className = 'avatar';
    av.innerHTML = BOT_ICON;
    row.appendChild(av);
  }
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;   // textContent: safe against HTML injection
  // Persian text must be RTL even if it starts with an English word
  // (otherwise the browser reorders words and punctuation).
  bubble.dir = /[\u0600-\u06FF]/.test(text) ? 'rtl' : 'ltr';
  bubble.style.textAlign = 'start';
  row.appendChild(bubble);
  chat.appendChild(row);
  scroller.scrollTop = scroller.scrollHeight;
  return row;
}

function addTyping() {
  const row = addMessage('bot', '');
  row.querySelector('.bubble').innerHTML = '<span class="dots"><span></span><span></span><span></span></span>';
  return row;
}

// Calls the FastAPI backend
async function getReply(userText) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText }),
  });
  if (!res.ok) throw new Error("Server error " + res.status);
  const data = await res.json();
  return data.reply;
}

async function send(text) {
  text = text.trim();
  if (!text) return;
  const hero = chat.querySelector('.hero');
  if (hero) { hero.remove(); const c = chat.querySelector('#chips'); if (c) c.remove(); }
  addMessage('user', text);
  input.value = '';
  const typing = addTyping();
  try {
    const reply = await getReply(text);
    typing.remove();
    addMessage('bot', reply);
  } catch (err) {
    console.error(err);
    typing.remove();
    addMessage('bot', 'Something went wrong. Please try again.');
  }
}

form.addEventListener('submit', e => { e.preventDefault(); send(input.value); });
if (chips) {
  chips.addEventListener('click', e => { if (e.target.classList.contains('chip')) send(e.target.textContent); });
}

// ---- mobile drawer ----
const menuBtn = document.getElementById('menuBtn');
const overlay = document.getElementById('overlay');
function setMenu(open) {
  document.body.classList.toggle('menu-open', open);
  if (menuBtn) menuBtn.setAttribute('aria-expanded', String(open));
}
if (menuBtn) menuBtn.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
if (overlay) overlay.addEventListener('click', () => setMenu(false));
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
document.querySelectorAll('.hist').forEach(b => b.addEventListener('click', () => setMenu(false)));

// ---- new chat (only if the button exists in the HTML) ----
const newChatBtn = document.getElementById('newChat');
if (newChatBtn) {
  newChatBtn.addEventListener('click', () => {
    setMenu(false);
    chat.innerHTML = heroHTML;
    const c = chat.querySelector('#chips');
    if (c) c.addEventListener('click', e => { if (e.target.classList.contains('chip')) send(e.target.textContent); });
  });
}