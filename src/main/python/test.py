from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/main_buttons.ui", self)  # Load UI dynamically

        # Get the StackedWidget
        self.stackedWidget = self.findChild(QWidget, "stackedWidget")

        # Connect buttons to switch pages by name
        self.butConnect.clicked.connect(lambda: self.switch_page("Connect"))
        self.butSetup.clicked.connect(lambda: self.switch_page("Setup"))
        self.butMeasure.clicked.connect(lambda: self.switch_page("Measure"))
        self.butView.clicked.connect(lambda: self.switch_page("View"))
        self.butDebug.clicked.connect(lambda: self.switch_page("Debug"))

    def switch_page(self, page_name):
        """Switch QStackedWidget page by name."""
        target_page = self.findChild(QWidget, page_name)
        if target_page:
            self.stackedWidget.setCurrentWidget(target_page)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())