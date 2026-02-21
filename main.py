import os
from google.cloud import texttospeech
from google.cloud import speech
import io


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_experimental_service_acct.json"


def text_to_speech(article_text, output_path='output.mp3', language_code='en-US', voice_name='en-US-Standard-C', speaking_rate=1.0):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=article_text)

    # Select the language and desired voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response to the output file.
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to "{output_path}"')

def audio_transcribe_with_word_timestamps(audio_file_path, transcript_text, language_code="en-US", sample_rate_hz=44100):
    """
    Transcribe an MP3 file, returning word-level time offsets as spoken.
    Args:
        audio_file_path (str): Path to the speech audio file (MP3 format).
        transcript_text (str): The expected transcript text (not explicitly used for forced alignment, see note below).
        language_code (str): Language code, e.g., 'en-US'.
        sample_rate_hz (int): Sample rate of the audio file (44100 typical for MP3).
    Returns:
        list of dict: Each dict contains the recognized transcript and word timing.
    """
    client = speech.SpeechClient()

    # Load MP3 data
    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    # Recognition configuration
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code,
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    results = []

    for result in response.results:
        alternative = result.alternatives[0]
        words = []
        for word_info in alternative.words:
            words.append({
                "word": word_info.word,
                "start": word_info.start_time.total_seconds(),
                "end": word_info.end_time.total_seconds()
            })
        results.append({"transcript": alternative.transcript, "words": words})

    return results

def main():
    article = """Your article text goes here. Provide me your text. You can provide any long or short text."""
    text_to_speech(article, output_path='article_audio.mp3')
    transcribe = audio_transcribe_with_word_timestamps('article_audio.mp3', article)
    with open('trascribe.csv', 'w') as f:
        for result in transcribe:
            f.write(f"transcript,{result.get('transcript')},words,{result.get('words')}\n")

if __name__ == "__main__":
    # main()
    article = """Your article text goes here. Provide me your text. You can provide any long or short text."""
    transcribe = audio_transcribe_with_word_timestamps('article_audio.mp3', article)
    with open('trascribe.csv', 'w') as f:
        for result in transcribe:
            f.write(f"transcript,{result.get('transcript')},words,{result.get('words')}\n")
