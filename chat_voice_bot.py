import os
import time  # Add this for sleep
import sounddevice as sd
import wavio
from openai import OpenAI
from google.cloud import speech, texttospeech
from playsound import playsound

# Initialize the OpenAI client using API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_audio(file_name="audio.wav", duration=5, fs=44100):
    # Optional sleep to ensure microphone is ready
    time.sleep(1)  # Wait 1 second before starting recording
    print("Recording... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    wavio.write(file_name, recording, fs, sampwidth=2)
    print(f"Saved recording to {file_name}")
    # Optional sleep after saving if needed (e.g., time.sleep(0.5))

def listen():
    # Record and transcribe user speech
    record_audio()
    speech_client = speech.SpeechClient()
    with open("audio.wav", "rb") as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())
    config = speech.RecognitionConfig(language_code="en-US")
    response = speech_client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript

def ask_chatgpt(text):
    # Send user input to ChatGPT and get the response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}],
        max_tokens=20
    )
    return response.choices[0].message.content

def speak(text, output_file="output.mp3"):
    # Delete old file if exists to avoid permission error
    if os.path.exists(output_file):
        os.remove(output_file)

    # Synthesize text to speech and play it back
    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Saved synthesized audio to {output_file}")
    playsound(output_file)

def talk_with_bot():
    # Main loop for conversation with the bot
    while True:
        print("Say something (type 'exit' to quit):")
        question = listen()
        print(f"You: {question}")
        if any(word in question.lower() for word in ["goodbye", "bye", "see you"]):
            print("Goodbye!")
            speak("Goodbye!")
            break
        answer = ask_chatgpt(question)
        print(f"Bot: {answer}")
        speak(answer)

if __name__ == "__main__":
    talk_with_bot()
