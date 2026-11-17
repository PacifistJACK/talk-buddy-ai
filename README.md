# Talk Buddy AI 🎙️

An ultra-low latency real-time voice-to-voice conversational assistant powered by **Google Gemini 3.6 Flash** and **Microsoft Azure Speech Services**.

Talk Buddy AI listens through your microphone, reasons with tool-calling intelligence, and speaks back naturally in real time with human-like prosody and emotional expression.

> [!NOTE]
> **Project Status: In Active Progress 🚧**
> This project is continuously evolving. Core voice-to-voice conversation, tool calling, and streaming pipelines are functional, with more capabilities, integrations, and optimizations actively being added.

---

## Key Features

- **True Voice-to-Voice Conversation**:
  - **Speech-to-Text (STT)**: Uses Azure Speech SDK to listen to your default hardware microphone with automatic Voice Activity Detection (VAD).
  - **Text-to-Speech (TTS)**: Speaks back in real-time through your hardware speakers using neural voices.
  - **Hybrid Input**: Speak directly into your microphone or type in the console whenever you prefer.
- **Gemini 3.6 Flash + LangChain**:
  - Modular `create_agent` tool-calling architecture.
  - Automatic retry protection against temporary Google `503 UNAVAILABLE` spikes without crashing.
- **Acoustic Sound Effects Awareness**:
  - Talk Buddy AI expressively uses natural human vocalizations (`"hahaha"`, `"hmm..."`, `"phew!"`, `"whoa!"`, `"aww..."`, `"oops!"`).
- **Clause-Level Sub-Sentence Streaming Chunker**:
  - Dispatches complete natural sentences to the voice engine immediately, delivering smooth prosody and sub-second response times.
- **External Tools Included**:
  - Live weather forecasts via Open-Meteo.
  - Live news headlines via Google News RSS.

---

## Quickstart

### 1. Clone & Set Up Virtual Environment

```powershell
git clone <your-repo-url>
cd "talk-buddy-ai"

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```powershell
cp .env.example .env
```

Open `.env` and configure your API keys:

```env
# Required for LangChain Agent:
GOOGLE_API_KEY=your_google_gemini_api_key

# (Optional) For Azure Student Account credits & low-latency STT/TTS:
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=centralindia
```

> **Note**: If `AZURE_SPEECH_KEY` is omitted, Talk Buddy AI smoothly falls back to free Microsoft Edge Neural voices!

### 3. Run Talk Buddy AI

```powershell
python main.py
```
*(Or `python -m voice_bot.main`)*

---

## Project Structure

```
talk-buddy-ai/
│
├── main.py                    # Root entry point
├── pyproject.toml             # Project package configuration & dependencies
├── README.md                  # Project documentation
├── .env.example               # Template environment configuration
├── .gitignore                 # Protects keys, environments, and cache
│
└── voice_bot/                 # Core modular package
    ├── __init__.py            # Package exports
    ├── config.py              # Central settings & API validation
    ├── tools.py               # LangChain @tool definitions (weather, news)
    ├── chunker.py             # RealTimeClauseChunker (sub-sentence streaming)
    ├── voice_engine.py        # MicrosoftVoiceEngine (Azure TTS + SSML)
    ├── listener.py            # SpeechListener (Microphone STT with VAD)
    ├── agent.py               # LangChain Agent definition (Gemini 3.6 Flash)
    └── main.py                # Main conversation coordinator loop
```

---

## Available Neural Voices

You can switch the default voice in [`voice_bot/config.py`](voice_bot/config.py):
- `de-DE-SeraphinaMultilingualNeural` (Seraphina Multilingual Neural — Default)
- `en-US-SaraNeural` (Sara Neural — supports styles: `whispering`, `cheerful`, `excited`, `sad`)
- `en-US-JennyNeural` (Jenny Neural — supports styles: `whisper`, `chat`, `cheerful`, `friendly`)
- `en-US-GuyNeural` (Guy Neural — natural conversational male)
- `en-IN-NeerjaNeural` / `en-IN-PrabhatNeural` (Indian English voices)

---

## 🚧 Roadmap & Upcoming Functionality

Talk Buddy AI is actively being developed. Upcoming enhancements in the pipeline:
- [ ] **Wake-Word Detection**: Hands-free always-on voice trigger (e.g., "Hey Buddy").
- [ ] **Persistent Memory**: Retaining multi-turn conversation context across sessions.
- [ ] **Interactive Web UI**: Modern browser interface with live audio waveform visualizers.
- [ ] **Dynamic Style Switching**: Automatically switching voice emotion/style in real time based on the topic.
- [ ] **Extended Tool Suite**: Web search, calendar management, and desktop system tasks.
