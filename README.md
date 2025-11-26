



# 🎩 AI Time Machine  
AI Time Machine is an interactive Pygame application where users can explore historical events through an AI persona called The Archivist.
It combines UX design, game-style UI, and LLM integration to deliver concise historical insights generated in real time.

---

## ✨ Features

- 🧠 **AI-generated summaries** (years, events, people, books, films, etc.)
- 🔮 **Custom AI persona** (“The Archivist”, a calm ancient philosopher)
- 🎨 **Pygame interface with polished UI**
- 📜 **Automatic word-wrapping for long text**
- 🖱️ **Scrollable content (Up/Down arrows)**
- 🎧 **Sound effects when “time traveling”**
- 🌌 **Semi-transparent background artwork**
- 🔐 **Environment-based API key (secure `.env`)**

---

## 📸 Screenshots

*(Replace these when you have final screenshots)*

### Main Interface
![TimeMachine Screenshot](bilder/screenshot_main.png)

### Example Query
![TimeMachine Query](bilder/screenshot_query.png)

---

## 🔧 Installation

### 1. Install **Python 3.11**
Required for full compatibility with Pygame and the OpenAI SDK.

Download:  
https://www.python.org/downloads/release/python-3110/

Make sure to check:



1. Install Python 3.11

Download Python 3.11 from the official site:

https://www.python.org/downloads/release/python-3110/

Make sure to check:

☑ Add Python to PATH

## 2 Clone the repository

git clone https://github.com/<your-username>/TimeMachine.git
cd TimeMachine


## 3 Create a virtual environment

python -m venv .venv

Activate it:

Windows PowerShell:
.\.venv\Scripts\Activate.ps1

macOS/Linux:
source .venv/bin/activate

## 4 Install dependencies

pip install -r requirements.txt

## 5 Add your API key

Create a .env file in the root folder:
OPENAI_API_KEY=your_api_key_here

## 6 Run the Time Machine

python timeMachine.py
