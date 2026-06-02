from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QGroupBox, QFormLayout,
                               QMessageBox)
from PySide6.QtCore import Qt


class DeleteDialog(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удаление клиентов по условиям")
        self.setMinimumWidth(500)
        self._init_ui()

    def _init_ui(self):

        layout = QVBoxLayout(self)


        info_label = QLabel("Введите условия для удаления записей.\n"
                            "Будут удалены все записи, совпадающие с условиями.")
        info_label.setWordWrap(True) #окно станет узким, текст автоматически перенесётся на следующую строку
        layout.addWidget(info_label)


        conditions_group = QGroupBox("Условия удаления")
        conditions_layout = QFormLayout()


        self.edit_surname = QLineEdit()
        self.edit_surname.setPlaceholderText("Иванов")
        conditions_layout.addRow("По фамилии:", self.edit_surname)


        self.edit_address = QLineEdit()
        self.edit_address.setPlaceholderText("г. Минск, ул. Ленина")
        conditions_layout.addRow("По адресу:", self.edit_address)


        self.edit_account = QLineEdit()
        self.edit_account.setPlaceholderText("40702810100000001234")
        conditions_layout.addRow("По номеру счета:", self.edit_account)


        self.edit_mobile_phone = QLineEdit()
        self.edit_mobile_phone.setPlaceholderText("+375 (29) 123-45-67")
        conditions_layout.addRow("По моб. номеру:", self.edit_mobile_phone)

        conditions_group.setLayout(conditions_layout)
        layout.addWidget(conditions_group)


        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.setStyleSheet(
            "QPushButton { background-color: #40E0D0; color: black; padding: 5px 15px; }")
        self.btn_delete.clicked.connect(self.accept)
        button_layout.addWidget(self.btn_delete)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)

    def get_delete_conditions(self):

        conditions = {}

        surname = self.edit_surname.text().strip()
        if surname:
            conditions['surname'] = surname

        address = self.edit_address.text().strip()
        if address:
            conditions['address'] = address

        account = self.edit_account.text().strip()
        if account:
            conditions['account'] = account

        mobile_phone = self.edit_mobile_phone.text().strip()
        if mobile_phone:
            conditions['mobile_phone'] = mobile_phone

        return conditions