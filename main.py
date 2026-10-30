
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

from jnius import autoclass, PythonJavaClass
from jnius import java_method


# Android Java classes
TextToSpeech = autoclass(
    'android.speech.tts.TextToSpeech'
)

Locale = autoclass('java.util.Locale')

PythonActivity = autoclass(
    'org.renpy.android.PythonActivity'
)


# TTS initialization listener
class TTSListener(PythonJavaClass):

    __javainterfaces__ = [
        'android/speech/tts/TextToSpeech$OnInitListener'
    ]

    __javacontext__ = 'app'

    def __init__(self, app):
        super().__init__()
        self.app = app

    @java_method('(I)V')
    def onInit(self, status):

        if status == TextToSpeech.SUCCESS:

            self.app.tts.setLanguage(Locale.US)
            self.app.tts.setSpeechRate(0.88)
            self.app.tts.setPitch(0.85)

            self.app.tts_ready = True

            Clock.schedule_once(
                self.app.voice_ready, 0
            )


# Main JARVIS application
class JarvisApp(App):

    def build(self):

        self.tts = None
        self.tts_ready = False
        self.listener = None

        layout = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=25
        )

        self.title_label = Label(
            text='J.A.R.V.I.S',
            font_size='38sp',
            color=(0, 0.8, 1, 1)
        )

        self.status_label = Label(
            text='INITIALIZING SYSTEM...',
            font_size='16sp'
        )

        self.voice_button = Button(
            text='TEST JARVIS VOICE',
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0, 0.35, 0.65, 1)
        )

        self.voice_button.bind(
            on_release=self.test_voice
        )

        layout.add_widget(self.title_label)
        layout.add_widget(self.status_label)
        layout.add_widget(self.voice_button)

        # Initialize Android TTS
        try:

            activity = PythonActivity.mActivity

            self.listener = TTSListener(self)

            self.tts = TextToSpeech(
                activity,
                self.listener
            )

        except Exception as error:

            self.status_label.text = (
                'TTS ERROR: ' + str(error)
            )

        return layout

    def voice_ready(self, dt):

        self.status_label.text = 'SYSTEM ONLINE'

        self.speak(
            'Good afternoon. '
            'JARVIS is now online.'
        )

    def speak(self, text):

        if self.tts_ready:

            self.tts.speak(
                text,
                TextToSpeech.QUEUE_FLUSH,
                None
            )

        else:

            self.status_label.text = (
                'VOICE ENGINE NOT READY'
            )

    def test_voice(self, instance):

        self.speak(
            'Hello. I am JARVIS. '
            'All systems are operational.'
        )

    def on_stop(self):

        if self.tts is not None:
            self.tts.stop()
            self.tts.shutdown()


if __name__ == '__main__':
    JarvisApp().run()
  
