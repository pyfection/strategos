

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from visual.main_menu import MainMenu


class GameApp(App):
    title = "Strategos"
    screenmanager = None
    main_menu = None

    def build(self):
        self.screenmanager = ScreenManager()
        self.main_menu = MainMenu()

        self.screenmanager.add_widget(self.main_menu)
        return self.screenmanager


if __name__ == '__main__':
    GameApp().run()
