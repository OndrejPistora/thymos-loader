from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from serial import Serial
from serial.tools import list_ports

# Load the UI
Form, Window = uic.loadUiType("src/ui/main.ui")

class SerialApp:
    def __init__(self):
        self.serial = None  # Placeholder for Serial connection
        self.connected = False

        # Initialize GUI
        self.app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)
        self.window.show()

        # Populate the ComboBox with available serial ports
        self.populate_serial_ports()

        # Connect buttons to their respective actions
        self.form.connectButton.clicked.connect(self.connect_serial)
        self.form.startButton.clicked.connect(self.start_command)

    def populate_serial_ports(self):
        """Populate the ComboBox with available serial ports."""
        self.form.serialPortComboBox.clear()
        ports = list_ports.comports()
        for port in ports:
            self.form.serialPortComboBox.addItem(port.device)
        if ports:
            self.form.serialPortComboBox.setCurrentIndex(0)

    def connect_serial(self):
        """Connect to the selected serial port."""
        if self.connected:
            # If already connected, disconnect
            self.serial.close()
            self.connected = False
            self.form.connectButton.setText("Connect")
            self.show_message("Disconnected from serial device.")
        else:
            try:
                selected_port = self.form.serialPortComboBox.currentText()
                self.serial = Serial(selected_port, baudrate=9600, timeout=1)
                self.connected = True
                self.form.connectButton.setText("Disconnect")
                self.show_message(f"Connected to {selected_port}")
            except Exception as e:
                self.show_message(f"Failed to connect: {e}", error=True)

    def start_command(self):
        """Send 'Start' command to the connected serial device."""
        if not self.connected:
            self.show_message("Please connect to a serial device first.", error=True)
            return

        try:
            self.serial.write(b"Start\n")  # Send the 'Start' command
            self.show_message("Command 'Start' sent.")
        except Exception as e:
            self.show_message(f"Failed to send command: {e}", error=True)

    def show_message(self, message, error=False):
        """Show a message box for errors or notifications."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical if error else QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error" if error else "Notification")
        msg_box.exec()

    def run(self):
        self.app.exec()

if __name__ == "__main__":
    app = SerialApp()
    app.run()