# 💬 PyBuddy - Pure Python Streamlit Chatbot

A friendly, normal conversational chatbot built **100% in pure Python** using **Streamlit** for the frontend user interface.

---

## 🎯 What is this Project?

This is a **Rule-Based Conversational Chatbot** created for a Python course assignment.

- **No AI / LLM APIs Required**: Built entirely using pure Python logic, string pattern matching, regular expressions (`re`), conditional flow (`if/elif/else`), and state dictionary memory.
- **Frontend UI with Streamlit**: Streamlit automatically turns Python code into an interactive web interface with chat bubbles, quick prompt buttons, statistics cards, and log downloads.

---

## 🌟 Chatbot Features

1. 💬 **Everyday Chit-Chat**: Responds to greetings, questions about how it's doing, movies, music, food, travel, and general conversation.
2. 👤 **Memory Storage**: Tell it your name (*"My name is Alex"*) or favorite color (*"My favorite color is blue"*), and it remembers your details during the session!
3. 🕒 **Live Time & Date**: Ask *"What time is it?"* or *"What is today's date?"*.
4. 🧮 **Built-in Calculator**: Perform instant calculations like `25 * 4` or `150 + 350`.
5. 🎭 **Fun Extras**: Ask for jokes, inspirational quotes, and fun trivia facts.
6. 📊 **Session Analytics & Export**: View total message count and download chat history as JSON.

---

## 🚀 How to Run this Project on Your Computer (Step-by-Step)

### Step 1: Open Terminal on Your Mac
Press `Cmd + Space` to open Spotlight, type **Terminal**, and press `Enter`.

### Step 2: Navigate to Project Folder
Run this command in Terminal:
```bash
cd "/Users/abhijithr/Desktop/chatbot python"
```

### Step 3: Run the Streamlit Chatbot App
Run this command to start the chatbot server:
```bash
/Users/abhijithr/Library/Python/3.9/bin/streamlit run app.py
```
*(Or simply `streamlit run app.py` if Streamlit is in your system PATH)*

### Step 4: Open in Web Browser
Streamlit will automatically open your default browser at:
```text
http://localhost:8501
```

---

## 📂 Project Structure

```text
chatbot python/
├── app.py              # Main Python application (Pattern matching logic + Streamlit UI)
├── requirements.txt    # Required Python packages (streamlit, pandas)
└── README.md           # Instructions on how to run & project overview
```

---

## 🎓 Tutor Presentation Explanation

When demonstrating this project to your tutor:
1. **Explain the Pure Python Logic**: Point out `process_bot_response()` in `app.py`, which processes input text using Python regular expressions (`re`), string methods, and conditionals—without relying on any paid black-box AI services.
2. **Explain Streamlit State**: Show how `st.session_state` preserves chat history and stores user memory (like user's name) across browser rerenders.
3. **Showcase Interactive UI**: Demonstrate quick starter buttons in the sidebar, chat message avatars, calculations, and JSON export.
