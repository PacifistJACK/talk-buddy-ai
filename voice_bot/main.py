"""
Voice Bot - Main Chat Loop
--------------------------
Interactive real-time chat interface connecting:
  1. LangChain Gemini 3.8 Flash Streaming
  2. RealTimeClauseChunker (Early clause detection)
  3. Microsoft Azure Speech Engine (Sara Neural in Whisper Mode)
"""

import sys
import os

# Ensure project root is in sys.path when running this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_core.messages import HumanMessage, AIMessage

from voice_bot.config import (
    AZURE_SPEECH_KEY,
    AZURE_SPEECH_REGION,
    DEFAULT_VOICE,
    DEFAULT_STYLE,
    SPEECH_RECOGNITION_LANGUAGE,
)
from voice_bot.agent import create_voice_agent
from voice_bot.voice_engine import MicrosoftVoiceEngine
from voice_bot.chunker import RealTimeClauseChunker
from voice_bot.listener import SpeechListener


def run():
    # 1. Initialize Voice Output Engine (TTS)
    voice = MicrosoftVoiceEngine(
        voice_name=DEFAULT_VOICE,
        style=DEFAULT_STYLE,
        azure_key=AZURE_SPEECH_KEY,
        azure_region=AZURE_SPEECH_REGION,
    )

    # 2. Initialize Speech Recognition Engine (STT)
    listener = SpeechListener(
        azure_key=AZURE_SPEECH_KEY,
        azure_region=AZURE_SPEECH_REGION,
        language=SPEECH_RECOGNITION_LANGUAGE,
    )

    # 3. Initialize LangChain Agent (Gemini 3.6 Flash)
    agent = create_voice_agent()

    # 4. Print Startup Banner
    print("\n" + "=" * 60)
    print("🎙️  Talk Buddy AI (Gemini 3.6 + Azure Speech)")
    print("=" * 60)
    print("✓ LLM Model         : gemini-3.6-flash (Google API Key verified)")
    if voice.mode == "AZURE_SDK":
        style_desc = f" [Style: {voice.style.upper()}]" if voice.style else ""
        print(f"✓ Speech Output     : Microsoft Azure Speech SDK (Region: {AZURE_SPEECH_REGION})")
        print(f"✓ Voice Model       : {voice.voice_name}{style_desc} (Azure Student Credits)")
    else:
        print(f"✓ Speech Output     : Microsoft Edge Neural (Zero-config high-fidelity)")
        print(f"✓ Voice Model       : {voice.voice_name}")
    if listener.available:
        print(f"✓ Speech Recognition: Active (Mic: Default, Lang: {SPEECH_RECOGNITION_LANGUAGE})")
    else:
        print("✓ Speech Recognition: Keyboard mode only")
    print("=" * 60)
    print("Speak naturally into your microphone or type your message.")
    print("Say 'goodbye' or type 'quit' to end the conversation.\n")

    chat_history = []

    try:
        while True:
            user_input = None

            # 1. Try speech recognition first if available
            if listener.available:
                user_input = listener.listen()

            # 2. If silence or no microphone input, provide keyboard prompt
            if not user_input:
                user_input = input("You (Type message or press Enter to speak): ").strip()
                if not user_input and listener.available:
                    # User pressed Enter to re-activate microphone
                    continue

            if not user_input:
                continue

            # Check for exit commands (spoken or typed)
            clean_input = user_input.lower().strip(".!? ")
            if clean_input in {"quit", "exit", "goodbye", "bye", "stop"}:
                print("\nGoodbye! Have a great day!")
                voice.enqueue_phrase("Goodbye! Have a wonderful day!")
                voice.end_turn()
                voice.wait_until_done()
                break

            chat_history.append(HumanMessage(content=user_input))

            # Stream token-by-token with automatic retry for temporary 503 / rate spikes
            max_retries = 3
            success = False

            for attempt in range(max_retries):
                print("Agent: ", end="", flush=True)
                full_response = ""
                chunker = RealTimeClauseChunker()

                try:
                    for chunk, _ in agent.stream({"messages": chat_history}, stream_mode="messages"):
                        if chunk.content:
                            if hasattr(chunk, "text") and chunk.text:
                                text = chunk.text
                            elif isinstance(chunk.content, str):
                                text = chunk.content
                            elif isinstance(chunk.content, list):
                                text = "".join(
                                    part["text"] for part in chunk.content
                                    if isinstance(part, dict) and "text" in part
                                )
                            else:
                                text = ""

                            # 1. Print immediately to terminal
                            print(text, end="", flush=True)
                            full_response += text

                            # 2. Check for clause breaks (speaks immediately without waiting for full sentences)
                            for ready_phrase in chunker.add_token(text):
                                voice.enqueue_phrase(ready_phrase)

                    # Flush any remaining tokens at the end of the turn
                    for rem_phrase in chunker.flush():
                        voice.enqueue_phrase(rem_phrase)

                    print("\n")
                    success = True
                    break

                except Exception as e:
                    err_str = str(e)
                    if "503" in err_str or "UNAVAILABLE" in err_str or "high demand" in err_str:
                        if attempt < max_retries - 1:
                            print(f"\n[Google API Notice] High server traffic (503). Retrying in 2s (attempt {attempt + 1}/{max_retries})...")
                            import time
                            time.sleep(2)
                            continue
                    print(f"\n[Notice] Temporary Google API service error: {err_str[:120]}...")
                    print("Please try your question again in a moment.\n")
                    # Remove the failed human message from history so state remains clean
                    chat_history.pop()
                    break

            if success:
                # Signal end of turn to speech queue
                voice.end_turn()

                # Record bot's response in chat history
                chat_history.append(AIMessage(content=full_response))

                # Wait for speech playback to finish before prompting for next user input
                voice.wait_until_done()

    finally:
        voice.shutdown()


if __name__ == "__main__":
    run()

