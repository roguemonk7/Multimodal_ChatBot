import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq
import tempfile


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def record_and_transcribe(GROQ_API_KEY, stt_model, timeout=10, phrase_time_limit=10):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("🎙️ Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("🔴 Speak now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("✅ Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))

            # Export to temporary MP3 file (Groq requires file upload)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
                audio_segment.export(temp_mp3.name, format="mp3", bitrate="128k")
                logging.info(f"📤 Sending audio to Groq Whisper model...")

                # Transcribe using Groq
                client = Groq(api_key=GROQ_API_KEY)
                with open(temp_mp3.name, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model=stt_model,
                        file=audio_file,
                        language="en"
                    )

            logging.info(f"📝 Transcription: {transcription.text}")
            return transcription.text

    except Exception as e:
        logging.error(f"❌ Error: {e}")
        return ""

