from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QFileDialog, QTreeWidgetItem
from PyQt6.QtCore import QTimer, QDateTime, QVariantAnimation, QEasingCurve
from PyQt6.QtGui import QShortcut, QKeySequence, QColor, QIcon, QTransform, QPixmap
from PyQt6.QtCore import Qt
from serial import Serial
from serial.tools import list_ports
from convertmattes import convert_mattes
from config import Config
import pyqtgraph as pg
import csv
import os
import polars as pl
import sys




# class TyhmosControlApp(QMainWindow, Ui_MainWindow):
class TyhmosControlApp(QMainWindow):
    def __init__(self, resources):
        super().__init__()
        #print pwd
        print("Current Working Directory:", os.getcwd())
        uic.loadUi(resources["design.ui"], self)
        self.resources = resources
        self.showMaximized()

        # CONFIG
        self.config = Config("config.yaml")

        self.serial = None  # Placeholder for Serial connection
        self.connected = False
        self.serial_buffer = ""

        self.selected_folder = None

        self.measurement_state = "ready"

        self.INIT_POS_DATA = pl.DataFrame(schema={
            "time": pl.Float64,
            "position": pl.Float64,
            "loadcell1": pl.Float64,
            "loadcell2": pl.Float64,
            "loadcell3": pl.Float64
        })

        # Timer to read data from the serial port periodically
        self.serial_read_timer = QTimer()
        self.serial_read_timer.timeout.connect(self.read_serial_data)
        self.graph_timer = QTimer()
        self.graph_timer.timeout.connect(self.draw_graph)
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.manual_movement_command)
        self.manual_speed = 0
        

        # Setup graph for real-time plotting
        self.setup_graph_timebased()
        self.setup_graph_positionbased()

        # Placeholder for graph data
        self.graph_time_data = [[], [], []]  # Stores time-based data for 3 loadcells
        # Stores position-based data for 3 loadcells
        self.graph_pos_data = self.INIT_POS_DATA.clone()
        self.last_pos = 0

        self.currentForce = 0
        self.currentPos = 0
        self.maxExpForce = 0

        self.SampleIndexManual = True
        self.numSampleIndex.valueChanged.connect(self.update_sample_index)
        
        # CONNECT page
        self.buttonConnect.clicked.connect(self.connect_serial)
        self.butRefresh.clicked.connect(self.populate_serial_ports)

        # MACHINE SETUP page
        self.buttonTare1.clicked.connect(lambda: self.send_command_tare(1))
        self.buttonTare2.clicked.connect(lambda: self.send_command_tare(2))
        self.buttonTare3.clicked.connect(lambda: self.send_command_tare(3))
        self.buttonHome.clicked.connect(self.send_command_home)

        # EXPERIMENT SETUP page
        self.buttonSelectFolder.clicked.connect(self.select_folder)
        # manual movement buttons
        self.set_icons_manual()
        VEL_MAN_SLOW = 5
        VEL_MAN_FAST = 50
        self.buttonUp.pressed.connect(lambda: self.start_moving(VEL_MAN_SLOW))
        self.buttonDown.pressed.connect(lambda: self.start_moving(-VEL_MAN_SLOW))
        self.buttonUp2.pressed.connect(lambda: self.start_moving(VEL_MAN_FAST))
        self.buttonDown2.pressed.connect(lambda: self.start_moving(-VEL_MAN_FAST))
        # Button Release Event
        self.buttonUp.released.connect(lambda: self.stop_moving())
        self.buttonUp2.released.connect(lambda: self.stop_moving())
        self.buttonDown.released.connect(lambda: self.stop_moving())
        self.buttonDown2.released.connect(lambda: self.stop_moving())

        # MEASURE page
        self.buttonStart.clicked.connect(self.measurementStart)
        self.buttonStop.clicked.connect(self.measurementStop)
        self.buttonSave.clicked.connect(self.saveExperimentData)
        self.buttonClear.clicked.connect(self.ask_clear)

        # VIEW page
        self.buttonSelectFolder2.clicked.connect(self.select_folder)
        self.wfTree.itemSelectionChanged.connect(self.handle_tree_selection)
        self.butRefreshTree.clicked.connect(self.populate_wfTree)
        self.buttonConvertMattes.clicked.connect(self.convert_mattes_wrapper)
        # graph menu
        self.buttonViewAll.clicked.connect(lambda: self.graphView.plotItem.vb.autoRange())
        self.buttonPanMode.clicked.connect(lambda: self.graphView.plotItem.vb.setMouseMode(pg.ViewBox.PanMode))
        self.buttonZoomMode.clicked.connect(lambda: self.graphView.plotItem.vb.setMouseMode(pg.ViewBox.RectMode))

        
        # DEBUG page
        self.commandLineEdit.returnPressed.connect(self.send_command_line)
        self.buttonSend.clicked.connect(self.send_command_line)
        self.buttonHelp.clicked.connect(self.send_command_help)

        # Left Main menu
        self.stackedWidget = self.findChild(QWidget, "fMain")
        self.nav_buttons = [
            self.butConnect,  
            self.butMachineSetup,    
            self.butExperimentSetup,    
            self.butMeasure,  
            self.butView,     
            self.butDebug     
        ]
        self.stackedWidget.currentChanged.connect(self.pageChanged)
        # Connect buttons to switch pages by name
        self.butConnect.clicked.connect(lambda: self.switch_page("Connect", self.butConnect))
        self.butMachineSetup.clicked.connect(lambda: self.switch_page("MachineSetup", self.butMachineSetup))
        self.butExperimentSetup.clicked.connect(lambda: self.switch_page("ExperimentSetup", self.butExperimentSetup))
        self.butMeasure.clicked.connect(lambda: self.switch_page("Measure", self.butMeasure))
        self.butView.clicked.connect(lambda: self.switch_page("View", self.butView))
        self.butDebug.clicked.connect(lambda: self.switch_page("Debug", self.butDebug))
        self.butMachineSetup.setEnabled(False)
        self.butExperimentSetup.setEnabled(False)
        self.butMeasure.setEnabled(False)
        self.butDebug.setEnabled(False)
        self.switch_page("Connect", self.butConnect)

        # Add secret keyboard shortcut to trigger dummy_measurement()
        self.secret_shortcut = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_D), self)
        self.secret_shortcut.activated.connect(self.dummy_measurement)
        # dummy connect
        self.secret_shortcut_connect = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_C), self)
        self.secret_shortcut_connect.activated.connect(self.dummy_connect)

        # Bind widgets and variables to config
        # CONNECT page
        # serial_port save is in function "populate_serial_ports"
        # ToDo
        # serial_port load is in function "connect_serial"
        # MACHINE SETUP page
        self.config.bind_checkbox(self.lcEnable1, "machine setup.loadcell1.enable", default=True)
        self.config.bind_checkbox(self.lcEnable2, "machine setup.loadcell2.enable", default=True)
        self.config.bind_checkbox(self.lcEnable3, "machine setup.loadcell3.enable", default=True)
        # EXPERIMENT SETUP page
        # folder save is in function "select_folder"
        self.selected_folder = self.config.load("experiment setup.folder")
        self.labOutFolder.setText(self.selected_folder)
        # parameters
        self.config.bind_spinbox(self.numExperimentDistance,             "experiment setup.parameters.distance")
        self.config.bind_spinbox(self.numExperimentSpeed,                "experiment setup.parameters.speed")
        self.config.bind_spinbox(self.numExperimentForceDrop,            "experiment setup.parameters.force drop")
        self.config.bind_spinbox(self.numExperimentForceDropPercent,     "experiment setup.parameters.force drop percent")
        self.config.bind_spinbox(self.numExperimentSafeForce,            "experiment setup.parameters.safe force")
        self.config.bind_checkbox(self.checkBoxPhotosEnable,             "experiment setup.parameters.photos.enable")
        self.config.bind_spinbox(self.numPhotosFrequency,                "experiment setup.parameters.photos.frequency")
        # description    
        self.config.bind_lineedit(self.inputExperimentTitle,             "experiment setup.description.title")
        self.config.bind_lineedit(self.inputExperimentAuthor,            "experiment setup.description.author")
        self.config.bind_configtextedit(self.inputExperimentDescription, "experiment setup.description.description")


    def set_icons_manual(self):
        # set button icons
        # text to nothing
        self.buttonUp.setText("")
        self.buttonDown.setText("")
        self.buttonUp2.setText("")
        self.buttonDown2.setText("")
        arrow1 = QPixmap(resources["arrow_1.png"])
        arrow2 = QPixmap(resources["arrow_2.png"])
        # scale icons
        arrow1 = arrow1.scaled(40, 40)
        arrow2 = arrow2.scaled(50, 50)
        arrow1 = arrow1.transformed(QTransform().rotate(-90))
        arrow2 = arrow2.transformed(QTransform().rotate(-90))
        self.buttonUp.setIcon(QIcon(arrow1))
        self.buttonUp2.setIcon(QIcon(arrow2))
        arrow1 = arrow1.transformed(QTransform().rotate(180))
        arrow2 = arrow2.transformed(QTransform().rotate(180))
        self.buttonDown.setIcon(QIcon(arrow1))
        self.buttonDown2.setIcon(QIcon(arrow2))
        self.buttonUp.setIconSize(arrow1.size())
        self.buttonDown.setIconSize(arrow1.size())
        self.buttonUp2.setIconSize(arrow2.size())
        self.buttonDown2.setIconSize(arrow2.size())

    def pageChanged(self):
        """Update the button highlight when the page changes."""
        current_page = self.stackedWidget.currentWidget()
        page_name = current_page.objectName()
        if page_name == "Connect":
            self.populate_serial_ports()
        elif page_name == "ExperimentSetup":
            self.inputExperimentDate.setDateTime(QDateTime.currentDateTime())
        elif page_name == "View":
            self.populate_wfTree()

    def update_sample_index(self):
        self.SampleIndexManual = True
        self.buttonStart.setText("START")
        self.buttonSave.setText("SAVE")
    
    def ask_clear(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure to clear the graph?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.SampleIndexManual = True
            self.clear_graph()
            self.set_measurement_state("CLEAR")
            # do not increment sample index

    def clear_graph(self):
        self.graph_pos_data = self.INIT_POS_DATA.clone()
        self.draw_graph(clear=True)
        self.last_pos = 0

    def dummy_connect(self):
        self.graph_timer.start(50)  # draw graphs 20 Hz
        self.set_connection_status(True)
        self.butMachineSetup.setEnabled(True)
        self.butExperimentSetup.setEnabled(True)
        self.butMeasure.setEnabled(True)
        self.butDebug.setEnabled(True)
    
    def dummy_measurement(self):
        self.set_measurement_state("START")
        # dummy data
        self.graph_pos_data = pl.DataFrame({
            "time": pl.Series("time", [0, 1, 2], dtype=pl.Float64),
            "position": pl.Series("position", [1, 2, 3], dtype=pl.Float64),
            "loadcell1": pl.Series("loadcell1", [None, None, None], dtype=pl.Float64),
            "loadcell2": pl.Series("loadcell2", [0, 10, 13.4], dtype=pl.Float64),
            "loadcell3": pl.Series("loadcell3", [None, None, None], dtype=pl.Float64),
        })
        # dummy metadata
        self.maxExpForce = self.graph_pos_data["loadcell2"].max()
        # finish
        self.draw_graph()
        self.set_measurement_state("COMPLETED")

    def switch_page(self, page_name, active_button):
        """Switch QStackedWidget page by name."""
        target_page = self.findChild(QWidget, page_name)
        if target_page:
            self.stackedWidget.setCurrentWidget(target_page)

            # Reset all button colors
            for button in self.nav_buttons:
                button.setStyleSheet("")

            # Highlight the active button with a green tint
            active_button.setStyleSheet("background-color: lightgreen; color: black;")

    def start_moving(self, speed):
        """Start sending movement commands for UP or DOWN."""
        self.manual_speed = speed
        self.send_command(f"MC SET SPEEDMM {abs(speed)}")
        
        # ToDo change dist based on current velocity?
        self.move_timer.start(50)

    def stop_moving(self):
        """Stop sending movement commands."""
        self.move_timer.stop()
        self.send_command(f"MC STOP")

    def manual_movement_command(self):
        """Send manual movement commands."""
        DIST = 5
        vel_sign = 1 if self.manual_speed > 0 else -1
        self.send_command(f"MC MOVEBY USER {DIST * vel_sign}")

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
        # filter out "/dev/" ports
        ports = [port for port in ports if not port.device.startswith("/dev/")]
        for port in ports:
            self.serialPortSelection.addItem(port.device)
        if ports:
            # set selected as from config
            last_selected_port = self.config.load("serial.port")
            print(f"Last selected port: {last_selected_port}")
            print(f"ports: {ports}")
            if self.serialPortSelection.findText(last_selected_port):
                self.serialPortSelection.setCurrentText(last_selected_port)
            else:
                self.serialPortSelection.setCurrentIndex(0)
            self.buttonConnect.setEnabled(True)
        else:
            self.serialPortSelection.addItem("No serial ports found. Please connect a device.")
            self.buttonConnect.setEnabled(False)

    def connect_serial(self):
        """Connect to the selected serial port."""
        if self.connected:
            # Disconnect if already connected
            self.serial.close()
            self.serial_read_timer.stop()
            self.graph_timer.stop()
            self.set_connection_status(False)
        else:
            try:
                selected_port = self.serialPortSelection.currentText()
                self.serial = Serial(selected_port, baudrate=9600, timeout=1)
                self.serial.flush()
                self.serial_read_timer.start(10)  # Start reading every 10ms
                self.graph_timer.start(50)  # draw graphs 20 Hz
                self.set_connection_status(True)
                # save selected port to config
                self.config.save("serial.port", selected_port)
                # INIT COMMANDS
                self.send_command("DATAC 1")
                self.send_command("MC SET SPEEDMM 5")
                self.send_command("MC SET ACCEL 1000")
                # enable pages which require connection
                self.butMachineSetup.setEnabled(True)
                self.butExperimentSetup.setEnabled(True)
                self.butMeasure.setEnabled(True)
                self.butDebug.setEnabled(True)
                # ToDo use watchdog
                #self.send_command("MISC SET WATCHDOG_ENABLED 1")
            except Exception as e:
                self.set_connection_status(False)
                self.show_message(f"Failed to connect: {e}", error=True)

    def set_connection_status(self, status):
        """Update UI based on connection status."""
        self.connected = status
        if status:
            self.labelConnection.setText("Connected")
            self.buttonConnect.setText("Disconnect")
            self.labelConnection.setStyleSheet("background-color: green;")  # Set background to green
        else:
            self.labelConnection.setText("Disconnected")
            self.buttonConnect.setText("Connect")
            self.labelConnection.setStyleSheet("")
            self.butMachineSetup.setEnabled(False)
            self.butExperimentSetup.setEnabled(False)
            self.butMeasure.setEnabled(False)
            self.butDebug.setEnabled(False)

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

    def set_measurement_state(self, transition, comment=""):
        butStartText = "START" if self.SampleIndexManual else "START\nNEXT"
        self.buttonStart.setText(butStartText)
        if transition == "CLEAR":  # init
            self.measurement_state = "CLEAR"
            self.lMeasurementState.setText("Ready")
            self.lMeasurementState.setStyleSheet("")
            self.lMeasurementState2.setText("")
            self.buttonStart.setEnabled(True)
            self.buttonStop.setEnabled(False)
            self.buttonSave.setEnabled(False)
            self.buttonSave.setText("SAVE")
            self.buttonClear.setEnabled(False)
        elif transition == "READY":  # after saved
            self.measurement_state = "READY"
            self.lMeasurementState.setText("Ready")
            self.lMeasurementState.setStyleSheet("")
            self.lMeasurementState2.setText("")
            self.buttonStart.setEnabled(True)
            self.buttonStop.setEnabled(False)
            self.buttonSave.setEnabled(True)
            self.buttonSave.setText("SAVE\nAGAIN")
            self.buttonClear.setEnabled(True)
        elif transition == "MEASURING":  # measuring
            self.measurement_state = "MEASURING"
            self.lMeasurementState.setText("Measuring...")
            self.lMeasurementState.setStyleSheet("background-color: lightgreen;")
            self.lMeasurementState2.setText("Please wait...")
            self.buttonStart.setEnabled(False)
            self.buttonStop.setEnabled(True)
            self.buttonSave.setEnabled(False)
            self.buttonClear.setEnabled(False)
            self.lSaveState.setText("")
        elif transition == "COMPLETED":  # measurement completed
            self.measurement_state = "COMPLETED"
            self.lMeasurementState.setText("Completed")
            self.lMeasurementState.setStyleSheet("background-color: green;")
            self.lMeasurementState2.setText(comment)
            self.buttonStart.setEnabled(False)
            self.buttonStop.setEnabled(False)
            self.buttonSave.setEnabled(True)
            self.buttonSave.setText("SAVE")
            self.buttonClear.setEnabled(True)
        elif transition == "FAILED":  # measurement failed on some limit
            self.measurement_state = "FAILED"
            self.lMeasurementState.setText("Failed")
            self.lMeasurementState.setStyleSheet("background-color: lightred;")
            self.lMeasurementState2.setText(comment)
            self.buttonStart.setEnabled(False)
            self.buttonStop.setEnabled(False)
            self.buttonSave.setEnabled(True)
            self.buttonSave.setText("SAVE")
            self.buttonClear.setEnabled(True)

    def measurementStart(self):
        self.clear_graph()
        self.inputExperimentDate.setDateTime(QDateTime.currentDateTime())
        # increment sample index
        if self.SampleIndexManual:
            self.SampleIndexManual = False
        else:
            self.numSampleIndex.blockSignals(True)
            self.numSampleIndex.setValue(self.numSampleIndex.value() + 1)
            self.numSampleIndex.blockSignals(False)
            self.flash_background(self.numSampleIndex)
        # start experiment
        dist = self.numExperimentDistance.value()
        speed = self.numExperimentSpeed.value()
        max_force = self.numExperimentSafeForce.value()
        self.send_command_experiment_standard(dist, speed, max_force)
        # send command to start camera taking photos
        # ToDo
        self.set_measurement_state("MEASURING")

    def measurementStop(self):
        """ Manual stop of the experiment."""
        # stop experiment
        self.send_command("EXP STOP")
        # move to intial position
        self.send_command(f"MC MOVETO MACH {self.initial_exp_position}")
        # stop checkign timer
        self.exp_stop_timer.stop()
        # set state to stopped
        self.set_measurement_state("COMPLETED", "Stopped by user.")

    def saveExperimentData(self):
        if not self.selected_folder:
            self.select_folder()
        if not self.inputExperimentTitle.text():
            self.show_message("Please enter an experiment title.", error=True)
            # switch to experiment setup page
            self.switch_page("ExperimentSetup", self.butExperimentSetup)
            # focus on title input
            self.inputExperimentTitle.setFocus()
            return
        #Save data to CSV
        metadata = {
            "Title": self.inputExperimentTitle.text(),
            "Sample Index": self.numSampleIndex.value(),
            "Sample": self.inputExperimentSample.text(),
            "Author": self.inputExperimentAuthor.text(),
            "Date": self.inputExperimentDate.text(),
            "Description": self.inputExperimentDescription.toPlainText(),
            "Notes": self.inputExperimentNotes.toPlainText(),
            "Speed": self.numExperimentSpeed.value(),
            "Max force": self.maxExpForce
            }
        filename = f"{self.inputExperimentTitle.text()}_{self.numSampleIndex.value()}.csv"
        self.save_to_csv(
            self.graph_pos_data,
            self.selected_folder,
            filename,
            metadata)
        self.lSaveState.setText(f"Saved to {filename}")
        self.set_measurement_state("READY")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:  # If user selected a folder
            self.selected_folder = folder
            self.config.save("experiment setup.folder", folder)
            self.labOutFolder.setText(folder)

    def save_to_csv(self, pos_data, folder, filename, metadata):
        """
        Saves position-based data for load cells to a CSV file.

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
        # check for overwrite
        if os.path.exists(filepath):
            reply = QMessageBox.question(self, 'Message', f"File already exists.\n{filename}\nDo you want to overwrite it?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write metadata at the top
            for key, value in metadata.items():
                writer.writerow([key, value])
            writer.writerow([])  # Empty row to separate metadata from data

            # Write data with polars
            # Keep only the columns that are enabled
            enabled_cols = ["time", "position"]
            if self.lcEnable1.isChecked():
                enabled_cols.append("loadcell1")
            if self.lcEnable2.isChecked():
                enabled_cols.append("loadcell2")
            if self.lcEnable3.isChecked():
                enabled_cols.append("loadcell3")
            self.graph_pos_data = self.graph_pos_data.select(enabled_cols)
            # Fill null values with 0
            print(self.graph_pos_data)
            self.graph_pos_data = self.graph_pos_data.with_columns(pl.all().cast(pl.Float64))
            self.graph_pos_data = self.graph_pos_data.fill_null(0)
            print(self.graph_pos_data)
            writer.writerow(self.graph_pos_data.columns)
            writer.writerows(self.graph_pos_data.iter_rows())
            self.flash_background(self.lSaveState)

        print(f"Data saved successfully to {filepath}")

    def convert_mattes_wrapper(self):
        # convert all selected csv files to MATTES
        if not self.selected_folder:
            self.show_message("Please select a folder first.", error=True)
            return
        # check for overwrite
        output_excel_path = os.path.join(self.selected_folder, f"{self.inputExperimentTitle.text()}_mattes.xlsx")
        if os.path.exists(output_excel_path):
            reply = QMessageBox.question(self, 'Message', f"File already exists.\n{output_excel_path}\nDo you want to overwrite it?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        # generate input CSV files
        csv_files = []
        for item in self.wfTree.selectedItems():
            item_path = item.data(0, Qt.ItemDataRole.UserRole)
            if os.path.isfile(item_path):
                csv_files.append(item_path)
        # do the conversion
        convert_mattes(csv_files, output_excel_path)
        # update ui
        self.flash_background(self.buttonConvertMattes)
        self.populate_wfTree()


    def flash_background(self, widget, flash_color="lightgreen", flash_duration=0, fade_duration=1000):
        # Uložíme původní barvu widgetu
        default_color = widget.palette().color(widget.backgroundRole())
        
        # Nastavíme flash barvu
        widget.setStyleSheet(f"background-color: {flash_color};")

        # Počkej a pak spusť vyblednutí
        def start_fade():
            start = QColor(flash_color)
            end = default_color

            anim = QVariantAnimation(
                startValue=start,
                endValue=end,
                duration=fade_duration,
                easingCurve=QEasingCurve.Type.InOutQuad
            )

            def update_bg(color):
                rgba = color.name(QColor.NameFormat.HexArgb)
                widget.setStyleSheet(f"background-color: {rgba};")

            def clear_style():
                widget.setStyleSheet("")

            anim.valueChanged.connect(update_bg)
            anim.finished.connect(clear_style)
            anim.start()

            # Zabránit garbage collectu
            widget._flash_anim = anim

        QTimer.singleShot(flash_duration, start_fade)

    def send_command_help(self):
        self.send_command("HELP")

    def send_command_home(self):
        self.send_command("MC CALIBRATE")

    def send_command_tare(self, lc_num):
        self.send_command(f"LC TARE {lc_num - 1}")

    def check_experiment_stop(self):
        if self.currentForce < self.maxExpForce * (1 - self.numExperimentForceDropPercent.value()/100) and self.currentForce > self.numExperimentForceDrop.value():
            self.send_command("EXP STOP")
            self.send_command(f"MC MOVETO MACH {self.initial_exp_position}")
            self.set_measurement_state("COMPLETED", f"Force dropped by {self.numExperimentForceDropPercent.value()}%")
            self.exp_stop_timer.stop()

    def send_command_experiment_standard(self, dist, speed, max_force):
        # save initial position
        self.initial_exp_position = self.currentPos
        self.maxExpForce = 0
        # run experiment
        self.send_command(f"EXP STANDARD {dist} {speed} {max_force} 1 1 0")
        # stop experiment if force_decrease_to_stop is reached or max_force is reached or distance is reached
        # start timer to check experiment stop
        self.exp_stop_timer = QTimer()
        self.exp_stop_timer.timeout.connect(self.check_experiment_stop)
        self.exp_stop_timer.start(10)

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
                        x_data = self.graph_pos_data["position"].to_list()
                        y_data = self.graph_pos_data[f"loadcell{i+1}"].fill_null(0).to_list()  # Replace nulls with 0
                        #print(x_data, y_data)
                        if any(y_data):
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
                new_row = pl.DataFrame({
                    "time": [timestamp],
                    "position": [curPos],
                    "loadcell1": [loadcells[0]],
                    "loadcell2": [loadcells[1]],
                    "loadcell3": [loadcells[2]]
                })
                self.graph_pos_data = pl.concat([self.graph_pos_data, new_row])
            self.last_pos = curPos

            # bargraphs
            self.loadcell1.setValue(int(loadcells[0]))
            self.loadcell2.setValue(int(loadcells[1]))
            self.loadcell3.setValue(int(loadcells[2]))
            # values
            self.nLC1.setText(f"{loadcells[0]:.2f} N")
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
                    if line.startswith("DS"):  # Process machine data (DATAC)
                        # print(line)
                        line = line.strip()[2:]
                        data = line.split(",")
                        timestamp = data[0]
                        curPos = data[1]
                        self.currentPos = curPos
                        curVel = data[2]
                        loadcells = [- data[3], - data[4], - data[5]]
                        self.currentForce = loadcells[1]

                        # Convert from string to float for plotting
                        loadcells = [float(i) for i in loadcells]
                        self.update_graphdata(loadcells, timestamp, curPos)
                    # ToDo deal cases
                    # "limit distance reached" 
                    # "limit machine force reached"
                    # "limit experiment force reached"
                    elif line.startswith("Experiment stopped."):
                        self.set_measurement_state("FAILED", "????.")
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

    def populate_wfTree(self):
        """Populate wfTree with files and subfolders in the working directory."""

        if not self.selected_folder:
            self.show_message("Please select a folder first.", error=True)
            return

        # save currently selected items
        selected_paths = []
        for item in self.wfTree.selectedItems():
            path = item.data(0, Qt.ItemDataRole.UserRole)
            if path:
                selected_paths.append(path)

        self.wfTree.clear()

        def add_items(parent, path):
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    tree_item = QTreeWidgetItem(parent, [item])
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                    add_items(tree_item, item_path)
                elif item.endswith((".csv", ".xlsx")):
                    tree_item = QTreeWidgetItem(parent, [item])
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, item_path)

        # Refresh the tree with the selected folder
        root_item = QTreeWidgetItem(self.wfTree, [self.selected_folder])
        root_item.setData(0, Qt.ItemDataRole.UserRole, self.selected_folder)
        add_items(root_item, self.selected_folder)
        self.wfTree.expandAll()

        # try to restore selection
        def restore_selection(item):
            path = item.data(0, Qt.ItemDataRole.UserRole)
            if path in selected_paths:
                item.setSelected(True)
            for i in range(item.childCount()):
                restore_selection(item.child(i))

        restore_selection(root_item)

    def handle_tree_selection(self):
        """Ensure folder and file selection consistency based on user actions."""
        # selected_items = self.wfTree.selectedItems()
        # selected_paths = {item.data(0, Qt.ItemDataRole.UserRole) for item in selected_items}

        # # Track previous selection state
        # previously_selected = getattr(self, "_prev_selected_items", set())
        # currently_selected = set(selected_paths)

        # added_items = currently_selected - previously_selected
        # removed_items = previously_selected - currently_selected
        # print("Added items:")
        # print(added_items)
        # print("Removed items:")
        # print(removed_items)

        # def get_all_tree_items(self):
        #     """Recursively get all items in the QTreeWidget (wfTree)."""
        #     all_items = []
        #     root = self.wfTree.invisibleRootItem()

        #     def collect_items(parent):
        #         for i in range(parent.childCount()):
        #             child = parent.child(i)
        #             all_items.append(child)
        #             collect_items(child)  # Recurse into subfolders

        #     collect_items(root)
        #     return all_items
        
        # for item in get_all_tree_items(self):
        #     print(item)
        #     item_path = item.data(0, Qt.ItemDataRole.UserRole)
        #     print(item_path)

        #     if item_path in added_items:  # User just selected this
        #         if os.path.isdir(item_path):  # Folder selected
        #             print("Folder selected", item_path)
        #             # ToDo select everyhing recursively
        #             for i in range(item.childCount()):
        #                 child = item.child(i)
        #                 child.setSelected(True)
        #             # ToDo check siblings also?
        #         else:  # File selected, check if all siblings are selected
        #             print("File selected", item_path)
        #             parent = item.parent()
        #             if parent and all(parent.child(i).isSelected() for i in range(parent.childCount())):
        #                 parent.setSelected(True)

        #     elif item_path in removed_items:  # User just deselected this
        #         if os.path.isdir(item_path):  # Folder deselected
        #             print("Folder deselected", item_path)
        #             for i in range(item.childCount()):
        #                 child = item.child(i)
        #                 child.setSelected(False)
        #         else:  # File deselected, deselect parent if any file remains unselected
        #             print("File deselected", item_path)
        #             parent = item.parent()
        #             if parent:
        #                 if any(not parent.child(i).isSelected() for i in range(parent.childCount())):
        #                     parent.setSelected(False)

        # # Store the new selection state for future reference
        # self._prev_selected_items = set({item.data(0, Qt.ItemDataRole.UserRole) for item in selected_items})

        # Load files after updating selection
        self.load_selected_files()

    def load_selected_files(self):
        """Load selected CSV files, skipping metadata, and plot them."""
        selected_items = self.wfTree.selectedItems()
        if not selected_items:
            return
 
        self.graph_pos_data = self.INIT_POS_DATA.clone()  # Reset graph data
        self.graphView.clear()  # Clear previous plots
        self.graphView.addLegend()  # Ensure legend updates dynamically
 
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Different colors for each file
        color_index = 0
 
        for item in selected_items:
            file_path = item.data(0, Qt.ItemDataRole.UserRole)
            if not file_path.endswith(".csv"):
                continue  # Skip non-CSV files
 
            try:
                # Read file and find the correct header
                with open(file_path, 'r', newline='') as f:
                    lines = f.readlines()
 
                header_index = -1
                for i, line in enumerate(lines):
                    if "position" in line and ("loadcell1" in line or "loadcell2" in line or "loadcell3" in line):
                        header_index = i
                        break
 
                if header_index == -1:
                    self.show_message(f"Could not find data header in {file_path}", error=True)
                    continue
 
                # Read CSV starting from the header
                df = pl.read_csv(
                    file_path, 
                    skip_rows=header_index,  # Start reading from the header
                    truncate_ragged_lines=True  # Ensure inconsistent rows don't break parsing
                ).fill_null(0).cast(pl.Float64)
 
                # Check if necessary columns exist
                x_data = df["position"].to_list()
                file_name = os.path.basename(file_path)
 
                # for optional loadcell columns plot them
                for col in df.columns:
                    if col.startswith("loadcell"):
                        y_data = df[col].to_list()
                        color = colors[color_index % len(colors)]
                        self.graphView.plot(x_data, y_data, pen=pg.mkPen(color), name=f"{file_name} - {col}")
                        color_index += 1  # Cycle through colors
 
            except Exception as e:
                self.show_message(f"Failed to load {file_path}: {e}", error=True)


if __name__ == "__main__":

    appctxt = ApplicationContext()
    resources = {
        "design.ui": appctxt.get_resource("design.ui"),
        "arrow_1.png": appctxt.get_resource("arrow_1.png"),
        "arrow_2.png": appctxt.get_resource("arrow_2.png"),
    }
    window = TyhmosControlApp(resources)
    appctxt.app.setStyle("fusion")
    # window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec()
    sys.exit(exit_code)

    