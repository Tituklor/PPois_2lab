from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem,
                             QToolBar, QStatusBar, QLabel, QPushButton,
                             QComboBox, QSpinBox, QMessageBox, QFileDialog,
                             QDialog, QHeaderView)
from PySide6.QtGui import QAction
from view.add_dialog import AddClientDialog
from view.search_dialog import SearchDialog
from view.delete_dialog import DeleteDialog


class MainWindow(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Управление клиентами")
        self.setMinimumSize(1200, 700)

        # Установка callbacks для связи с контроллером
        self.controller.set_view_callbacks(
            on_data_changed=self.refresh_table,
            on_pagination_changed=self.update_pagination_controls,
            on_status_message=self.show_status_message
        )
        self._init_ui()
        self.refresh_table()
        self.update_pagination_controls()

    def _init_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)


        self.table = QTableWidget()
        self._setup_table()
        layout.addWidget(self.table)
        self._create_pagination_panel(layout) # создаем панель пагинации
        self._create_menu()
        self._create_toolbar()


        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Готов к работе")

    def _setup_table(self):
        headers = ["ФИО клиента", "Номер счета", "Адрес прописки",
                   "Моб. телефон", "Городской телефон"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Interactive)
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        header.setSectionResizeMode(4, QHeaderView.Interactive)
        self.table.setColumnWidth(0, 270)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 150)

        self.table.setSelectionBehavior(QTableWidget.SelectRows) #кликом выделяем всю строку
        self.table.setSelectionMode(QTableWidget.SingleSelection) #выбрать одну за раз строку
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

    def _create_pagination_panel(self, layout):

        pagination_layout = QHBoxLayout()


        self.btn_first = QPushButton("<< Первая")
        self.btn_prev = QPushButton("< Пред.")
        self.btn_next = QPushButton("След. >")
        self.btn_last = QPushButton("Последняя >>")
        self.lbl_page_info = QLabel("Страница 1 из 1")
        self.lbl_records_info = QLabel("Записей: 0")

        pagination_layout.addWidget(QLabel("Записей на странице:"))
        self.combo_page_size = QComboBox()
        self.combo_page_size.addItems(["10", "20", "50", "100"])
        self.combo_page_size.setCurrentText("10")
        self.combo_page_size.currentTextChanged.connect(self.on_page_size_changed)

        self.spin_page = QSpinBox()# ввод номера страницы
        self.spin_page.setMinimum(1)
        self.spin_page.setMaximum(1)
        self.spin_page.valueChanged.connect(self.on_page_changed)

        # выстраиваем все в одну строку
        pagination_layout.addWidget(self.btn_first)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.lbl_page_info)
        pagination_layout.addWidget(self.spin_page)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addWidget(self.btn_last)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.lbl_records_info)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.combo_page_size)


        self.btn_first.clicked.connect(lambda: self.controller.navigate_page('first'))
        self.btn_prev.clicked.connect(lambda: self.controller.navigate_page('prev'))
        self.btn_next.clicked.connect(lambda: self.controller.navigate_page('next'))
        self.btn_last.clicked.connect(lambda: self.controller.navigate_page('last'))

        layout.addLayout(pagination_layout)

    def _create_menu(self):

        menubar = self.menuBar()


        file_menu = menubar.addMenu("Файл")

        self.action_open = QAction("Открыть...", self)
        self.action_open.setShortcut("Ctrl+O") # назначаем горячую клавишу
        self.action_open.triggered.connect(self.open_file)
        file_menu.addAction(self.action_open)

        self.action_save = QAction("Сохранить", self)
        self.action_save.setShortcut("Ctrl+S")
        self.action_save.triggered.connect(self.save_file)
        file_menu.addAction(self.action_save)

        self.action_save_as = QAction("Сохранить как...", self)
        self.action_save_as.setShortcut("Ctrl+Shift+S")
        self.action_save_as.triggered.connect(self.save_file_as)
        file_menu.addAction(self.action_save_as)

        file_menu.addSeparator()

        self.action_exit = QAction("Выход", self)
        self.action_exit.setShortcut("Alt+F4")
        self.action_exit.triggered.connect(self.close)
        file_menu.addAction(self.action_exit)


        clients_menu = menubar.addMenu("Клиенты")

        self.action_add = QAction("Добавить клиента...", self)
        self.action_add.setShortcut("Ctrl+N")
        self.action_add.triggered.connect(self.add_client)
        clients_menu.addAction(self.action_add)


        search_menu = menubar.addMenu("Поиск")

        self.action_search = QAction("Найти клиентов...", self)
        self.action_search.setShortcut("Ctrl+F")
        self.action_search.triggered.connect(self.search_clients)
        search_menu.addAction(self.action_search)

        self.action_clear_search = QAction("Сбросить поиск", self)
        self.action_clear_search.setShortcut("Esc")
        self.action_clear_search.triggered.connect(self.clear_search)
        search_menu.addAction(self.action_clear_search)

        delete_menu = menubar.addMenu("Удаление")

        self.action_delete = QAction("Удалить по условиям...", self)
        self.action_delete.setShortcut("Ctrl+D")
        self.action_delete.triggered.connect(self.delete_clients)
        delete_menu.addAction(self.action_delete)

        help_menu = menubar.addMenu("Справка")

        self.action_about = QAction("О программе...", self)
        self.action_about.triggered.connect(self.show_about)
        help_menu.addAction(self.action_about)

    def _create_toolbar(self):
        toolbar = QToolBar("Основные действия")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self.action_open)
        toolbar.addAction(self.action_save)
        toolbar.addSeparator()
        toolbar.addAction(self.action_add)
        toolbar.addSeparator()
        toolbar.addAction(self.action_search)
        toolbar.addAction(self.action_clear_search)
        toolbar.addSeparator()
        toolbar.addAction(self.action_delete)

    def refresh_table(self):
        clients = self.controller.get_current_page_data() #Запрашивает у контроллера список объектов клиентов для текущей страницы
        self.table.setRowCount(len(clients))

        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QTableWidgetItem(client.full_name))
            self.table.setItem(row, 1, QTableWidgetItem(client.account_number))
            self.table.setItem(row, 2, QTableWidgetItem(client.registration_address))
            self.table.setItem(row, 3, QTableWidgetItem(client.phone_mobile))
            self.table.setItem(row, 4, QTableWidgetItem(client.phone_landline))

    def update_pagination_controls(self, pagination_info=None):

        if pagination_info is not None:
            pagination = pagination_info
        else:
            pagination = self.controller.get_pagination_info()


        self.lbl_page_info.setText(f"Страница {pagination.current_page} из {pagination.total_pages}")
        self.lbl_records_info.setText(f"Записей: {pagination.total_items} (на странице: {pagination.items_on_page})")


        self.spin_page.blockSignals(True)
        self.spin_page.setMaximum(max(1, pagination.total_pages))
        self.spin_page.setValue(pagination.current_page)
        self.spin_page.blockSignals(False)


        has_pages = pagination.total_pages > 1
        self.btn_first.setEnabled(has_pages and pagination.current_page > 1)
        self.btn_prev.setEnabled(has_pages and pagination.current_page > 1)
        self.btn_next.setEnabled(has_pages and pagination.current_page < pagination.total_pages)
        self.btn_last.setEnabled(has_pages and pagination.current_page < pagination.total_pages)

    def show_status_message(self, message: str):

        self.statusBar.showMessage(message, 5000)

    def on_page_size_changed(self, value: str):

        try:
            size = int(value)
            self.controller.set_page_size(size)
        except ValueError:
            pass

    def on_page_changed(self, value: int):

        pagination = self.controller.get_pagination_info()
        if 1 <= value <= pagination.total_pages:

            self.controller._current_page = value
            self.controller._notify_data_changed()
            self.controller._notify_pagination_changed()



    def open_file(self):

        filepath, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "data", "XML файлы (*.xml);;Все файлы (*)"
        )
        if filepath:
            if self.controller.load_data(filepath):
                self.refresh_table()
                self.update_pagination_controls()

    def save_file(self):
        filepath = self.controller.get_current_file()
        if filepath:
            self.controller.save_data(filepath)
        else:
            self.save_file_as()

    def save_file_as(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "data/clients.xml", "XML файлы (*.xml);;Все файлы (*)"
        )
        if filepath:
            self.controller.save_data(filepath)

    def add_client(self):
        dialog = AddClientDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            client_data = dialog.get_client_data()
            if self.controller.add_client(client_data):
                self.refresh_table()
                self.update_pagination_controls()

    def search_clients(self):
        dialog = SearchDialog(self)
        if dialog.exec() == QDialog.Accepted:
            conditions = dialog.get_search_conditions()
            if self.controller.perform_search(conditions):
                self.refresh_table()
                self.update_pagination_controls()

    def clear_search(self):
        self.controller.clear_search()
        self.refresh_table()
        self.update_pagination_controls()

    def delete_clients(self):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            conditions = dialog.get_delete_conditions()
            count = self.controller.delete_by_conditions(conditions)
            if count > 0:
                self.refresh_table()
                self.update_pagination_controls()
                QMessageBox.information(self, "Удаление",
                                        f"Удалено записей: {count}")
            else:
                QMessageBox.warning(self, "Удаление",
                                    "Записи, соответствующие условиям, не найдены")

    def show_about(self):
        QMessageBox.information(
            self, "О программе",
            "Управление клиентами\n\n"
            "Поиск и удаление:\n"
            "- По номеру телефона \n"
            "- По  фамилии\n"
            "- По номеру счета \n"
            "- По адресу"
        )