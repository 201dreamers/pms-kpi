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


class ThreeHorizontalImagesGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 1
        self.size_hint = (1, 0.25)
        self.padding = (dp(2), dp(2))
        self.spacing = dp(4)

    @property
    def has_free_cells(self):
        if len(self.cols) >= len(self.children):
            return False
        return True


class ThreeImagesBlockGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.size_hint = (1, 0.5)
        self.padding = (dp(2), dp(2))
        self.spacing = dp(4)


class TwoVerticalImagesGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint = (0.33, 1)
        self.padding = (dp(2), dp(2))
        self.spacing = dp(4)

    @property
    def has_free_cells(self):
        if len(self.rows) >= len(self.children):
            return False
        return True


class BigImageGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        self.size_hint = (0.66, 1)
        self.padding = (dp(2), dp(2))
        self.spacing = dp(4)

    @property
    def has_free_cells(self):
        if len(self.rows) >= len(self.children):
            return False
        return True


class ImageGridBuilder(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (1, 1.1)
        self._current_grid = None
        self.images = []
        self._to_next_grid()

    def _to_next_grid(self):
        if self._current_grid == self.first_row_grid:
            self._current_grid = self.middle_small_images_grid
        elif self._current_grid == self.middle_small_images_grid:
            self._current_grid = self.middle_big_image_grid
        elif self._current_grid == self.middle_big_image_grid:
            self._current_grid = self.last_row_grid
        else:
            self._make_new_grid()
            self._current_grid = self.first_row_grid

    def add_image(self, source):
        image = ImageCell(source=source)
        if not self._current_grid.has_free_cells:
            self._to_next_grid()
        self._current_grid.add_widget(image)

    def _make_new_grid(self):
        self.first_row_grid = ThreeHorizontalImagesGrid()
        self.last_row_grid = ThreeHorizontalImagesGrid()
        middle_block_grid = ThreeImagesBlockGrid()
        self.middle_small_images_grid = TwoVerticalImagesGrid()
        self.middle_big_image_grid = BigImageGrid()

        middle_block_grid.add_widget(self.middle_small_images_grid)
        middle_block_grid.add_widget(self.middle_big_image_grid)

        self.last_row_grid.add_widget(self.images[6])
        self.last_row_grid.add_widget(self.images[7])
        self.last_row_grid.add_widget(self.images[8])

        self.add_widget(self.first_row_grid)
        self.add_widget(middle_block_grid)
        self.add_widget(self.last_row_grid)


class ImageChooser(MDFileManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.exit_manager = self.exit
        self.preview = False
        self.external_storage = os.getenv('EXTERNAL_STORAGE')
        self.images_folder = f"{self.external_storage}/Pictures"

    def select_path(self, path):
        ImageCollectionTab.image_collection.builder.add_image(path)
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

        self.add_image_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_image_chooser
        )

        self.scroll_view = ScrollView(size_hint=(1, 1))

        self.builder = ImageGridBuilder()

        self.scroll_view.add_widget(self.builder)
        self.add_widget(self.scroll_view)
        self.add_widget(self.add_image_button)

    def open_image_chooser(self, touch):
        ImageCollectionTab.image_chooser.open()


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
