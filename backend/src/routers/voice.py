"""
Voice Commands API Router

Provides voice-to-text and voice command processing endpoints.
Supports English and Urdu languages.
"""

import os
from typing import Literal

from fastapi import APIRouter, File, HTTPException, UploadFile
from openai import OpenAI
from pydantic import BaseModel

from ..agents.skills import SkillOrchestrator

router = APIRouter(prefix="/voice", tags=["Voice"])

# Initialize
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
orchestrator = SkillOrchestrator()


class TranscriptionResponse(BaseModel):
    """Response from transcription."""

    text: str
    language: str
    confidence: float | None = None


class VoiceCommandResponse(BaseModel):
    """Response from voice command processing."""

    transcription: str
    language: str
    intent: str | None = None
    response: str
    action_taken: dict | None = None


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: Literal["en", "ur", "auto"] = "auto",
) -> TranscriptionResponse:
    """
    Transcribe audio file to text using OpenAI Whisper.

    Supports:
    - English (en)
    - Urdu (ur)
    - Auto-detect (auto)

    Accepted formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
    """
    # Validate file type
    allowed_types = [
        "audio/mpeg",
        "audio/mp3",
        "audio/mp4",
        "audio/m4a",
        "audio/wav",
        "audio/webm",
        "audio/ogg",
    ]

    if audio.content_type and audio.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio format. Allowed: mp3, mp4, m4a, wav, webm, ogg",
        )

    try:
        # Read audio content
        content = await audio.read()

        # Create a file-like object for OpenAI
        audio_file = (audio.filename or "audio.webm", content, audio.content_type)

        # Transcribe with Whisper
        transcription_params = {
            "model": "whisper-1",
            "file": audio_file,
            "response_format": "json",
        }

        # Set language if specified
        if language != "auto":
            transcription_params["language"] = language

        response = client.audio.transcriptions.create(**transcription_params)

        # Detect language from response if auto
        detected_language = language
        if language == "auto":
            # Simple heuristic: check for Urdu characters
            if any("\u0600" <= char <= "\u06ff" for char in response.text):
                detected_language = "ur"
            else:
                detected_language = "en"

        return TranscriptionResponse(
            text=response.text,
            language=detected_language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}",
        )


@router.post("/command", response_model=VoiceCommandResponse)
async def process_voice_command(
    audio: UploadFile = File(...),
    user_id: str = "default",
    language: Literal["en", "ur", "auto"] = "auto",
) -> VoiceCommandResponse:
    """
    Process a voice command: transcribe and execute.

    This endpoint:
    1. Transcribes the audio to text
    2. Parses the text to understand intent
    3. Executes the appropriate action
    4. Returns the result

    Supports natural language commands in English and Urdu like:
    - "Add a task to buy groceries" / "گروسری خریدنے کا کام شامل کریں"
    - "Show my tasks" / "میرے کام دکھائیں"
    - "Mark task 3 as complete" / "کام 3 کو مکمل کریں"
    """
    # First, transcribe
    transcription_result = await transcribe_audio(audio, language)

    text = transcription_result.text
    detected_lang = transcription_result.language

    if not text.strip():
        return VoiceCommandResponse(
            transcription="",
            language=detected_lang,
            response="No speech detected"
            if detected_lang == "en"
            else "کوئی آواز نہیں سنی گئی",
        )

    try:
        # Process with NLP skill
        result = await orchestrator.process_natural_language(
            text=text,
            context={"user_id": user_id},
            language=detected_lang,
        )

        parsed_data = result.data.get("parsed", {}) if result.data else {}
        intent = parsed_data.get("intent", "other")

        # Generate response message
        if detected_lang == "ur":
            response_msg = parsed_data.get("suggested_response_ur") or parsed_data.get(
                "suggested_response", ""
            )
        else:
            response_msg = parsed_data.get("suggested_response", "")

        if not response_msg:
            response_msg = (
                "Command received" if detected_lang == "en" else "کمانڈ موصول ہوئی"
            )

        return VoiceCommandResponse(
            transcription=text,
            language=detected_lang,
            intent=intent,
            response=response_msg,
            action_taken=parsed_data.get("extracted_data"),
        )

    except Exception as e:
        error_msg = f"Processing failed: {str(e)}"
        return VoiceCommandResponse(
            transcription=text,
            language=detected_lang,
            response=error_msg
            if detected_lang == "en"
            else f"پروسیسنگ ناکام: {str(e)}",
        )


@router.post("/text-to-speech")
async def text_to_speech(
    text: str,
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "nova",
    speed: float = 1.0,
):
    """
    Convert text to speech using OpenAI TTS.

    Returns audio/mpeg stream.

    Available voices:
    - alloy: Neutral
    - echo: Male
    - fable: British
    - onyx: Deep male
    - nova: Female (default, works well with Urdu)
    - shimmer: Soft female
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    if speed < 0.25 or speed > 4.0:
        raise HTTPException(
            status_code=400, detail="Speed must be between 0.25 and 4.0"
        )

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=speed,
        )

        # Stream the audio response
        from fastapi.responses import StreamingResponse

        return StreamingResponse(
            response.iter_bytes(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3",
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text-to-speech failed: {str(e)}",
        )
