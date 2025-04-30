import os
import streamlit as st
from io import BytesIO
import tempfile
from brain import encode_image, analyse_image_with_query
from human_voice import record_and_transcribe
from bot_voice import text_to_speech_with_elevenlabs
from autoplay import autoplay_audio

system_prompt = """
You are a professional football manager. You are shown an image of a football player. Based only on the image you are suppose to genartae brief summary about professional player shown in the image.
If you dont know just say no i have no infomration on him.
"""

def process_inputs(audio_filepath, image_filepath):
    try:
        print("Starting processing...")

        # Step 1: Transcribe the audio input
        speech_to_text_output = record_and_transcribe(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            stt_model="whisper-large-v3"
        )
        print("Transcription done.")

        # Step 2: Analyze the image (if provided) and query the assistant
        if image_filepath:
            encoded_img = encode_image(image_filepath)
            print("Image encoded.")
            assistant_response = analyse_image_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encoded_img,
                model="meta-llama/llama-4-maverick-17b-128e-instruct"
            )
        else:
            assistant_response = "No image for me to analyze"

        print(f"Assistant response: {assistant_response}")

        # Log the TTS input (to ensure it's the correct response)
        print(f"Text to Speech input: {assistant_response}")

        # Step 3: Convert assistant response to speech
        # Use a temporary file for the TTS output
        output_filepath = "assistant_response_audio.mp3"
        
        # Generate the audio with TTS
        text_to_speech_with_elevenlabs(input_text=assistant_response, output_filepath=output_filepath)

        print(f"TTS done. Audio saved to {output_filepath}. Returning results.")
        
        return speech_to_text_output, assistant_response, output_filepath
    
    except Exception as e:
        print(f"❌ Error in process_inputs: {str(e)}")
        return "Error", str(e), None

def main():
    st.set_page_config(page_title="Football Manager AI", layout="centered")
    st.title("⚽ Football Manager AI Assistant")
    st.write("Upload a football player's image and click **Start Recording** to ask a question.")

    # Upload image
    image_file = st.file_uploader("Upload Player Image", type=["jpg", "jpeg", "png"])

    if image_file:
        st.image(image_file, caption="Uploaded Player Image", use_column_width=True)

    # Start interaction
    if st.button("🎙️ Start Recording"):
        if image_file:
            # Save uploaded image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
                temp_image.write(image_file.read())
                image_filepath = temp_image.name

            with st.spinner("🎤 Speak now... Listening..."):
                # Process image and voice
                stt, response, audio_output = process_inputs(None, image_filepath)

            # Check if processing succeeded
            if stt != "Error" and audio_output:
                st.success(" Transcription completed!")

                # Show transcribed speech
                st.subheader("You said:")
                st.code(stt, language="")

                # Show assistant's response
                st.subheader("Assistant Response:")
                st.text_area("Answer", response, height=80)

                # Play audio
                autoplay_audio(audio_output)
            else:
                st.error(f"Something went wrong during processing:\n\n{response}")
        else:
            st.warning("Please upload a player image first.")


if __name__ == "__main__":
    main()

