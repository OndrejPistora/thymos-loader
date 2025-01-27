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
        self.form.buttonConnect.clicked.connect(self.connect_serial)
        self.form.buttonStart.clicked.connect(self.send_command_start)
        self.form.buttonSend.clicked.connect(self.send_command_line)
        self.form.buttonCalibrate.clicked.connect(self.send_command_calibrate)
        self.form.buttonTare.clicked.connect(self.send_command_tare)

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
        self.form.serialPortSelection.clear()
        ports = list_ports.comports()
        for port in ports:
            self.form.serialPortSelection.addItem(port.device)
        if ports:
            self.form.serialPortSelection.setCurrentIndex(0)

    def connect_serial(self):
        """Connect to the selected serial port."""
        if self.connected:
            # Disconnect if already connected
            self.serial.close()
            self.connected = False
            self.serial_read_timer.stop()
            self.set_connection_status(False)
        else:
            try:
                selected_port = self.form.serialPortSelection.currentText()
                self.serial = Serial(selected_port, baudrate=9600, timeout=1)
                self.connected = True
                self.serial_read_timer.start(10)  # Start reading every 10ms
                self.set_connection_status(True)
            except Exception as e:
                self.set_connection_status(False)
                self.show_message(f"Failed to connect: {e}", error=True)

    def set_connection_status(self, status):
        """Update UI based on connection status."""
        if status:
            self.form.labelConnection.setText("Connected")
            self.form.buttonConnect.setText("Disconnect")
            self.form.labelConnection.setStyleSheet("background-color: green; color: white;")  # Set background to green
        else:
            self.form.labelConnection.setText("Disconnected")
            self.form.buttonConnect.setText("Connect")
            self.form.labelConnection.setStyleSheet("")

    def send_command(self, command):
        """Send a command to the connected serial device."""
        if not self.connected:
            self.show_message("Please connect to a serial device first.", error=True)
            return
        try:
            self.serial.write(f"{command}".encode())  # Send the command
            # self.serial.flush()  # Try to make the recieving faster
            self.form.commandLineOutput.append(f">>> {command}")  # Add to output with prefix
        except Exception as e:
            self.show_message(f"Failed to send command: {e}", error=True)

    def send_command_start(self):
        """Send 'Start' command to the connected serial device."""
        # ToDo start measurement
        self.send_command("ToDo implement experiment start command")

    def send_command_help(self):
        """Send 'Start' command to the connected serial device."""
        self.send_command("HELP")

    def send_command_calibrate(self):
        """Send 'Start' command to the connected serial device."""
        self.send_command("MC CALIBRATE")

    def send_command_tare(self):
        """Send 'Start' command to the connected serial device."""
        # ToDo send command to tare 
        self.send_command("ToDo implement tare command")

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

    def update_loadcells(self, loadcells):
        """Update the loadcell values in the UI."""
        try:
            self.form.loadcell1.setValue(loadcells[0])
            self.form.loadcell2.setValue(loadcells[1])
            self.form.loadcell3.setValue(loadcells[2])
        except Exception as e:
            print(f"Failed to update loadcells: {e}", error=True)
            quit()


    def read_serial_data(self):
        """Read data from the serial port and display it in the QTextEdit."""
        if self.connected and self.serial.in_waiting > 0:
            try:
                # Read all available data from the serial buffer
                raw_data = self.serial.read(self.serial.in_waiting).decode()
                lines = raw_data.strip().split("\n")
                for line in lines:
                    if line.startswith("DS"):  # machine data received
                        # DS925049089,0.00,0.00,0.00,53.47,0.00
                        print(line)
                        line = line.strip()[2:]
                        data = line.split(",")
                        timestamp = data[0]
                        curPos = data[1]
                        curVel = data[2]
                        loadcells = [data[3], data[4], data[5]]
                        #convert from string to int
                        loadcells = [int(float(i)) for i in loadcells]
                        self.update_loadcells(loadcells)
                    else:
                        self.form.commandLineOutput.append(line.strip())
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