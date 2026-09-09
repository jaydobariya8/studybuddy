# StudyBuddy 📚

A study-tutor chatbot built in one Python file with **Streamlit** and **Gemini**.
Built live at the NextGen Chatbot Arena session, Silver Oak University.

Ask it anything you're studying. It explains simply, gives one example, and checks you understood.
Turn on **Quiz mode** and it tests you with MCQs.

## How it works

```
You type in the browser  →  app.py (Streamlit)  →  Gemini API  →  answer back in the browser
```

Three boxes. Every chatbot you will ever build is these three boxes.

- **UI** - Streamlit draws the chat box and the message bubbles.
- **Backend** - `app.py` holds the API key, the system prompt, and the chat history.
- **LLM API** - Gemini receives text, returns text. It knows nothing about your app.

## Run it on your laptop

**1. Get the code**

```bash
git clone https://github.com/jaydobariya8/studybuddy.git
cd studybuddy
```

**2. Create a virtual environment and install the three libraries**

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Get a free Gemini API key**

Go to https://aistudio.google.com/apikey → **Create API key** → copy it.

**4. Put the key in a `.env` file**

```bash
cp .env.example .env             # Windows: copy .env.example .env
```

Open `.env` and replace `paste-your-key-here` with your key.
`.env` is in `.gitignore` - it never goes to GitHub. Your key is a password. Treat it like one.

**5. Test the API with one call**

```bash
python hello_gemini.py
```

You should see Gemini explain gravity. That was an API call: request out, response back.

**6. Run the chatbot**

```bash
streamlit run app.py
```

Your browser opens at http://localhost:8501.

## Put it on the internet (free)

1. Push this folder to your own GitHub repo. Check `.env` is **not** in it (`git status` should never list it).
2. Go to https://share.streamlit.io → **New app** → pick your repo, branch `main`, file `app.py`.
3. **Advanced settings → Secrets** → paste `GEMINI_API_KEY = "your-key"`. This is the cloud's `.env`.
4. **Deploy**. Two minutes later you have a public URL. Send it to anyone.

## Make it yours

Everything that makes this *StudyBuddy* instead of a generic bot is in one place: `SYSTEM_PROMPT` in `app.py`.
It follows **Role · Task · Context · Rules**. Change those four and you have a different chatbot -
a fitness coach, a cooking helper, a customer-support bot. Same code, different prompt.

## If something breaks

| You see | It means | Fix |
|---|---|---|
| `No API key found` | `.env` missing or empty | Step 4 again |
| `Gemini rejected the API key` | Typo in the key | Copy it again from AI Studio |
| `Too many requests` | Free-tier limit hit | Wait a minute |
| `ModuleNotFoundError` | venv not activated | `source .venv/bin/activate` |
