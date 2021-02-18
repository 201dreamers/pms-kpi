from kivy.lang import Builder
from kivymd.app import MDApp


class Lab1_1App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Hakman Dmytro IO-81"


if __name__ == "__main__":
    Lab1_1App().run()