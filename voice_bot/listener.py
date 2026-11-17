"""
Speech Recognition (STT) Engine
-------------------------------
Captures live audio from your microphone and transcribes it into text
in real-time using Microsoft Azure Cognitive Services Speech SDK.
"""

import azure.cognitiveservices.speech as speechsdk


class SpeechListener:
    """
    Listens to microphone input and converts speech to text.
    Uses Azure's built-in Voice Activity Detection (VAD) to automatically
    detect when you start speaking and when you stop.
    """

    def __init__(
        self,
        azure_key: str | None = None,
        azure_region: str | None = None,
        language: str = "en-US",
    ):
        self.language = language
        self.available = False
        self.recognizer = None

        if azure_key and azure_key.strip():
            try:
                speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
                speech_config.speech_recognition_language = language

                # Voice Activity Detection tuning
                # Initial silence: how long to wait before user speaks (in ms)
                speech_config.set_property(
                    speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "8000"
                )
                # End silence: how much pause indicates user finished their sentence (in ms)
                speech_config.set_property(
                    speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "1200"
                )

                # Connect to default hardware microphone
                audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
                self.recognizer = speechsdk.SpeechRecognizer(
                    speech_config=speech_config, audio_config=audio_config
                )
                self.available = True
                print(f"[Speech Recognition] Active (Language: {language}, Hardware Mic)")
            except Exception as e:
                print(f"[Speech Recognition] Warning: Could not initialize microphone ({e})")
        else:
            print("[Speech Recognition] Disabled: No AZURE_SPEECH_KEY provided.")

    def listen(self) -> str | None:
        """
        Actively listens to the microphone until the user finishes speaking.
        Returns the recognized text string, or None if no speech was detected.
        """
        if not self.available or not self.recognizer:
            return None

        print("\n🎤 Listening... (Speak into your microphone)", flush=True)
        try:
            result = self.recognizer.recognize_once_async().get()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = result.text.strip()
                if text:
                    print(f"You (Voice): {text}")
                    return text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                # No speech was detected (silence or background noise)
                return None
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    print(f"\n[STT Error]: {cancellation.error_details}")
                return None
        except Exception as e:
            print(f"\n[STT Exception]: {e}")
            return None

        return None

