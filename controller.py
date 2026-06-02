from typing import Dict, List, Optional, Any, Callable
import math
import os

from model import Client, ClientCollection
from xml_handler import XMLHandler


class PaginationInfo:


    def __init__(self, total_items: int, total_pages: int,
                 current_page: int, page_size: int, items_on_page: int):
        self.total_items = total_items
        self.total_pages = total_pages
        self.current_page = current_page
        self.page_size = page_size
        self.items_on_page = items_on_page


class MainController:

    def __init__(self):
        self._collection = ClientCollection()
        self._display_list: List[Client] = []  # Текущий список для отображения
        self._current_page: int = 1
        self._page_size: int = 10
        self._current_file_path: Optional[str] = None

        # Callbacks для связи с View
        self._on_data_changed: Optional[Callable] = None
        self._on_pagination_changed: Optional[Callable[[PaginationInfo], None]] = None
        self._on_status_message: Optional[Callable[[str], None]] = None

    def set_view_callbacks(self, on_data_changed: Callable,
                           on_pagination_changed: Callable[[PaginationInfo], None],
                           on_status_message: Callable[[str], None]):
        self._on_data_changed = on_data_changed
        self._on_pagination_changed = on_pagination_changed
        self._on_status_message = on_status_message

    def _notify_data_changed(self):
        if self._on_data_changed:
            self._on_data_changed()

    def _notify_pagination_changed(self):
        if self._on_pagination_changed:
            info = self.get_pagination_info()
            self._on_pagination_changed(info)

    def _show_status(self, message: str):
        if self._on_status_message:
            self._on_status_message(message)



    def load_data(self, filepath: str) -> bool:
        """Загрузка данных из XML файла"""
        if not os.path.exists(filepath):
            self._show_status(f"Файл не найден: {filepath}")
            return False

        try:
            self._collection = XMLHandler.load_from_xml(filepath)
            self._current_file_path = filepath
            self._reset_display()
            self._show_status(f"Загружено {len(self._collection)} записей из {os.path.basename(filepath)}")
            return True
        except Exception as e:
            self._show_status(f"Ошибка загрузки: {e}")
            return False

    def save_data(self, filepath: str) -> bool:
        """Сохранение данных в XML файл"""
        try:
            success = XMLHandler.save_to_xml(self._collection, filepath)
            if success:
                self._current_file_path = filepath
                self._show_status(f"Данные сохранены в {os.path.basename(filepath)}")
            return success
        except Exception as e:
            self._show_status(f"Ошибка сохранения: {e}")
            return False

    def get_current_file(self) -> Optional[str]:
        return self._current_file_path

    def add_client(self, client_data: Dict[str, str]) -> bool:
        try:
            client = Client(**client_data)
            self._collection.add_client(client)

            # Если есть открытый файл, обновляем его
            if self._current_file_path:
                XMLHandler.append_client_to_xml(client, self._current_file_path)

            self._reset_display()
            self._show_status("Клиент успешно добавлен")
            return True
        except Exception as e:
            self._show_status(f"Ошибка добавления: {e}")
            return False

    def delete_by_conditions(self, conditions: Dict[str, Any]) -> int:
        if not any(conditions.values()):
            self._show_status("Укажите условия для удаления")
            return 0

        count = self._collection.delete_by_conditions(**conditions)

        if count > 0:
            # Обновляем файл если он открыт
            if self._current_file_path:
                XMLHandler.save_to_xml(self._collection, self._current_file_path)

            self._reset_display()
            self._show_status(f"Удалено записей: {count}")
        else:
            self._show_status("Записи, соответствующие условиям, не найдены")

        return count


    def perform_search(self, conditions: Dict[str, Any]) -> bool:
        if not any(conditions.values()):
            self._show_status("Укажите условия для поиска")
            return False

        self._display_list = self._collection.search_clients(**conditions)
        self._current_page = 1

        if len(self._display_list) == 0:
            self._show_status("Ничего не найдено")
        else:
            self._show_status(f"Найдено записей: {len(self._display_list)}")

        self._notify_data_changed()
        self._notify_pagination_changed()
        return True

    def clear_search(self):
        self._reset_display()
        self._show_status("Поиск сброшен. Отображаются все записи.")

    def _reset_display(self):
        self._display_list = self._collection.get_all_clients()
        self._current_page = 1
        self._notify_data_changed()
        self._notify_pagination_changed()

    def get_current_page_data(self) -> List[Client]:
        if not self._display_list:
            return []

        start_idx = (self._current_page - 1) * self._page_size
        end_idx = start_idx + self._page_size

        return self._display_list[start_idx:end_idx]

    def navigate_page(self, direction: str) -> bool:

        total_pages = self.get_pagination_info().total_pages
        if total_pages <= 1:
            return False

        if direction == 'first':
            self._current_page = 1
        elif direction == 'last':
            self._current_page = total_pages
        elif direction == 'next':
            if self._current_page < total_pages:
                self._current_page += 1
            else:
                return False
        elif direction == 'prev':
            if self._current_page > 1:
                self._current_page -= 1
            else:
                return False
        else:
            return False

        self._notify_data_changed()
        self._notify_pagination_changed()
        return True

    def set_page_size(self, size: int):
        if size < 1:
            size = 1
        self._page_size = size
        self._current_page = 1  # Сброс на первую страницу при изменении размера
        self._notify_data_changed()
        self._notify_pagination_changed()

    def get_pagination_info(self) -> PaginationInfo:
        total_items = len(self._display_list)
        total_pages = math.ceil(total_items / self._page_size) if total_items > 0 else 1

        # Корректировка текущей страницы если она вышла за пределы
        if self._current_page > total_pages:
            self._current_page = total_pages

        start_idx = (self._current_page - 1) * self._page_size
        end_idx = min(start_idx + self._page_size, total_items)
        items_on_page = end_idx - start_idx if total_items > 0 else 0

        return PaginationInfo(
            total_items=total_items,
            total_pages=total_pages,
            current_page=self._current_page,
            page_size=self._page_size,
            items_on_page = items_on_page
        )