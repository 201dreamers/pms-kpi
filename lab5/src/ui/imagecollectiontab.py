from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.imagelist import SmartTile
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton
# from kivymd.uix.boxlayout import MDBoxLayout
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/imagecollectiontab.kv")


class StandardImage(SmartTile):

    def __init__(self, **kwargs):
        super().__init__(height=dp(240), **kwargs)
        self.minimum_height = self.height
        self.box_color


class ImageAdderScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDGridLayout(cols=1)

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["plus", self.add_image]]

        self.scroll_view = ScrollView()

        layout.add_widget(toolbar)
        layout.add_widget(self.scroll_view)
        self.add_widget(layout)

    def load_content(self):
        self.scroll_view.clear_widgets()
        layout = MDGridLayout(cols=1)
        self.scroll_view.add_widget(layout)

    def go_back(self, touch):
        self.scroll_view.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(ImageCollectionTab.screens["image_collection"])

    def add_image(self, touch):
        pass
        # book = Book(
        #     title=self.title_input.text,
        #     subtitle=self.subtitle_input.text,
        #     price=self.price_input.text
        # )
        # BooksTab.screens["books_list"].books.append(book)
        # books_list = BooksTab.screens["books_list"].books
        # BooksTab.screens["books_list"].load_books_list(books_list)
        # self.go_back(touch)


class ImageCollectionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.images = (
            StandardImage(),
            StandardImage(),
            StandardImage(),
            StandardImage(),
            StandardImage(),
            StandardImage(),
            StandardImage(),
            StandardImage(),
            StandardImage(),
        )

        layout = MDGridLayout(cols=1)

        # toolbar = MDToolbar(type="top")
        # toolbar.right_action_items = [["plus", self.add_image]]

        add_image_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_image_adder_screen
        )

        self.scroll_view = ScrollView()

        self.load_images()

        layout.add_widget(self.scroll_view)
        layout.add_widget(add_image_button)
        self.add_widget(layout)

    def open_image_adder_screen(self, touch):
        ImageCollectionTab.screens["image_adder"].load_content()
        ImageCollectionTab.screen_manager.transition.direction = "left"
        ImageCollectionTab.screen_manager.switch_to(
            ImageCollectionTab.screens["image_adder"]
        )

    def load_images(self):
        self.scroll_view.clear_widgets()

        layout = MDGridLayout(cols=1, padding=(dp(4), dp(4)), spacing=dp(4))
        first_row_layout = MDGridLayout(
            cols=3,
            rows=1,
            padding=(dp(4), dp(4)),
            spacing=dp(4)
        )
        last_row_layout = MDGridLayout(
            cols=3,
            rows=1,
            padding=(dp(4), dp(4)),
            spacing=dp(4)
        )
        middle_block_layout = MDGridLayout(
            cols=2,
            rows=1,
            padding=(dp(4), dp(4)),
            spacing=dp(4)
        )
        inner_small_images_layout = MDGridLayout(
            cols=1,
            rows=2,
            padding=(dp(4), dp(4)),
            spacing=(dp(4))
        )
        inner_big_image_layout = MDGridLayout(
            cols=1,
            rows=1,
            padding=(dp(4), dp(4)),
            spacing=(dp(4))
        )

        first_row_layout.add_widget(self.images[0])
        first_row_layout.add_widget(self.images[1])
        first_row_layout.add_widget(self.images[2])

        inner_small_images_layout.add_widget(self.images[3])
        inner_small_images_layout.add_widget(self.images[4])
        inner_big_image_layout.add_widget(self.images[5])

        middle_block_layout.add_widget(inner_small_images_layout)
        middle_block_layout.add_widget(inner_big_image_layout)

        last_row_layout.add_widget(self.images[6])
        last_row_layout.add_widget(self.images[7])
        last_row_layout.add_widget(self.images[8])

        layout.add_widget(first_row_layout)
        layout.add_widget(middle_block_layout)
        layout.add_widget(last_row_layout)

        self.scroll_view.add_widget(layout)


class ImageCollectionTab(MDBottomNavigationItem):
    """Tab that contains personal information."""

    screen_manager = None
    screens = None

    def __init__(self, **kwargs):
        super().__init__(name="img_collection", text="Images",
                         icon="image-frame", **kwargs)

        ImageCollectionTab.screen_manager = ScreenManager()
        ImageCollectionTab.screens = {
            "image_collection": ImageCollectionScreen(name="image_collection"),
            "image_adder": ImageAdderScreen(name="image_adder")
        }

        for screen in self.screens.values():
            ImageCollectionTab.screen_manager.add_widget(screen)

        self.add_widget(ImageCollectionTab.screen_manager)
