

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


kv = """
<Console>:
    size_hint: (None, None)
    size: (500, 500)
    orientation: 'vertical'
    canvas:
        Color:
            rgba: 0, 0, 0, .5
        Rectangle:
            size: self.size
            pos: self.pos
    ScrollView:
        BoxLayout:
            id: history
            orientation: 'vertical'
    TextInput:
        id: input
        text: root.PROMPT
        multiline: False
        size_hint_y: None
        height: 30
"""

Builder.load_string(kv)


class Console(BoxLayout):
    PROMPT = '>>> '
    HELP_TEXT = """Following commands are available:{commands}"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.commands = {
            'help': self.help
        }
        self.history = []
        self.results = []
        self.current = None

        self.ids.input.bind(on_text_validate=self._on_text_validate)

    def _on_text_validate(self, inst):
        def _refocus(dt):
            inst.focus = True
        self.add_history(inst.text)
        command = inst.text[len(self.PROMPT):]
        command, *args = command.split()
        self.execute_command(command, *args)
        inst.text = self.PROMPT
        Clock.schedule_once(_refocus)

    def _add_history_label(self, text):
        def _on_size(inst, size):
            inst.size = size

        label = Label(text=text, size_hint=(None, None))
        label.bind(texture_size=_on_size)
        label.size = label.texture_size
        self.ids.history.add_widget(label)
        return label

    def add_history(self, text):
        label = self._add_history_label(text)
        self.history.append(label)

    def add_result(self, text):
        label = self._add_history_label(text)
        self.results.append(label)

    def execute_command(self, command, *args):
        try:
            command = self.commands[command]
        except KeyError:
            self.add_result(f"ERROR: command {command} is not valid")
            return
        try:
            command(*args)
        except Exception as e:
            self.add_result(str(e))

    def help(self, command=None):
        if not command:
            text = self.HELP_TEXT.format(
                commands='\n    '.join([''] + list(self.commands.keys()))
            )
            self.add_result(text)
            return
        try:
            command = self.commands[command]
        except KeyError:
            self.add_result(f"ERROR: command {command} is not valid")
        self.add_result(command.__doc__)
