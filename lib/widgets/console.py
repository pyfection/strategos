

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label


class Console(BoxLayout):
    PROMPT = '>>> '
    HELP_TEXT = """
        Following commands are available:
        {commands}
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.commands = {
            'help': self.help
        }
        self.history = []
        self.results = []
        self.current = None

        self._scroll = ScrollView()
        self.past = BoxLayout()
        self.input = TextInput(text=self.PROMPT, multiline=False, height=30, size_hint_y=None)

        self._scroll.add_widget(self.past)
        self.add_widget(self._scroll)
        self.add_widget(self.input)

        self.input.bind(on_text_validate=self._on_text_validate)

    def _on_text_validate(self, inst):
        self.add_history(inst.text)
        command = inst.text[len(self.PROMPT):]
        command, *args = command.split()
        self.execute_command(command, *args)
        inst.text = self.PROMPT

    def add_history(self, text):
        label = Label(text=text)
        self.history.append(label)
        self.past.add_widget(label)

    def add_result(self, text):
        label = Label(text=text)
        self.results.append(label)
        self.past.add_widget(label)

    def execute_command(self, command, *args):
        try:
            command = self.commands[command]
        except KeyError:
            self.add_result(f"ERROR: command {command} is not valid")
            return
        command(*args)

    def help(self, command=None):
        if not command:
            text = self.HELP_TEXT.format(
                commands='\n'.join(self.commands.keys())
            )
            self.add_result(text)
            return
        try:
            command = self.commands[command]
        except KeyError:
            self.add_result(f"ERROR: command {command} is not valid")
        self.add_result(command.__doc__)
