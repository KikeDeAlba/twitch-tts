from gtts import gTTS
import subprocess
import twitchio
from dotenv import load_dotenv
import time
import os

load_dotenv()

def init():
    print("Starting bot...")

    typing = True
    channels = []

    while typing:
        channel = input("Enter the channel name you want to join: ")
        channels.append(channel)
        typing = input("Do you want to add another channel? (y/n) ") == 'y'

        lang=input("Enter the language you want the bot to speak in: ")

    print("Bot will join the following channels: ", channels)

    bot = TwitchBot(
        channels=channels,
        lang=lang
    )

    print("Bot started.")
    bot.run()

class AudioPlayer:
    def await_play_audio(self, file_path):
        duration = self.get_duration(file_path)
        subprocess.Popen(["vlc", '--one-instance', file_path])
        print("Audio playback finished.")
        time.sleep(duration)

    def get_duration(self, file_path):
        duration = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path])
        return float(duration.decode("utf-8").strip())

    def text_to_speech(cls, text: str, lang='en'):
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save("tts.mp3")
        cls.await_play_audio("tts.mp3")

class TwitchBot(twitchio.Client):
    def __init__(self, channels: list[str] = [], lang='en'):
        super().__init__(
            token=os.getenv('TWITCH_TOKEN'),
            initial_channels=channels
        )
        self.lang = lang
        self.audio_player = AudioPlayer()

    def __delete_urls_from_message__(self, message):
        return ' '.join(filter(lambda x: 'http' not in x, message.split()))

    async def event_message(self, message):
        message.content = self.__delete_urls_from_message__(message.content)
        self.audio_player.text_to_speech(message.content, lang=self.lang)

if __name__ == '__main__':
    init()