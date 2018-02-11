

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from visual.main_menu import MainMenu
from visual.game_setup import GameSetup


class GameApp(App):
    title = "Strategos"
    screenmanager = None
    main_menu = None
    game_setup = None

    def build(self):
        self.screenmanager = ScreenManager()
        self.main_menu = MainMenu()
        self.game_setup = GameSetup()

        self.screenmanager.add_widget(self.main_menu)
        self.screenmanager.add_widget(self.game_setup)
        return self.screenmanager


if __name__ == '__main__':
    GameApp().run()
