# Multimodal_ChatBot

This is Multimodal Chatbot build on Groq,ELEvenLabs and Streamlit

# Functionality

The Bot will receive image.
Then it will analyse the image using LLAMA/Vision model and generate the analysis.
Using STT the user query will be transcribed using Whisper and will be passed with system prompt to chat model.
The chat model will generate response which will be ported to Elevenlabs configuration to generate TTS.


