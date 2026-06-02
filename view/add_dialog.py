from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFormLayout, QMessageBox,
                             QGroupBox, QWidget)
from PySide6.QtCore import Qt


class AddClientDialog(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить клиента")
        self.setMinimumWidth(500)
        self._init_ui()

    def _init_ui(self):
        #Инициализация интерфейса
        layout = QVBoxLayout(self)


        main_group = QGroupBox("Основная информация")
        main_layout = QFormLayout()

        self.edit_full_name = QLineEdit()
        self.edit_full_name.setPlaceholderText("Иванов Иван Иванович")
        main_layout.addRow("ФИО клиента:", self.edit_full_name)

        self.edit_account = QLineEdit()
        self.edit_account.setPlaceholderText("40702810100000001234")
        main_layout.addRow("Номер счета:", self.edit_account)

        self.edit_address = QLineEdit()
        self.edit_address.setPlaceholderText("г. Мозырь, ул. Примерная, д. 67, кв. 67")
        main_layout.addRow("Адрес прописки:", self.edit_address)

        main_group.setLayout(main_layout)
        layout.addWidget(main_group)


        contact_group = QGroupBox("Контактная информация")
        contact_layout = QFormLayout()

        self.edit_phone_mobile = QLineEdit()
        self.edit_phone_mobile.setPlaceholderText("+375 (29) 123-45-67")
        contact_layout.addRow("Мобильный телефон:", self.edit_phone_mobile)

        self.edit_phone_landline = QLineEdit()
        self.edit_phone_landline.setPlaceholderText("+375 (29) 123-45-67")
        contact_layout.addRow("Городской телефон:", self.edit_phone_landline)

        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)


        button_layout = QHBoxLayout() #Создается горизонтальная коробка для кнопок
        button_layout.addStretch() #Кнопки будут находиться около правого края

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept)
        button_layout.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)

    def get_client_data(self):
        #Получение и валидация данных клиента


        full_name = self.edit_full_name.text().strip()
        if not full_name:
            QMessageBox.warning(self, "Ошибка", "Поле 'ФИО клиента' обязательно для заполнения")
            self.edit_full_name.setFocus()
            return None


        account_number = self.edit_account.text().strip()
        if not account_number:
            QMessageBox.warning(self, "Ошибка", "Поле 'Номер счета' обязательно для заполнения")
            self.edit_account.setFocus()
            return None


        address = self.edit_address.text().strip()
        if not address:
            QMessageBox.warning(self, "Ошибка", "Поле 'Адрес прописки' обязательно для заполнения")
            self.edit_address.setFocus()
            return None


        phone_mobile = self.edit_phone_mobile.text().strip()
        if not phone_mobile:
            QMessageBox.warning(self, "Ошибка", "Поле 'Мобильный телефон' обязательно для заполнения")
            self.edit_phone_mobile.setFocus()
            return None


        phone_landline = self.edit_phone_landline.text().strip()
        if not phone_landline:
            QMessageBox.warning(self, "Ошибка", "Поле 'Городской телефон' обязательно для заполнения")
            self.edit_phone_landline.setFocus()
            return None


        from view.validators import validate_client_data
        raw_data = {
            'full_name': full_name,
            'account_number': account_number,
            'registration_address': address,
            'phone_mobile': phone_mobile,
            'phone_landline': phone_landline
        }

        is_valid, error_msg = validate_client_data(raw_data)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка ввода", error_msg)
            return None

        return raw_data
