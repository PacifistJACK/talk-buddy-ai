# Talk Buddy AI 🎙️

A high-performance, real-time voice-to-voice conversational AI agent engineered with **LangChain**, **Google Gemini 3.6 Flash**, and **Microsoft Azure Speech Services**.

Talk Buddy AI delivers sub-second conversational latency through streaming Speech-to-Text (STT), agentic tool orchestration, and expressive Neural Text-to-Speech (TTS) synthesis.

> [!NOTE]
> **Project Status: In Active Progress 🚧**
> This project is in active development. Core voice-to-voice pipelines, agentic tool calling, and streaming synthesis are operational, with multi-turn memory, wake-word detection, and web UI integrations currently underway.

---

## Key Features

- **End-to-End Voice-to-Voice Pipeline**:
  - **Speech-to-Text (STT)**: Real-time microphone capture via Azure Cognitive Services with hardware-level Voice Activity Detection (VAD) and automated silence trimming.
  - **Neural Text-to-Speech (TTS)**: Direct-to-speaker WASAPI streaming using multilingual neural models with customizable SSML expressive styles.
  - **Multimodal Hybrid Input**: Zero-friction transition between continuous hands-free voice conversation and keyboard input.
- **Agentic Reasoning & Tool Calling**:
  - **LangChain & Gemini 3.6 Flash**: Autonomous reasoning, schema-based parameter extraction, and dynamic tool execution.
  - **Fault-Tolerant Architecture**: Built-in exponential backoff retry guard to handle transient upstream API rate limits and 503 spikes without interruption.
- **Acoustic Prosody & Expressive Vocalizations**:
  - **Contextual Paralinguistics**: Generates natural non-verbal human reactions (`"hahaha"`, `"hmm..."`, `"phew!"`, `"whoa!"`, `"aww..."`) through phonetic neural modeling.
- **Sub-Sentence Real-Time Chunker**:
  - **Low-Latency Streaming**: Token-level sentence boundary parsing delivering sub-500ms Time-to-First-Audio (TTFA) while preserving melodic prosody.
- **Production Tool Integrations**:
  - **Telemetry Tool**: Real-time meteorological forecasting via Open-Meteo REST API.
  - **News Ingestion Tool**: Live global and local headline extraction via Google News XML feeds.

---

## Quickstart

### 1. Clone & Set Up Virtual Environment

```powershell
git clone https://github.com/PacifistJACK/talk-buddy-ai.git
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
