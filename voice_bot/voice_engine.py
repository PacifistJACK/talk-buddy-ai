"""
Microsoft Voice Engine
----------------------
Handles speech synthesis using:
  1. Azure Cognitive Services Speech SDK (Azure Student Credits)
     * Supports SSML expressive styles (e.g., whisper mode)
     * Plays directly to hardware speakers with < 150ms latency
  2. Microsoft Edge Neural Speech (Free zero-config fallback via edge-tts)
"""

import os
import re
import html
import queue
import threading
import time
import tempfile
import asyncio

# Audio libraries
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import edge_tts

try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SDK_AVAILABLE = True
except ImportError:
    AZURE_SDK_AVAILABLE = False


class MicrosoftVoiceEngine:
    def __init__(
        self,
        voice_name: str = "de-DE-SeraphinaMultilingualNeural",
        style: str | None = None,
        azure_key: str | None = None,
        azure_region: str | None = None,
    ):
        self.voice_name = voice_name

        # Normalize whisper style: SaraNeural requires "whispering", JennyNeural requires "whisper"
        if style:
            if "Sara" in voice_name and style.lower() in {"whisper", "whispering"}:
                self.style = "whispering"
            elif "Jenny" in voice_name and style.lower() in {"whisper", "whispering"}:
                self.style = "whispering"
            else:
                self.style = style
        else:
            self.style = None

        self.speech_queue: queue.Queue = queue.Queue()
        self.is_running = True

        # Determine mode: Azure SDK vs Edge-TTS fallback
        if AZURE_SDK_AVAILABLE and azure_key and azure_key.strip():
            self.mode = "AZURE_SDK"
            self.speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
            self.speech_config.speech_synthesis_voice_name = self.voice_name
            # Output directly to the default audio speakers
            self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            self.synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, audio_config=self.audio_config
            )
            style_label = f" (Style: {style.upper()})" if style else ""
            print(f"[Voice Engine] Connected to Azure Speech SDK (Region: {azure_region}, Voice: {voice_name}{style_label})")
        else:
            self.mode = "EDGE_TTS"
            pygame.mixer.init()
            print(f"[Voice Engine] Using Microsoft Edge Neural Speech (Voice: {voice_name})")
            if not azure_key:
                print("  💡 Tip: To use your Azure Student Credits, add AZURE_SPEECH_KEY & AZURE_SPEECH_REGION to .env")

        # Start background sequential worker thread
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()

    def _build_ssml(self, text: str) -> str:
        """Build SSML markup to apply styles like whisper mode."""
        safe_text = html.escape(text)
        if self.style:
            return (
                f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
                f'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n'
                f'    <voice name="{self.voice_name}">\n'
                f'        <mstts:express-as style="{self.style}">\n'
                f'            {safe_text}\n'
                f'        </mstts:express-as>\n'
                f'    </voice>\n'
                f'</speak>'
            )
        return (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">\n'
            f'    <voice name="{self.voice_name}">\n'
            f'        {safe_text}\n'
            f'    </voice>\n'
            f'</speak>'
        )

    def _speech_worker(self):
        """Worker thread that synthesizes and speaks queued text sequentially."""
        while self.is_running:
            try:
                item = self.speech_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if item is None:  # Sentinel marking end of agent turn
                self.speech_queue.task_done()
                continue

            clean_text = self._clean_for_speech(item)
            if not clean_text:
                self.speech_queue.task_done()
                continue

            try:
                if self.mode == "AZURE_SDK":
                    # Direct hardware speaker playback via SSML (< 150ms latency)
                    ssml = self._build_ssml(clean_text)
                    self.synthesizer.speak_ssml(ssml)
                else:
                    # Edge-TTS playback via pygame (< 300ms latency)
                    self._play_edge_tts(clean_text)
            except Exception as e:
                print(f"\n[Voice Warning]: {e}")

            self.speech_queue.task_done()

    def _play_edge_tts(self, text: str):
        """Synthesize and play audio chunk using Microsoft Edge Neural TTS."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
            temp_path = tf.name

        try:
            async def _generate():
                communicate = edge_tts.Communicate(text, self.voice_name)
                await communicate.save(temp_path)

            asyncio.run(_generate())

            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.is_running:
                time.sleep(0.05)
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            try:
                os.remove(temp_path)
            except OSError:
                pass

    @staticmethod
    def _clean_for_speech(text: str) -> str:
        """Strip markdown symbols and raw URLs so speech sounds natural."""
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`.*?`", "", text)
        text = re.sub(r"^[#*>\-\d\.]+\s+", "", text, flags=re.MULTILINE)
        text = text.replace("*", "").replace("_", "").replace("#", "")
        return text.strip()

    def enqueue_phrase(self, phrase: str):
        """Enqueue a phrase/clause for immediate speech synthesis."""
        if phrase.strip():
            self.speech_queue.put(phrase)

    def end_turn(self):
        """Signal that the agent has finished outputting this turn."""
        self.speech_queue.put(None)

    def wait_until_done(self):
        """Wait until speech playback finishes before accepting the next user input."""
        self.speech_queue.join()

    def shutdown(self):
        self.is_running = False

