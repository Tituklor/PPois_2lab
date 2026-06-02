import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from controller import MainController
from view.main_window import MainWindow


def main():
    # Инициализация приложения
    app = QApplication(sys.argv)
    app.setApplicationName("Клиентский менеджер ")
    app.setOrganizationName("Lab2_Project")

    # Установка стиля для кроссплатформенной совместимости
    app.setStyle("Fusion")

    try:
        # Создание контроллера
        controller = MainController()

        # Создание главного окна с привязкой к контроллеру
        window = MainWindow(controller)
        window.show()

        # Запуск цикла обработки событий
        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.critical(None, "Критическая ошибка", f"При запуске приложения произошла ошибка:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()