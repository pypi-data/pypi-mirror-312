import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class HtmlViewerApp:
    def __init__(self, html_content=None, html_file=None, title="HTML Viewer"):
        """
        Инициализация приложения для отображения HTML-контента.
        :param html_content: HTML-контент в виде строки для отображения.
        :param html_file: Путь к HTML-файлу для отображения.
        :param title: Название окна.
        """
        self.app = QApplication(sys.argv)  # Запускаем QApplication
        self.window = QMainWindow()  # Главное окно приложения
        self.window.setWindowTitle(title)  # Устанавливаем название окна

        self.layout = QVBoxLayout()  # Вертикальное расположение элементов
        self.central_widget = QWidget()  # Центральный виджет
        self.central_widget.setLayout(self.layout)  # Устанавливаем компоновку
        self.window.setCentralWidget(self.central_widget)

        # Создаем QWebEngineView для отображения HTML
        self.web_view = QWebEngineView(self.central_widget)

        # Загружаем HTML: строку или файл
        if html_content:
            self.load_html(html_content)
        elif html_file:
            self.load_html_file(html_file)
        else:
            self.load_default_html()

        # Добавляем WebView в layout
        self.layout.addWidget(self.web_view)

    def load_html(self, html_content):
        """
        Загружает HTML-контент в QWebEngineView.
        :param html_content: HTML-контент для загрузки.
        """
        self.web_view.setHtml(html_content)

    def load_html_file(self, html_file):
        """
        Загружает HTML из файла в QWebEngineView.
        :param html_file: Путь к HTML-файлу.
        """
        self.web_view.setUrl(QUrl.fromLocalFile(html_file))

    def load_default_html(self):
        """
        Загружает стандартный HTML (например, локальный файл или URL).
        """
        self.web_view.setUrl(QUrl("https://www.example.com"))

    def run(self):
        """
        Запускает главное окно приложения.
        """
        self.window.show()
        sys.exit(self.app.exec_())

