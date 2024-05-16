from gtts import gTTS
import subprocess
import twitchio
from dotenv import load_dotenv
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
    def __init__(self):
        self.is_reading = False

    @classmethod
    def await_play_audio(self, file_path):
        process = subprocess.Popen(["vlc", "--intf", "dummy", "--play-and-exit", file_path])
        process.wait()  # Espera a que el proceso de reproducción termine
        print("Audio playback finished.")

    @classmethod
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

    def __delete_urls_from_message__(self, message):
        return ' '.join(filter(lambda x: 'http' not in x, message.split()))

    async def event_message(self, message):
        message.content = self.__delete_urls_from_message__(message.content)
        AudioPlayer.text_to_speech(message.content, lang=self.lang)

if __name__ == '__main__':
    init()