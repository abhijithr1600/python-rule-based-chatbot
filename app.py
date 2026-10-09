import streamlit as st
import datetime
import random
import json
import time
import re

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & VISUAL THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PyBuddy - Friendly Python Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic Dark CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-header {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .chat-header h1 {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        margin: 0;
        font-weight: 800;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(34, 197, 94, 0.2);
        border: 1px solid rgba(34, 197, 94, 0.4);
        color: #4ade80;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        margin-right: 6px;
        box-shadow: 0 0 8px #22c55e;
    }

    .stat-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }

    .stat-val {
        font-size: 1.4rem;
        font-weight: bold;
        color: #38bdf8;
    }

    .stat-lbl {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION (Memory & Chat History)
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 **Hi there! I'm PyBuddy**, a friendly general chatbot built entirely in Python using Streamlit.\n\nYou can talk to me about anything! Ask me for a joke, the time, a calculation, or just say hello!",
            "timestamp": datetime.datetime.now().strftime("%H:%M")
        }
    ]

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {
        "name": None,
        "favorite_color": None,
        "hobby": None
    }

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# -----------------------------------------------------------------------------
# 3. CONVERSATIONAL KNOWLEDGE BASE & PATTERN MATCHING (PURE PYTHON)
# -----------------------------------------------------------------------------

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything! 😂",
    "Why did the computer go to the doctor? Because it had a virus! 💻🤒",
    "What do you call a fake noodle? An impasta! 🍝",
    "Why was the math book sad? Because it had too many problems! 📚",
    "What gets wetter the more it dries? A towel! 🧼"
]

QUOTES = [
    "✨ *'The future belongs to those who believe in the beauty of their dreams.'* — Eleanor Roosevelt",
    "🚀 *'It always seems impossible until it's done.'* — Nelson Mandela",
    "💡 *'Success is not final, failure is not fatal: it is the courage to continue that counts.'* — Winston Churchill",
    "🌟 *'Do what you can, with what you have, where you are.'* — Theodore Roosevelt"
]

FUN_FACTS = [
    "🌌 **Did you know?** A day on Venus is longer than a year on Venus!",
    "🐙 **Did you know?** Octopuses have three hearts and blue blood!",
    "🍌 **Did you know?** Bananas are naturally slightly radioactive because of potassium!",
    "🍯 **Did you know?** Honey never spoils. Archeologists found 3000-year-old honey in Egyptian tombs that is still edible!"
]

