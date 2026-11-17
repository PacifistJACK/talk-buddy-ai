# Interactive Voice-to-Voice Agent (LangChain + Microsoft Speech)

An ultra-low latency real-time voice-to-voice assistant powered by **Google Gemini 3.6 Flash** and **Microsoft Azure Speech Services**.

## Features

- **True Voice-to-Voice Conversation**:
  - **Speech-to-Text (STT)**: Uses Azure Speech SDK to listen to your default hardware microphone with automatic Voice Activity Detection (VAD).
  - **Text-to-Speech (TTS)**: Speaks back in real-time through your hardware speakers using neural voices.
  - **Hybrid Input**: Speak directly into your microphone or type in the console whenever you prefer.
- **Gemini 3.6 Flash + LangChain**:
  - Follows modular `create_agent` tool-calling syntax.
  - Automatically retries temporary Google `503 UNAVAILABLE` spikes without crashing.
- **Acoustic Sound Effects Awareness**:
  - The agent knows how to expressively use natural human vocalizations (`"hahaha"`, `"hmm..."`, `"phew!"`, `"whoa!"`, `"aww..."`).
- **Clause-Level Sub-Sentence Streaming Chunker**:
  - Dispatches complete natural sentences to the voice engine immediately, delivering smooth prosody and sub-second response times.

---

## Configuration (`.env`)

Add the following to your [`.env`](.env) file:

```env
# Required for LangChain Agent:
GOOGLE_API_KEY=your_google_api_key

# (Optional) For Azure Student Credits:
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus
```

> **Note**: If you haven't created your Azure Speech resource yet, you can still run the bot immediately! It will automatically use the free Microsoft Edge Neural Speech engine.

---

## How to Run

```powershell
.\.venv\Scripts\python.exe voice_agent.py
```

---

## Available Neural Voices & Expressive Styles

The agent is currently configured to use **Seraphina Multilingual Neural (`de-DE-SeraphinaMultilingualNeural`)**.
As a multilingual neural voice, Seraphina can speak German, English, French, Spanish, Hindi, and more with natural fluency!

You can adjust `voice_name` and `style` in `MicrosoftVoiceEngine` inside [voice_agent.py](file:///d:/Antigravity%20projects/building%20interactive%20agent%20with%20langchain/voice_agent.py#L407) or [voice_bot/config.py](file:///d:/Antigravity%20projects/building%20interactive%20agent%20with%20langchain/voice_bot/config.py#L28):

```python
voice = MicrosoftVoiceEngine(
    voice_name="de-DE-SeraphinaMultilingualNeural",  # Seraphina Multilingual
    style=None,
    azure_key=azure_speech_key,
    azure_region=azure_speech_region,
)
```

Other popular voices you can switch between:
- `en-US-SaraNeural` (Supports style: `whispering`, `cheerful`, `excited`, `sad`)
- `en-US-JennyNeural` (Supports style: `whisper`, `chat`, `cheerful`, `excited`)
- `en-US-GuyNeural` (Natural conversational male)
- `en-IN-NeerjaNeural` / `en-IN-PrabhatNeural` (Indian English voices)
