# Aboutme: Resume Website with an AI Chatbot

A personal resume website with a built-in chatbot that answers questions about my skills, experience and services in **Persian and English**.

<!-- Add a screenshot or GIF here: ![Chatbot demo](docs/demo.png) -->

## How it works

1. Every question is converted to a sentence embedding with a multilingual SentenceTransformer model (`paraphrase-multilingual-MiniLM-L12-v2`).
2. A small Keras neural network classifies the embedding into an intent (skills, experience, contact, ...).
3. The bot replies with a predefined answer in the same language as the question.
4. Low-confidence or off-topic questions get a polite "I can't answer that" reply, and asking "why?" explains that the information was never defined for the bot.

## Tech stack

- **Backend:** Python, FastAPI, Uvicorn
- **ML:** Keras / TensorFlow, sentence-transformers
- **Frontend:** HTML, CSS, JavaScript (vanilla)

## Project structure

```
aboutme/
├── index.html
├── html/chatbot.html      # chat page
├── css/  js/              # frontend assets
├── json/resume.json       # intents: patterns and responses
├── model/                 # trained Keras model
├── pkl/classes.pkl        # intent labels
└── python/
    ├── agent.py           # trains the classifier
    ├── chatbot.py         # loads the model and picks replies
    └── main.py            # FastAPI app (API + serves the site)
```

## Run locally

```bash
# 1. create and activate a virtual environment
python -m venv env
env\Scripts\activate          # Windows
# source env/bin/activate     # Linux / macOS

# 2. install dependencies
pip install -r requirements.txt

# 3. (optional) retrain the model after editing json/resume.json
cd python
python agent.py

# 4. start the server
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/** (or `/html/chatbot.html`) in your browser.
The first run downloads the SentenceTransformer model (a few hundred MB).

## API

`POST /chat`

```json
{ "message": "What are your skills?" }
```

Response:

```json
{ "reply": "...", "intent": "skills", "confidence": 0.93 }
```

Interactive docs: **http://127.0.0.1:8000/docs**

## Customizing the bot

Edit `json/resume.json` (add intents, patterns and responses), then run `python agent.py` again to retrain.
Use the same `MODEL_NAME` in `agent.py` and `chatbot.py`.