def process_bot_response(user_input: str) -> str:
    """
    Pure Python Rule-Based Natural Language Response Engine.
    Uses regex, conditional logic, and string parsing (Zero AI/API dependencies).
    """
    text = user_input.lower().strip()
    memory = st.session_state.user_memory
    
    # 1. Check for Name Saving Intent ("My name is Alex", "I am John", "Call me Sam")
    name_match = re.search(r"\b(my name is|i am|call me)\s+([a-zA-Z]+)", text)
    if name_match:
        name = name_match.group(2).capitalize()
        # Avoid matching words like "happy" or "fine"
        if name.lower() not in ["happy", "sad", "fine", "good", "bored", "here"]:
            memory["name"] = name
            return f"Nice to meet you, **{name}**! 😊 I'll remember your name for the rest of our chat."

    # Check for Name Recall ("What is my name?", "Who am I?")
    if any(q in text for q in ["what is my name", "what's my name", "do you know my name", "who am i"]):
        if memory["name"]:
            return f"Your name is **{memory['name']}**! 👤"
        else:
            return "I don't know your name yet! You can tell me by typing e.g., *'My name is Alex'*."

    # 2. Check for Favorite Color / Hobby Saving
    color_match = re.search(r"\b(my favorite color is|i like the color)\s+([a-zA-Z]+)", text)
    if color_match:
        color = color_match.group(2)
        memory["favorite_color"] = color
        return f"Got it! **{color.capitalize()}** is a awesome color! 🎨"

    if "what is my favorite color" in text or "what's my favorite color" in text:
        if memory["favorite_color"]:
            return f"Your favorite color is **{memory['favorite_color']}**! 🎨"
        else:
            return "You haven't told me your favorite color yet! Say *'My favorite color is blue'*."

    # 3. Greetings & Friendly Chit-Chat
    if any(word in text for word in ["hello", "hi", "hey", "greetings", "yo", "hola", "good morning", "good afternoon", "good evening"]):
        user_name_str = f", {memory['name']}" if memory["name"] else ""
        return f"Hello{user_name_str}! 👋 How are you doing today?"

    if any(phrase in text for phrase in ["how are you", "how's it going", "how do you do", "how are u"]):
        return "I'm doing great, thank you for asking! 😊 How can I help you today?"

    if any(phrase in text for phrase in ["who are you", "what are you", "what's your name", "what is your name"]):
        return "I'm **PyBuddy**, a friendly normal chatbot built entirely in Python using Streamlit! 🤖"

    if any(phrase in text for phrase in ["who created you", "who made you", "who built you"]):
        return "I was built completely in pure Python using Streamlit! 🐍"

    # 4. Time & Date Information
    if any(word in text for word in ["time", "clock"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"🕒 The current local time is **{now}**."

    if any(word in text for word in ["date", "today"]):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"📅 Today's date is **{today}**."

    # 5. Jokes, Quotes & Fun Facts
    if any(word in text for word in ["joke", "funny", "laugh"]):
        return random.choice(JOKES)

    if any(word in text for word in ["quote", "inspire", "inspiration", "motivate"]):
        return random.choice(QUOTES)

    if any(word in text for word in ["fact", "fun fact", "trivia", "interesting"]):
        return random.choice(FUN_FACTS)

    # 6. Built-in Simple Math Calculator ("calculate 15 + 25", "100 * 5", "50 / 2")
    math_match = re.search(r"(\d+\s*[\+\-\*\/\^]\s*\d+)", text)
    if math_match:
        expr = math_match.group(1)
        try:
            # Safe basic evaluation of arithmetic expression
            safe_expr = expr.replace("^", "**")
            result = eval(safe_expr, {"__builtins__": None}, {})
            return f"🧮 **Calculation Result**: `{expr} = {result}`"
        except Exception:
            pass

    # 7. Common Everyday Topics
    if any(word in text for word in ["weather", "temperature", "rain", "sunny"]):
        return "☀️ I don't have a real-time weather sensor, but I hope it's bright and pleasant wherever you are today!"

    if any(word in text for word in ["movie", "film", "recommendation"]):
        return "🎬 Here are a few classic movie recommendations:\n- 🚀 *Interstellar*\n- 🍃 *Spirited Away*\n- 🕶️ *The Matrix*\n- 🍕 *Spider-Man: Into the Spider-Verse*"

    if any(word in text for word in ["music", "song", "band"]):
        return "🎵 Listening to good music is always great! What genre do you enjoy listening to?"

    if any(word in text for word in ["food", "hungry", "eat", "dinner", "lunch"]):
        return "🍕 Pizza, pasta, sushi, or tacos? You can never go wrong with a good meal!"

    if any(word in text for word in ["thank", "thanks", "thank you"]):
        return "You're very welcome! 😊 I'm always happy to chat."

    if any(word in text for word in ["bye", "goodbye", "see ya", "exit"]):
        return "Goodbye! 👋 Have a wonderful day ahead!"

    # 8. Help / Capabilities
    if any(word in text for word in ["help", "what can you do", "options", "menu"]):
        return """### 🤖 Here is what I can do:

1. 💬 **General Conversation**: Talk to me about daily life, movies, music, or food!
2. 👤 **Remember Info**: Say *"My name is Alex"* or *"My favorite color is green"*.
3. 🕒 **Time & Date**: Ask *"What time is it?"* or *"What is today's date?"*.
4. 🧮 **Calculator**: Type expressions like `25 * 4` or `150 + 350`.
5. 🎭 **Fun Features**: Ask me to *"Tell me a joke"*, *"Give me a quote"*, or *"Tell me a fun fact"*.
"""

    # 9. Smart Fallback for unrecognized inputs
    fallbacks = [
        f"That's interesting! Tell me more about **\"{user_input}\"**.",
        f"I hear you! How does **\"{user_input}\"** connect to what you're working on today?",
        "I'm a simple rule-based Python chatbot! Try asking me for the time, a joke, a calculation, or type **'help'** to see what I can do!"
    ]
    return random.choice(fallbacks)


# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROLS & STATISTICS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("---")
    
    st.markdown("### 💡 Quick Starters")
    if st.button("👋 Say Hello", use_container_width=True):
        st.session_state.pending_prompt = "Hello!"
    if st.button("😂 Tell me a Joke", use_container_width=True):
        st.session_state.pending_prompt = "Tell me a joke"
    if st.button("🕒 Check Time & Date", use_container_width=True):
        st.session_state.pending_prompt = "What time is it and what is today's date?"
    if st.button("🧮 Calculate 45 * 12", use_container_width=True):
        st.session_state.pending_prompt = "Calculate 45 * 12"
    if st.button("❓ What can you do?", use_container_width=True):
        st.session_state.pending_prompt = "help"
        
    st.markdown("---")
    
    st.markdown("### 📊 Chat Statistics")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-val">{st.session_state.message_count}</div>
            <div class="stat-lbl">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        saved_name = st.session_state.user_memory["name"] or "None"
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-val">{saved_name}</div>
            <div class="stat-lbl">Saved Name</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export Chat History
    chat_export = json.dumps(st.session_state.messages, indent=2)
    st.download_button(
        label="📥 Download Chat Log (JSON)",
        data=chat_export,
        file_name="chat_history.json",
        mime="application/json",
        use_container_width=True
    )
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Chat reset! How can I help you?",
                "timestamp": datetime.datetime.now().strftime("%H:%M")
            }
        ]
        st.session_state.message_count = 0
        st.rerun()

# -----------------------------------------------------------------------------
# 5. MAIN CHAT DISPLAY & INPUT INTERFACE
# -----------------------------------------------------------------------------
# Top Banner
st.markdown("""
<div class="chat-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>PyBuddy Chatbot</h1>
            <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 1rem;">
                A normal conversational chatbot built <strong>100% in pure Python</strong> with <strong>Streamlit</strong>.
            </p>
        </div>
        <div>
            <div class="status-badge">
                <div class="status-dot"></div> Online
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if "timestamp" in msg:
            st.caption(f"⏱️ {msg['timestamp']}")

# Determine Prompt Input
user_input = None
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
else:
    user_input = st.chat_input("Type a message... (e.g. 'Hello', 'Tell me a joke', 'My name is Alex')")

# Handle User Input
if user_input:
    now_str = datetime.datetime.now().strftime("%H:%M")
    
    # Add User message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": now_str
    })
    st.session_state.message_count += 1
    
    # Generate Bot Response using pure Python logic
    bot_reply = process_bot_response(user_input)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "timestamp": now_str
    })
    st.session_state.message_count += 1
    
    st.rerun()
