"""Chatbot logic: load the model once, then answer messages.

Must match agent.py: sentence embeddings (normalized) -> Keras classifier.
"""
import json
import pickle
import random
import re
from pathlib import Path

import numpy as np
from keras.models import load_model
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent.parent
JSON_PATH = BASE / "json" / "resume.json"
CLASSES_PATH = BASE / "pkl" / "classes.pkl"
MODEL_PATH = BASE / "model" / "chatbot_model.keras"

# Multilingual (Persian + English). Must be IDENTICAL to MODEL_NAME in agent.py
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
THRESHOLD = 0.6  # below this confidence -> use the "noanswer" reply

# Loaded once when the server starts (not on every request)
with open(JSON_PATH, encoding="utf-8") as f:
    intents = json.load(f)
with open(CLASSES_PATH, "rb") as f:
    classes = pickle.load(f)

model = load_model(MODEL_PATH)
encoder = SentenceTransformer(MODEL_NAME)

intents_by_tag = {i["tag"]: i for i in intents["intents"]}


def is_persian(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF]", text))


def pick_response(tag: str, sentence: str) -> str:
    """Pick a response in the same language as the user's sentence."""
    responses = intents_by_tag[tag]["responses"]
    same_lang = [r for r in responses if is_persian(r) == is_persian(sentence)]
    return random.choice(same_lang or responses)


def predict_intent(sentence: str):
    """Return (tag, confidence) of the best intent."""
    vec = encoder.encode([sentence], normalize_embeddings=True)
    probs = model.predict(vec, verbose=0)[0]
    best = int(np.argmax(probs))
    return classes[best], float(probs[best])


def get_reply(sentence: str):
    """Return (reply, tag, confidence)."""
    tag, confidence = predict_intent(sentence)
    if tag == "noanswer" or confidence < THRESHOLD:
        return pick_response("noanswer", sentence), None, confidence
    return pick_response(tag, sentence), tag, confidence
