"""
Configuration & Environment Setup
----------------------------------
Loads API keys from .env and validates them.
"""

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# 1. Google Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY or GOOGLE_API_KEY.strip() == "":
    raise ValueError(
        "❌ Error: GOOGLE_API_KEY was not found in your .env file!\n"
        "Please add: GOOGLE_API_KEY=your_key_here to .env before starting."
    )

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# 2. Microsoft Azure Speech Configuration (Student Account)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "centralindia")

# 3. Default Voice Output Settings (TTS)
DEFAULT_VOICE = "de-DE-SeraphinaMultilingualNeural"  # Seraphina Multilingual Neural Voice
DEFAULT_STYLE = None                                 # Natural multilingual tone (or "whispering" for Sara)

# 4. Default Speech Recognition Settings (STT)
SPEECH_RECOGNITION_LANGUAGE = "en-US"  # Options: "en-US", "en-IN", "de-DE", "hi-IN", etc.
