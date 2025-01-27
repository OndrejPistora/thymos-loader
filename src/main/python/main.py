from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from serial import Serial
from serial.tools import list_ports
import pyqtgraph as pg

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
        self.graph_timer = QTimer()
        self.graph_timer.timeout.connect(self.draw_graph)

        # Set default label for connection status
        self.form.labelConnection.setText("Not Connected")

        # Setup graph for real-time plotting
        self.setup_graph()

        # Placeholder for graph data
        self.graph_data = [[], [], []]  # Three separate lists for loadcells

    def setup_graph(self):
        """Initialize the graph for real-time plotting."""
        # Access the PlotWidget directly
        self.form.graphicsView.setBackground('w')  # Set white background
        self.form.graphicsView.showGrid(x=True, y=True)  # Show gridlines
        self.form.graphicsView.setTitle("Load Cell Data")  # Set title
        self.form.graphicsView.addLegend()  # Add legend

        # Initialize curves for each loadcell
        self.curves = [
            self.form.graphicsView.plot(pen=pg.mkPen('r'), name="Loadcell 1"),  # Red
            self.form.graphicsView.plot(pen=pg.mkPen('g'), name="Loadcell 2"),  # Green
            self.form.graphicsView.plot(pen=pg.mkPen('b'), name="Loadcell 3"),  # Blue
        ]


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
            self.graph_timer.stop()
            self.set_connection_status(False)
        else:
            try:
                selected_port = self.form.serialPortSelection.currentText()
                self.serial = Serial(selected_port, baudrate=9600, timeout=1)
                self.connected = True
                self.serial_read_timer.start(10)  # Start reading every 10ms
                self.graph_timer.start(50)  # draw graphs 20 Hz
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

    def draw_graph(self):
        try:
            for i, data in enumerate(self.graph_data):
                self.curves[i].setData(self.graph_data[i])  # Update the graph
        except Exception as e:
            print(f"Failed to draw graphs: {e}")
            quit()

    def update_loadcells(self, loadcells):
        """Update the loadcell values in the UI."""
        try:
            for i, load in enumerate(loadcells):
                self.graph_data[i].append(load)  # Add the new value to the graph data
                self.graph_data[i] = self.graph_data[i][-4000:]  # Keep the last 100 points
            self.form.loadcell1.setValue(int(loadcells[0]))
            self.form.loadcell2.setValue(int(loadcells[1]))
            self.form.loadcell3.setValue(int(loadcells[2]))
        except Exception as e:
            print(f"Failed to update loadcells: {e}")
            quit()



    def read_serial_data(self):
        """Read data from the serial port and display it in the QTextEdit."""
        if self.connected and self.serial.in_waiting > 0:
            try:
                # Initialize a buffer to store incomplete lines
                if not hasattr(self, "serial_buffer"):
                    self.serial_buffer = ""
                raw_data = self.serial.read(self.serial.in_waiting).decode()
                self.serial_buffer += raw_data
                lines = self.serial_buffer.split("\n")
                self.serial_buffer = lines[-1]

                # Process all complete lines
                for line in lines[:-1]:  # Skip the incomplete last line
                    line = line.strip()
                    if line.startswith("DS"):  # Process machine data
                        print(line)
                        line = line.strip()[2:]
                        data = line.split(",")
                        timestamp = data[0]
                        curPos = data[1]
                        curVel = data[2]
                        loadcells = [data[3], data[4], data[5]]

                        # Convert from string to float for plotting
                        loadcells = [float(i) for i in loadcells]
                        self.update_loadcells(loadcells)
                    else:  # Handle other data
                        self.form.commandLineOutput.append(line)
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