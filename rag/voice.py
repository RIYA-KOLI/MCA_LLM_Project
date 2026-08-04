from gtts import gTTS
import tempfile


def speak(text):
    """
    Convert text to speech and return the mp3 filename.
    """

    tts = gTTS(
        text=text,
        lang="en"
    )

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp.name)

    return temp.name