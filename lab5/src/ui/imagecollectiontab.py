import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.imagelist import SmartTile
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/imagecollectiontab.kv")


class ImageCell(SmartTile):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_color = (0, 0, 0, 0)


class ImagesGrid(MDGridLayout):
    def __init__(self, scale=1, **kwargs):
        super().__init__(**kwargs)
        self.padding = (dp(2), dp(2))
        self.spacing = dp(4)


class ImageChooser(MDFileManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.exit_manager = self.exit
        self.preview = False
        self.external_storage = os.getenv('EXTERNAL_STORAGE')
        self.images_folder = f"{self.external_storage}/Pictures"

    def select_path(self, path):
        ImageCollectionTab.image_collection.new_image.source = path
        self.exit()
        toast("You have selected an image")

    def exit(self, *args):
        self.close()

    def open(self):
        toast(self.images_folder)
        self.show(self.images_folder)


class ImageCollection(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols=1, **kwargs)

        self.__next_image_index = 0
        self.images = (
            ImageCell(),
            ImageCell(),
            ImageCell(),
            ImageCell(),
            ImageCell(),
            ImageCell(),
            ImageCell(),
            ImageCell(),
            ImageCell(),
        )

        self.add_image_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_image_chooser
        )

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.layout = ImagesGrid(cols=1, size_hint=(1, 1.1))

        self.load_images()

        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)
        self.add_widget(self.add_image_button)

    @property
    def new_image(self):
        if self.__next_image_index > 8:
            self.__next_image_index = 0
        cell = self.images[self.__next_image_index]
        self.__next_image_index += 1
        return cell

    def open_image_chooser(self, touch):
        ImageCollectionTab.image_chooser.open()

    def load_images(self):
        self.layout.clear_widgets()

        first_row_layout = ImagesGrid(cols=3, rows=1, size_hint=(1, 0.25))
        last_row_layout = ImagesGrid(cols=3, rows=1, size_hint=(1, 0.25))
        middle_block_layout = ImagesGrid(cols=2, rows=1, size_hint=(1, 0.5))
        inner_small_images_layout = ImagesGrid(
            cols=1, rows=2, size_hint=(0.33, 1))
        inner_big_image_layout = ImagesGrid(
            cols=1, rows=1, scale=2, size_hint=(0.66, 1))

        first_row_layout.add_widget(self.images[0])
        first_row_layout.add_widget(self.images[1])
        first_row_layout.add_widget(self.images[2])

        inner_small_images_layout.add_widget(self.images[3])
        inner_big_image_layout.add_widget(self.images[4])
        inner_small_images_layout.add_widget(self.images[5])

        middle_block_layout.add_widget(inner_small_images_layout)
        middle_block_layout.add_widget(inner_big_image_layout)

        last_row_layout.add_widget(self.images[6])
        last_row_layout.add_widget(self.images[7])
        last_row_layout.add_widget(self.images[8])

        self.layout.add_widget(first_row_layout)
        self.layout.add_widget(middle_block_layout)
        self.layout.add_widget(last_row_layout)


class ImageCollectionTab(MDBottomNavigationItem):
    """Tab that contains personal information."""

    image_chooser = None
    image_collection = None
    x_size = None

    def __init__(self, **kwargs):
        super().__init__(name="img_collection", text="Images",
                         icon="image-frame", **kwargs)

        ImageCollectionTab.x_size = self.size[0]
        ImageCollectionTab.image_chooser = ImageChooser()
        ImageCollectionTab.image_collection = ImageCollection()

        self.add_widget(ImageCollectionTab.image_collection)
