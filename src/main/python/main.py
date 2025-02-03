from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from PyQt6.QtCore import QTimer
from serial import Serial
from serial.tools import list_ports
import pyqtgraph as pg

class TyhmosControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/main_buttons.ui", self)

        self.serial = None  # Placeholder for Serial connection
        self.connected = False

        self.serial_buffer = ""

        # Populate the ComboBox with available serial ports 
        self.populate_serial_ports()

        # Connect buttons to their respective actions
        self.buttonConnect.clicked.connect(self.connect_serial)
        self.buttonStart.clicked.connect(self.send_command_start)
        self.buttonSend.clicked.connect(self.send_command_line)
        self.buttonCalibrate.clicked.connect(self.send_command_calibrate)
        self.buttonTare.clicked.connect(self.send_command_tare)

        # Trigger sendButton when Enter is pressed in commandLineEdit
        self.commandLineEdit.returnPressed.connect(self.send_command_line)
        self.buttonHelp.clicked.connect(self.send_command_help)  # Connect buttonHelp

        # Timer to read data from the serial port periodically
        self.serial_read_timer = QTimer()
        self.serial_read_timer.timeout.connect(self.read_serial_data)
        self.graph_timer = QTimer()
        self.graph_timer.timeout.connect(self.draw_graph)
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.manual_movement_command)
        self.moving_dir = ""

        # Button Press Event
        self.buttonUp.pressed.connect(lambda: self.start_moving("UP"))
        self.buttonDown.pressed.connect(lambda: self.start_moving("DOWN"))
        # Button Release Event
        self.buttonUp.released.connect(lambda: self.stop_moving())
        self.buttonDown.released.connect(lambda: self.stop_moving())

        self.butRefresh.clicked.connect(self.populate_serial_ports)

        # Set default label for connection status
        self.labelConnection.setText("Not Connected")

        # Setup graph for real-time plotting
        self.setup_graph_timebased()
        self.setup_graph_positionbased()

        # Placeholder for graph data
        self.graph_time_data = [[], [], []]  # Stores time-based data for 3 loadcells
        self.graph_pos_data = [[], [], []]   # Stores position-based data for 3 loadcells
        self.last_pos = 0

        self.butClear.clicked.connect(self.clear_output)

        # Get the StackedWidget
        self.stackedWidget = self.findChild(QWidget, "stackedWidget")

        self.nav_buttons = [
            self.butConnect,  
            self.butSetup,    
            self.butMeasure,  
            self.butView,     
            self.butDebug     
        ]

        # Connect buttons to switch pages by name
        self.butConnect.clicked.connect(lambda: self.switch_page("Connect", self.butConnect))
        self.butSetup.clicked.connect(lambda: self.switch_page("Setup", self.butSetup))
        self.butMeasure.clicked.connect(lambda: self.switch_page("Measure", self.butMeasure))
        self.butView.clicked.connect(lambda: self.switch_page("View", self.butView))
        self.butDebug.clicked.connect(lambda: self.switch_page("Debug", self.butDebug))

        # Set the initial button highlight
        self.switch_page("Connect", self.butConnect)

    def clear_output(self):
        pos_data = [[], [], []]   # Stores position-based data for 3 loadcells
        self.last_pos = 0

    def switch_page(self, page_name, active_button):
        """Switch QStackedWidget page by name."""
        target_page = self.findChild(QWidget, page_name)
        if target_page:
            self.stackedWidget.setCurrentWidget(target_page)

            # Reset all button colors
            for button in self.nav_buttons:
                button.setStyleSheet("")

            # Highlight the active button with a green tint
            active_button.setStyleSheet("background-color: lightgreen;")

    def start_moving(self, dir):
        """Start sending movement commands for UP or DOWN."""
        self.moving_dir = dir
        # ToDo change dist based on current velocity?
        self.move_timer.start(50)

    def stop_moving(self):
        """Stop sending movement commands."""
        self.move_timer.stop()
        self.send_command(f"MC STOP")

    def manual_movement_command(self):
        """Send manual movement commands."""
        DIST = 3
        if self.moving_dir == "UP":
            self.send_command(f"MC MOVEBY USER {-DIST}")
        elif self.moving_dir == "DOWN":
            self.send_command(f"MC MOVEBY USER {DIST}")

    def setup_graph_timebased(self):
        """Initialize the graph for real-time plotting."""
        # Access the PlotWidget directly
        self.graphTimeBased.showGrid(x=True, y=True)  # Show gridlines
        self.graphTimeBased.setTitle("Load Cell Data")  # Set title
        self.graphTimeBased.addLegend()  # Add legend

        # Initialize curves for each loadcell
        self.curves_time = [
            self.graphTimeBased.plot(pen=pg.mkPen('r'), name="Loadcell 1"),  # Red
            self.graphTimeBased.plot(pen=pg.mkPen('g'), name="Loadcell 2"),  # Green
            self.graphTimeBased.plot(pen=pg.mkPen('b'), name="Loadcell 3"),  # Blue
        ]
    
    def setup_graph_positionbased(self):
        """Initialize the graph for real-time plotting."""
        # Access the PlotWidget directly
        self.graphPosBased.showGrid(x=True, y=True)
        self.graphPosBased.setTitle("Position Data")
        self.graphPosBased.addLegend()

        # Initialize curves for each loadcell
        self.curves_pos = [
            self.graphPosBased.plot(pen=pg.mkPen('r'), name="Loadcell 1"),  # Red
            self.graphPosBased.plot(pen=pg.mkPen('g'), name="Loadcell 2"),  # Green
            self.graphPosBased.plot(pen=pg.mkPen('b'), name="Loadcell 3"),  # Blue
        ]


    def populate_serial_ports(self):
        """Populate the ComboBox with available serial ports."""
        self.serialPortSelection.clear()
        ports = list_ports.comports()
        for port in ports:
            self.serialPortSelection.addItem(port.device)
        if ports:
            self.serialPortSelection.setCurrentIndex(0)

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
                selected_port = self.serialPortSelection.currentText()
                self.serial = Serial(selected_port, baudrate=9600, timeout=1)
                self.serial.flush()
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
            self.labelConnection.setText("Connected")
            self.buttonConnect.setText("Disconnect")
            self.labelConnection.setStyleSheet("background-color: green; color: white;")  # Set background to green
        else:
            self.labelConnection.setText("Disconnected")
            self.buttonConnect.setText("Connect")
            self.labelConnection.setStyleSheet("")

    def send_command(self, command):
        """Send a command to the connected serial device."""
        if not self.connected:
            self.show_message("Please connect to a serial device first.", error=True)
            return
        try:
            self.serial.write(f"{command}\n".encode())  # Send the command
            # self.serial.flush()  # Ensure the command is sent immediately
            self.commandLineOutput.append(f">>> {command}")  # Add to output with prefix
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
        command = self.commandLineEdit.text()  # Get the command from QLineEdit
        if command.strip() == "":
            self.show_message("Command cannot be empty.", error=True)
            return
        try:
            self.send_command(command)  # Send the command
            self.commandLineEdit.clear()  # Clear the input field
        except Exception as e:
            self.show_message(f"Failed to send command: {e}", error=True)

    def draw_graph(self):
        try:
            # Check if the tab with the graph is currently visible
            current_tab_index = self.tabWidget.currentIndex()

            if current_tab_index == 0 and self.graph_time_data[0]:  # Time-based graph
                for i in range(3):
                    x_data, y_data = zip(*self.graph_time_data[i])  # Extract timestamps & values
                    self.curves_time[i].setData(x_data, y_data)

            elif current_tab_index == 1 and self.graph_pos_data[0]:  # Position-based graph
                for i in range(3):
                    x_data, y_data = zip(*self.graph_pos_data[i])  # Extract positions & values
                    self.curves_pos[i].setData(x_data, y_data)
        except Exception as e:
            print(f"Failed to draw graphs: {e}")
            quit()

    def update_graphdata(self, loadcells, timestamp, curPos):
        """Update the loadcell values in the UI."""
        try:
            # Convert timestamp and position to float
            timestamp = float(timestamp)
            curPos = float(curPos)

            # Keep only the last X points
            DATA_POINTS = 4000

            for i, load in enumerate(loadcells):
                self.graph_time_data[i].append((timestamp, load))  # Store time-based data
                self.graph_time_data[i] = self.graph_time_data[i][-DATA_POINTS:]

            if curPos != self.last_pos:
                for i, load in enumerate(loadcells):
                    self.graph_pos_data[i].append((curPos, load))      # Store position-based data
                    self.graph_pos_data[i] = self.graph_pos_data[i][-DATA_POINTS:]
            self.last_pos = curPos


            self.loadcell1.setValue(int(loadcells[0]))
            self.loadcell2.setValue(int(loadcells[1]))
            self.loadcell3.setValue(int(loadcells[2]))
        except Exception as e:
            print(f"Failed to update loadcells: {e}")
            quit()



    def read_serial_data(self):
        """Read data from the serial port and display it in the QTextEdit."""
        if self.connected and self.serial.in_waiting > 0:
            try:
                # Initialize a buffer to store incomplete lines
                raw_data = self.serial.read(self.serial.in_waiting).decode()
                self.serial_buffer += raw_data
                lines = self.serial_buffer.split("\n")
                self.serial_buffer = lines[-1]

                # Process all complete lines
                for line in lines[:-1]:  # Skip the incomplete last line
                    line = line.strip()
                    if line.startswith("DS"):  # Process machine data
                        # print(line)
                        line = line.strip()[2:]
                        data = line.split(",")
                        timestamp = data[0]
                        curPos = data[1]
                        curVel = data[2]
                        loadcells = [data[3], data[4], data[5]]

                        # Convert from string to float for plotting
                        loadcells = [float(i) for i in loadcells]
                        self.update_graphdata(loadcells, timestamp, curPos)
                    else:  # Handle other data
                        self.commandLineOutput.append(line)
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
    import sys
    app = QApplication(sys.argv)
    window = TyhmosControlApp()
    window.show()
    sys.exit(app.exec())