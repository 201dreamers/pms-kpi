import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.imagelist import SmartTile
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.filemanager import MDFileManager

from config import Config
from src.images_provider import ImagesProvider


Builder.load_file(f"{Config.TEMPLATES_DIR}/imagecollectiontab.kv")


class ImageCell(SmartTile):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_color = (0, 0, 0, 0)

class ImageGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (dp(2), dp(2))
        self.spacing = dp(4)

    def get_free_cell(self):
        for image in self.images:
            if not image.source:
                return image
        return

    def add_image_cells(self):
        for image in self.images:
            self.add_widget(image)


class ThreeHorizontalImagesGrid(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 1
        self.size_hint = (1, 0.083)
        self.images = (ImageCell(), ImageCell(), ImageCell())
        self.add_image_cells()


class ThreeImagesBlockGrid(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.size_hint = (1, 0.16)


class TwoVerticalImagesGrid(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint = (0.33, 0.083)
        self.images = (ImageCell(), ImageCell())
        self.add_image_cells()


class BigImageGrid(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        self.size_hint = (0.66, 0.16)
        self.images = (ImageCell(),)
        self.add_image_cells()


class BlockOfImages(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_grid = None

        self._first_row_grid = None
        self._middle_block_grid = None
        self._middle_small_images_grid = None
        self._middle_big_image_grid = None
        self._last_row_grid = None

        self.cols = 1
        self.size_hint = (1, 1.1)

        self.images = []
        self._make_new_grid()

    def _to_next_grid(self):
        if self._current_grid == self._first_row_grid:
            self._current_grid = self._middle_small_images_grid
        elif self._current_grid == self._middle_small_images_grid:
            self._current_grid = self._middle_big_image_grid
        elif self._current_grid == self._middle_big_image_grid:
            self._current_grid = self._last_row_grid
        elif self._current_grid == self._last_row_grid:
            self._make_new_grid()

    def get_free_cell(self):
        if self._last_row_grid.children[0].source:
            return
        image = self._current_grid.get_free_cell()
        if not image:
            self._to_next_grid()
            image = self._current_grid.get_free_cell()
        return image

    def _make_new_grid(self):
        self._first_row_grid = ThreeHorizontalImagesGrid()
        self._last_row_grid = ThreeHorizontalImagesGrid()

        self._middle_block_grid = ThreeImagesBlockGrid()
        self._middle_small_images_grid = TwoVerticalImagesGrid()
        self._middle_big_image_grid = BigImageGrid()

        self._middle_block_grid.add_widget(self._middle_small_images_grid)
        self._middle_block_grid.add_widget(self._middle_big_image_grid)

        self.add_widget(self._first_row_grid)
        self.add_widget(self._middle_block_grid)
        self.add_widget(self._last_row_grid)

        self._current_grid = self._first_row_grid


class ImageGridBuilder(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocks = [BlockOfImages(), BlockOfImages(), BlockOfImages()]
        self._idx = 0
        self._current_block = self.blocks[self._idx]
        self.cols = 1
        self.size_hint = (1, 3.3)

        for block in self.blocks:
            self.add_widget(block)

    def _to_next_block(self):
        self._idx += 1
        self._current_block = self.blocks[self._idx]

    def add_image(self, source):
        image = self._current_block.get_free_cell()
        if not image:
            self._to_next_block()
            image = self._current_block.get_free_cell()
        image.source = source


class ImageChooser(MDFileManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.preview = True
        self.exit_manager = self.exit
        self.external_storage = os.getenv('EXTERNAL_STORAGE')
        self.images_folder = os.path.join(self.external_storage, "Pictures")

    def select_path(self, path):
        ImageCollectionTab.image_collection.builder.add_image(path)
        self.exit()

    def exit(self, *args):
        self.close()

    def open(self):
        self.show(self.images_folder)


class ImageCollection(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols=1, **kwargs)

        self.__next_image_index = 0

        self.add_image_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.load_images
        )

        self.scroll_view = ScrollView(size_hint=(1, 1))

        self.builder = ImageGridBuilder()

        self.scroll_view.add_widget(self.builder)
        self.add_widget(self.scroll_view)
        self.add_widget(self.add_image_button)

    def load_images(self, touch):
        # ImageCollectionTab.image_chooser.open()
        self.images_links = ImagesProvider.load_images()
        for link in self.images_links:
            self.builder.add_image(source=link)



class ImageCollectionTab(MDBottomNavigationItem):
    """Tab that contains personal information."""

    image_chooser = None
    image_collection = None
    x_size = None

    def __init__(self, **kwargs):
        super().__init__(name="img_collection", text="Images",
                         icon="image-frame", **kwargs)

        ImageCollectionTab.x_size = self.size[0]
        ImageCollectionTab.image_collection = ImageCollection()
        ImageCollectionTab.image_chooser = ImageChooser()

        self.add_widget(ImageCollectionTab.image_collection)
