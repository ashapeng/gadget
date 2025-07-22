import json
from typing import Dict
from transformers import pipeline
import torch

# Initialize the pipelines (they will download models on first use)
sentiment_analyzer = pipeline("sentiment-analysis")
emotion_detector = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
zero_shot = pipeline("zero-shot-classification")

def get_emotion(text: str) -> Dict:
    """Get detailed emotion analysis."""
    result = emotion_detector(text)[0]
    return {
        "emotion": result["label"],
        "confidence": round(result["score"], 3)
    }

def get_underlying_meaning(text: str) -> str:
    """Analyze the underlying meaning/intent of the text."""
    candidate_meanings = [
        "asking for information",
        "expressing agreement",
        "expressing disagreement",
        "showing enthusiasm",
        "showing concern",
        "making a suggestion",
        "expressing frustration"
    ]
    result = zero_shot(text, candidate_meanings)
    top_meaning = result["labels"][0]
    return f"{top_meaning} ({round(result['scores'][0] * 100)}% confidence)"

def suggest_response(text: str, mood: str, underlying_meaning: str) -> str:
    """Generate a response suggestion based on analysis."""
    if "frustration" in underlying_meaning.lower():
        return "Acknowledge their frustration and offer specific help or solutions."
    elif "concern" in underlying_meaning.lower():
        return "Show empathy and ask clarifying questions to better understand their concerns."
    elif "enthusiasm" in underlying_meaning.lower():
        return "Match their positive energy and build upon their enthusiasm."
    elif "asking for information" in underlying_meaning.lower():
        return "Provide clear, concise information and ask if they need more details."
    elif mood == "NEGATIVE":
        return "Respond with empathy and understanding, then offer constructive solutions."
    else:
        return "Maintain the positive tone and continue building rapport."

def analyze_conversation(text: str, audio_features: Dict = None) -> Dict:
    """
    Analyze the given text and audio features to extract mood, tone, and suggest a response.
    """
    # Get sentiment (positive/negative)
    sentiment = sentiment_analyzer(text)[0]
    mood = sentiment["label"]
    
    # Get specific emotion
    emotion_data = get_emotion(text)
    tone = emotion_data["emotion"]
    
    # Get underlying meaning
    underlying_meaning = get_underlying_meaning(text)
    
    # Generate response suggestion
    suggestion = suggest_response(text, mood, underlying_meaning)
    
    return {
        "mood": mood,
        "tone": tone,
        "underlying_meaning": underlying_meaning,
        "suggestion": suggestion
    }
