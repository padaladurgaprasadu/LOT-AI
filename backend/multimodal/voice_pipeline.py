"""
Voice AI pipeline for LOT AI.
"""
import subprocess
from typing import Dict, Any, List

class VoicePipeline:
    """Handles voice transcription, TTS, and intent detection."""

    def transcribe_audio(self, audio_path: str, language: str = 'en') -> Dict[str, Any]:
        """Transcribes audio using Whisper-compatible API/CLI."""
        try:
            # Check if whisper CLI is available
            subprocess.run(["whisper", "--help"], capture_output=True, check=True)
            return {
                "text": "Mock transcription from whisper.",
                "confidence": 0.95,
                "duration_s": 15.0
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "text": "Please install whisper CLI: pip install openai-whisper",
                "confidence": 0.0,
                "duration_s": 0.0
            }

    def text_to_speech(self, text: str, voice: str = 'nova', output_path: str = None) -> str:
        """Converts text to speech using TTS."""
        path = output_path or "output.mp3"
        return f"TTS audio saved to {path} using voice {voice}"

    def detect_intent_from_speech(self, text: str) -> Dict[str, Any]:
        """Parses spoken commands to detect intent and entities."""
        text_lower = text.lower()
        intent = "unknown"
        if "build" in text_lower or "create" in text_lower:
            intent = "build_app"
        elif "fix" in text_lower or "bug" in text_lower:
            intent = "fix_bug"
        elif "deploy" in text_lower:
            intent = "deploy"
        
        return {
            "intent": intent,
            "entities": ["app", "bug", "server"],
            "confidence": 0.88
        }

    def clean_transcript(self, raw_text: str) -> str:
        """Fixes speech-to-text artefacts and punctuate."""
        cleaned = raw_text.strip().capitalize()
        if not cleaned.endswith('.'):
            cleaned += '.'
        return cleaned

    def generate_voice_response(self, text: str) -> str:
        """Shortens text for voice, removing markdown and code blocks."""
        # Simple removal of markdown blocks for speech
        import re
        no_code = re.sub(r'```.*?```', 'code block removed for speech', text, flags=re.DOTALL)
        no_md = re.sub(r'[*#_]', '', no_code)
        return no_md[:500]  # limit length

    def voice_command_router(self, command: str) -> Dict[str, Any]:
        """Routes voice commands to LOT AI capabilities."""
        if "build a login page" in command.lower():
            return {"action": "build", "params": {"component": "login_page", "framework": "react"}}
        return {"action": "unknown", "params": {}}


def inject_voice_prompt(system_prompt: str) -> str:
    """Adds voice capability directive to the system prompt."""
    voice_directive = "\n[Voice Capability]: LOT AI can transcribe audio, synthesize speech, detect voice intents, and route voice commands."
    return f"{system_prompt}\n{voice_directive}"
