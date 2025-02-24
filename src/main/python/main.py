from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QFileDialog
from PyQt6.QtCore import QTimer, QDateTime
from serial import Serial
from serial.tools import list_ports
import pyqtgraph as pg
import csv
import os
import pandas as pd

class TyhmosControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/main_buttons.ui", self)

        self.serial = None  # Placeholder for Serial connection
        self.connected = False

        self.selected_folder = None
        self.serial_buffer = ""

        # Populate the ComboBox with available serial ports 
        self.populate_serial_ports()

        # Connect buttons to their respective actions
        self.buttonConnect.clicked.connect(self.connect_serial)
        self.buttonStartStop.clicked.connect(self.measurementStartStop)
        self.buttonSend.clicked.connect(self.send_command_line)
        self.buttonHome.clicked.connect(self.send_command_home)
        self.buttonTare.clicked.connect(self.send_command_tare)

        # Trigger sendButton when Enter is pressed in commandLineEdit
        self.commandLineEdit.returnPressed.connect(self.send_command_line)
        self.buttonHelp.clicked.connect(self.send_command_help)  # Connect buttonHelp

        self.testSuccess.clicked.connect(self.dummy_measurement)

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

        self.butOutSelectFolder.clicked.connect(self.select_folder)

        # Set default label for connection status
        self.labelConnection.setText("Not Connected")

        # Setup graph for real-time plotting
        self.setup_graph_timebased()
        self.setup_graph_positionbased()

        self.measurement_state = "ready"

        # Placeholder for graph data
        self.graph_time_data = [[], [], []]  # Stores time-based data for 3 loadcells
        # Stores position-based data for 3 loadcells
        self.graph_pos_data = pd.DataFrame(columns=["position", "loadcell1", "loadcell2", "loadcell3"])
        self.last_pos = 0

        self.firstSampleIndex = True
        self.numSampleIndex.editingFinished.connect(self.update_sample_index)

        self.butClear.clicked.connect(self.ask_clear)
        self.butExport.clicked.connect(lambda: self.set_measurement_state("EXPORT"))

        # Get the StackedWidget
        self.stackedWidget = self.findChild(QWidget, "stackedWidget")

        self.nav_buttons = [
            self.butConnect,  
            self.butMachineSetup,    
            self.butExperimentSetup,    
            self.butMeasure,  
            self.butView,     
            self.butDebug     
        ]

        # Connect buttons to switch pages by name
        self.butConnect.clicked.connect(lambda: self.switch_page("Connect", self.butConnect))
        self.butMachineSetup.clicked.connect(lambda: self.switch_page("MachineSetup", self.butMachineSetup))
        self.butExperimentSetup.clicked.connect(lambda: self.switch_page("ExperimentSetup", self.butExperimentSetup))
        self.butMeasure.clicked.connect(lambda: self.switch_page("Measure", self.butMeasure))
        self.butView.clicked.connect(lambda: self.switch_page("View", self.butView))
        self.butDebug.clicked.connect(lambda: self.switch_page("Debug", self.butDebug))

        # Set the initial button highlight
        self.switch_page("Connect", self.butConnect)

    def update_sample_index(self):
        self.firstSampleIndex = True
    
    def ask_clear(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure to clear the graph?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.set_measurement_state("CLEAR")

    def clear_graph(self):
        self.graph_pos_data = pd.DataFrame(columns=["position", "loadcell1", "loadcell2", "loadcell3"])
        self.draw_graph(clear=True)
        self.last_pos = 0
    
    def dummy_measurement(self):
        self.graph_pos_data.loc[0] = [1, None, 0, None]
        self.graph_pos_data.loc[1] = [2, None, 10, None]
        self.graph_pos_data.loc[2] = [3, None, 13, None]
        self.draw_graph()
        self.set_measurement_state("SUCCESS")

    def switch_page(self, page_name, active_button):
        """Switch QStackedWidget page by name."""
        target_page = self.findChild(QWidget, page_name)
        if target_page:
            self.stackedWidget.setCurrentWidget(target_page)
            if page_name == "ExperimentSetup":
                self.inputExperimentDate.setDateTime(QDateTime.currentDateTime())

            # Reset all button colors
            for button in self.nav_buttons:
                button.setStyleSheet("")

            # Highlight the active button with a green tint
            active_button.setStyleSheet("background-color: lightgreen; color: black;")

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
                # send command to start receiving data
                self.send_command("DATAC")

            except Exception as e:
                self.set_connection_status(False)
                self.show_message(f"Failed to connect: {e}", error=True)

    def set_connection_status(self, status):
        """Update UI based on connection status."""
        if status:
            self.labelConnection.setText("Connected")
            self.buttonConnect.setText("Disconnect")
            self.labelConnection.setStyleSheet("background-color: green;")  # Set background to green
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

    def set_measurement_state(self, transition):
        if self.measurement_state == "ready":
            if transition == "START":
                self.measurement_state = "measuring"
                self.lMeasurementState.setText("Measuring...")
                self.buttonStartStop.setText("Stop")
                self.lMeasurementState.setStyleSheet("background-color: lightgreen;")
                self.butExport.setEnabled(False)
                self.butClear.setEnabled(False)
                self.inputExperimentDate.setDateTime(QDateTime.currentDateTime())
                self.clear_graph()
                if self.firstSampleIndex:
                    self.firstSampleIndex = False
                else:
                    self.numSampleIndex.setValue(self.numSampleIndex.value() + 1)
                # ToDo start measurement
                #self.send_command("ToDo implement experiment start command")

        elif self.measurement_state == "measuring":
            if transition == "STOP":
                self.measurement_state = "done"
                self.lMeasurementState.setText("Stopped")
                self.buttonStartStop.setText("Start")
                self.lMeasurementState.setStyleSheet("background-color: orange;")
                self.buttonStartStop.setEnabled(False)
                self.butExport.setEnabled(True)
                self.butClear.setEnabled(True)

            elif transition == "SUCCESS":
                self.measurement_state = "done"
                self.lMeasurementState.setText("Done")
                self.buttonStartStop.setText("Start")
                self.lMeasurementState.setStyleSheet("background-color: green;")
                self.buttonStartStop.setEnabled(False)
                self.butExport.setEnabled(True)
                self.butClear.setEnabled(True)

        elif self.measurement_state == "done":
            if transition == "CLEAR":
                self.measurement_state = "ready"
                self.lMeasurementState.setText("Ready")
                self.buttonStartStop.setText("Start")
                self.lMeasurementState.setStyleSheet("")
                self.buttonStartStop.setEnabled(True)
                self.butExport.setEnabled(False)
                self.butClear.setEnabled(False)
                self.clear_graph()
                self.firstSampleIndex = True

            elif transition == "EXPORT":
                if self.selected_folder:
                    self.measurement_state = "ready"
                    self.lMeasurementState.setText("Ready")
                    self.buttonStartStop.setText("Start")
                    self.lMeasurementState.setStyleSheet("")
                    self.buttonStartStop.setEnabled(True)
                    self.butExport.setEnabled(False)
                    self.butClear.setEnabled(False)
                    #Export data to CSV
                    metadata = {
                        "Title": self.inputExperimentTitle.text(),
                        "Sample Index": self.numSampleIndex.value(),
                        "Sample": self.inputExperimentSample.text(),
                        "Author": self.inputExperimentAuthor.text(),
                        "Date": self.inputExperimentDate.text(),
                        "Description": self.inputExperimentDescription.toPlainText(),
                        "Notes": self.inputExperimentNotes.toPlainText(),
                        "Speed": self.numExperimentSpeed.value(),
                        }
                    filename = f"{self.inputExperimentTitle.text()}_{self.numSampleIndex.value()}.csv"
                    self.export_to_csv(
                        self.graph_pos_data,
                        self.selected_folder,
                        filename,
                        metadata)
                else:
                    self.show_message("Please select an output folder first.", error=True)


    def measurementStartStop(self):
        """Send 'Start' command to the connected serial device."""
        # STOP
        if self.measurement_state == "ready":
            self.set_measurement_state("START")
        # START
        elif self.measurement_state == "measuring":
            self.set_measurement_state("STOP")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:  # If user selected a folder
            self.selected_folder = folder
            self.labOutFolder.setText(folder)

    def export_to_csv(self, pos_data, folder, filename, metadata):
        """
        Exports position-based data for load cells to a CSV file.

        :param pos_data: List of lists containing (position, value) tuples.
        :param folder: The folder where the CSV file will be saved.
        :param filename: Name of the CSV file.
        :param metadata: Dictionary containing metadata (e.g., author, date, title).
        """
        if not os.path.exists(folder):
            print(f"Error: Folder '{folder}' does not exist.")
            return

        filepath = os.path.join(folder, filename)

        max_length = max(len(data) for data in pos_data)  # Find longest list

        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write metadata at the top
            for key, value in metadata.items():
                writer.writerow([key, value])
            writer.writerow([])  # Empty row to separate metadata from data

            # Extract columns dynamically (keeping "position" first)
            headers = ["position"] + [col for col in self.graph_pos_data.columns if col != "position"]
            writer.writerow(headers)

            # Write data row by row
            for _, row in self.graph_pos_data.iterrows():
                writer.writerow(row.fillna("").tolist())  # Replace NaN with empty string

        print(f"Data exported successfully to {filepath}")

    def send_command_help(self):
        self.send_command("HELP")

    def send_command_home(self):
        self.send_command("MC CALIBRATE")

    def send_command_tare(self):
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

    def draw_graph(self, clear=False):
        try:
            # Check if the tab with the graph is currently visible
            current_tab_index = self.tabWidget.currentIndex()

            if current_tab_index == 0:  # Time-based graph
                for i in range(3):
                    if self.graph_time_data[i]:
                        x_data, y_data = zip(*self.graph_time_data[i])  # Extract timestamps & values
                        self.curves_time[i].setData(x_data, y_data)
                    if clear:
                        x_data, y_data = [], []
                        self.curves_time[i].setData(x_data, y_data)

            elif current_tab_index == 1:  # Position-based graph
                for i in range(3):
                    if clear:
                        x_data, y_data = [], []
                        self.curves_pos[i].setData(x_data, y_data)
                    else:
                        x_data = self.graph_pos_data["position"]
                        y_data = self.graph_pos_data[f"loadcell{i+1}"]
                        print(x_data, y_data)
                        if y_data.any():
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

            if curPos != self.last_pos and self.measurement_state == "measuring":
                self.graph_pos_data.loc[len(self.graph_pos_data)] = [curPos, *loadcells]  # Add a new row at the end
                # self.graph_pos_data[i] = self.graph_pos_data[i][-DATA_POINTS:]
            self.last_pos = curPos

            # bargraphhs
            self.loadcell1.setValue(int(loadcells[0]))
            self.loadcell2.setValue(int(loadcells[1]))
            self.loadcell3.setValue(int(loadcells[2]))
            # values
            self.nLC1.display(int(loadcells[0]))
            self.nLC2.setText(f"{loadcells[1]:.2f} N") 
            self.nLC3.setText(f"{loadcells[2]:.2f} N") 

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