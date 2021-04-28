from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, ThreeLineAvatarListItem, ImageLeftWidget

from src.data_provider import get_json_books
from src.books import Book


Builder.load_file('templates/ui.kv')


class BookItem(ThreeLineAvatarListItem):
    def __init__(self, book, *args, **kwargs):
        super().__init__(
            *args,
            text=book.title,
            secondary_text=book.subtitle,
            tertiary_text=book.price,
            **kwargs
        )
        image = ImageLeftWidget(source=book.image_path)
        self.add_widget(image)


class BooksList(MDList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        json_books = get_json_books()
        for json_book in json_books:
            book = Book.init_from_dict(json_book)
            list_item_widget = BookItem(book)
            self.add_widget(list_item_widget)


class UI(MDBoxLayout):
    pass
