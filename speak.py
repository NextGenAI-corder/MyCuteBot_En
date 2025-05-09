from google.cloud import texttospeech
from playsound import playsound

def synthesize_text(text, output_file="output.mp3"):
    # Create a client for the Google Text-to-Speech API
    client = texttospeech.TextToSpeechClient()

    # Set the input text to synthesize
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice parameters: language and gender
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the audio configuration: output format as MP3
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the audio content to an output file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Saved synthesized audio to {output_file}")

    # Play the audio file using playsound
    playsound(output_file)

# Example usage
if __name__ == "__main__":
    synthesize_text("Hello, how are you?")
