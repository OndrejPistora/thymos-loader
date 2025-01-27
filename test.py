from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material Testing Machine")
        self.setGeometry(100, 100, 600, 400)
        self.label = QLabel("Welcome to Material Tester", self)
        self.label.setGeometry(200, 180, 200, 50)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()