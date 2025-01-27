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
        self.form.startButton.clicked.connect(self.send_command_start)
        self.form.buttonSend.clicked.connect(self.send_command_line)

        # Trigger sendButton when Enter is pressed in commandLineEdit
        self.form.commandLineEdit.returnPressed.connect(self.send_command_line)
        self.form.buttonHelp.clicked.connect(self.send_command_help)  # Connect buttonHelp

        # Timer to read data from the serial port periodically
        self.serial_read_timer = QTimer()
        self.serial_read_timer.timeout.connect(self.read_serial_data)

        # Set default label for connection status
        self.form.labelConnection.setText("Not Connected")


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
            # Disconnect if already connected
            self.serial.close()
            self.connected = False
            self.serial_read_timer.stop()
            self.form.connectButton.setText("Connect")
            self.form.labelConnection.setText("Disconnected")  # Update connection status
            self.show_message("Disconnected from serial device.")
        else:
            try:
                selected_port = self.form.serialPortComboBox.currentText()
                self.serial = Serial(selected_port, baudrate=9600, timeout=1)
                self.connected = True
                self.serial_read_timer.start(100)  # Start reading every 100ms
                self.form.connectButton.setText("Disconnect")
                self.form.labelConnection.setText(f"Connected")  # Update connection status
            except Exception as e:
                self.show_message(f"Failed to connect: {e}", error=True)
                self.form.labelConnection.setText("Failed")  # Handle error case

    def send_command(self, command):
        """Send a command to the connected serial device."""
        if not self.connected:
            self.show_message("Please connect to a serial device first.", error=True)
            return
        try:
            self.serial.write(f"{command}\n".encode())  # Send the command
            self.form.commandLineOutput.append(f">>> {command}")  # Add to output with prefix
        except Exception as e:
            self.show_message(f"Failed to send command: {e}", error=True)

    def send_command_start(self):
        """Send 'Start' command to the connected serial device."""
        self.send_command("Start")

    def send_command_help(self):
        """Send 'Start' command to the connected serial device."""
        self.send_command("HELP")


    def send_command_line(self):
        """Send a command manually entered in the commandLineEdit."""
        if not self.connected:
            self.show_message("Please connect to a serial device first.", error=True)
            return

        command = self.form.commandLineEdit.text()  # Get the command from QLineEdit
        if command.strip() == "":
            self.show_message("Command cannot be empty.", error=True)
            return
        try:
            self.send_command(command)  # Send the command
            self.form.commandLineEdit.clear()  # Clear the input field
        except Exception as e:
            self.show_message(f"Failed to send command: {e}", error=True)

    def read_serial_data(self):
        """Read data from the serial port and display it in the QTextEdit."""
        if self.connected and self.serial.in_waiting > 0:
            try:
                data = self.serial.readline().decode().strip()
                self.form.commandLineOutput.append(data)  # Append data to the QTextEdit
            except Exception as e:
                self.show_message(f"Failed to read data: {e}", error=True)

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