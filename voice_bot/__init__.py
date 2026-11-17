"""
Voice Bot Package
-----------------
A modular real-time conversational voice assistant using:
  - LangChain + Google Gemini 3.6 Flash
  - Microsoft Azure Speech SDK:
    * Speech Recognition (Microphone STT)
    * Neural Voice Synthesis (Speaker TTS)
  - Real-Time Clause Streaming
"""

from voice_bot.agent import create_voice_agent
from voice_bot.voice_engine import MicrosoftVoiceEngine
from voice_bot.chunker import RealTimeClauseChunker
from voice_bot.listener import SpeechListener
from voice_bot.config import (
    GOOGLE_API_KEY,
    AZURE_SPEECH_KEY,
    AZURE_SPEECH_REGION,
    DEFAULT_VOICE,
    DEFAULT_STYLE,
    SPEECH_RECOGNITION_LANGUAGE,
)

__all__ = [
    "create_voice_agent",
    "MicrosoftVoiceEngine",
    "RealTimeClauseChunker",
    "SpeechListener",
    "GOOGLE_API_KEY",
    "AZURE_SPEECH_KEY",
    "AZURE_SPEECH_REGION",
    "DEFAULT_VOICE",
    "DEFAULT_STYLE",
    "SPEECH_RECOGNITION_LANGUAGE",
]
