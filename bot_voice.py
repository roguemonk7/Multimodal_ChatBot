import requests
import os

ELEVENLABS_API_KEY = "sk_22ae3ab298c013bb1d7aa349849f178595651c2e3cd97444"  # Ensure your API key is correct
VOICE_ID = "ALgMVHkymAnEbk2koqfD"  # Replace with the ID of the voice you want to use

# Function to convert text to speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_22050_32"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": input_text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        # Save the audio content to the specified file path
        with open(output_filepath, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to {output_filepath}")
    else:
        print(f"Error in TTS request: {response.status_code} - {response.text}")
