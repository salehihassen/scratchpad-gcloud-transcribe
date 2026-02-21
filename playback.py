import time
import threading
import simpleaudio as sa

SYNC_OFFSET = 0

def play_audio(path):
    wave_obj = sa.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until playback is finished

def highlight_words_in_sync(words):
    start_time = time.perf_counter()
    for w in words:
        adjusted_start = w['start'] - SYNC_OFFSET
        now = time.perf_counter()
        delay = adjusted_start - (now - start_time)
        if delay > 0:
            time.sleep(delay)
        print(f"Speaking: {w['word']}")
    print("Done highlighting words.")

def sync_audio_with_words(audio_path, words):
    audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
    audio_thread.start()
    highlight_words_in_sync(words)
    audio_thread.join()

# Example word timing data
words = [
    {'word': 'your', 'start': 0.0, 'end': 0.4},
    {'word': 'article', 'start': 0.4, 'end': 0.6},
    {'word': 'text', 'start': 0.6, 'end': 1.0},
    {'word': 'goes', 'start': 1.0, 'end': 1.2},
    {'word': 'here', 'start': 1.2, 'end': 1.5},
    {'word': 'provide', 'start': 1.5, 'end': 2.4},
    {'word': 'me', 'start': 2.4, 'end': 2.6},
    {'word': 'your', 'start': 2.6, 'end': 2.9},
    {'word': 'text', 'start': 2.9, 'end': 3.1},
    {'word': 'you', 'start': 3.1, 'end': 3.6},
    {'word': 'can', 'start': 3.6, 'end': 3.7},
    {'word': 'provide', 'start': 3.7, 'end': 3.9},
    {'word': 'any', 'start': 3.9, 'end': 4.4},
    {'word': 'long', 'start': 4.4, 'end': 4.7},
    {'word': 'or', 'start': 4.7, 'end': 5.0},
    {'word': 'short', 'start': 5.0, 'end': 5.2},
    {'word': 'text', 'start': 5.2, 'end': 5.6}
]

# Note: simpleaudio requires .wav files, so if your audio is mp3 you'll need to convert it first to wav

# Run sync demo - make sure your audio is wav format
sync_audio_with_words('article_audio.wav', words)
