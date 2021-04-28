from kivymd.app import MDApp

from src.ui import UI
from pprint import pprint


class Lab3App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Hakman Dmytro IO-81"

    def build(self):
        return UI()         


if __name__ == "__main__":
    Lab3App().run()
