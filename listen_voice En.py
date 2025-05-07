import pyaudio
import wave
from google.cloud import speech

def record_audio(file_name="audio.wav", duration=5, rate=44100, chunk=1024, channels=1):
    # Initialize the PyAudio object
    audio = pyaudio.PyAudio()
    # Open a new audio stream for recording
    stream = audio.open(format=pyaudio.paInt16, channels=channels,
                        rate=rate, input=True, frames_per_buffer=chunk)
    print("Recording... Speak now!")
    frames = []

    # Read audio data in chunks for the specified duration
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(file_name, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))

    print(f"Saved recording to {file_name}")

def transcribe_audio(file_path, language_code="en-US"):
    # Initialize Google Speech-to-Text client
    client = speech.SpeechClient()
    # Load the audio file content
    with open(file_path, "rb") as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())
    # Set recognition configuration, including language
    config = speech.RecognitionConfig(language_code=language_code)
    # Perform speech recognition
    response = client.recognize(config=config, audio=audio)
    # Print the transcribed text
    for result in response.results:
        print("Transcript:", result.alternatives[0].transcript)

if __name__ == "__main__":
    file_name = "audio.wav"
    record_audio(file_name, duration=5)  # Record audio for 5 seconds
    transcribe_audio(file_name)         # Transcribe the recorded audio
