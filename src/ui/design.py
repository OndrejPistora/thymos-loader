# Form implementation generated from reading ui file 'src/ui/design.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1018, 751)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(500, 500))
        self.centralwidget.setBaseSize(QtCore.QSize(1400, 1000))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 991, 1120))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.butConnect = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butConnect.sizePolicy().hasHeightForWidth())
        self.butConnect.setSizePolicy(sizePolicy)
        self.butConnect.setMinimumSize(QtCore.QSize(100, 100))
        self.butConnect.setObjectName("butConnect")
        self.verticalLayout.addWidget(self.butConnect)
        self.butMachineSetup = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butMachineSetup.sizePolicy().hasHeightForWidth())
        self.butMachineSetup.setSizePolicy(sizePolicy)
        self.butMachineSetup.setMinimumSize(QtCore.QSize(100, 100))
        self.butMachineSetup.setObjectName("butMachineSetup")
        self.verticalLayout.addWidget(self.butMachineSetup)
        self.butExperimentSetup = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butExperimentSetup.sizePolicy().hasHeightForWidth())
        self.butExperimentSetup.setSizePolicy(sizePolicy)
        self.butExperimentSetup.setMinimumSize(QtCore.QSize(100, 100))
        self.butExperimentSetup.setObjectName("butExperimentSetup")
        self.verticalLayout.addWidget(self.butExperimentSetup)
        self.butMeasure = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butMeasure.sizePolicy().hasHeightForWidth())
        self.butMeasure.setSizePolicy(sizePolicy)
        self.butMeasure.setMinimumSize(QtCore.QSize(100, 100))
        self.butMeasure.setObjectName("butMeasure")
        self.verticalLayout.addWidget(self.butMeasure)
        self.butView = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butView.sizePolicy().hasHeightForWidth())
        self.butView.setSizePolicy(sizePolicy)
        self.butView.setMinimumSize(QtCore.QSize(100, 100))
        self.butView.setObjectName("butView")
        self.verticalLayout.addWidget(self.butView)
        self.butDebug = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butDebug.sizePolicy().hasHeightForWidth())
        self.butDebug.setSizePolicy(sizePolicy)
        self.butDebug.setMinimumSize(QtCore.QSize(100, 100))
        self.butDebug.setObjectName("butDebug")
        self.verticalLayout.addWidget(self.butDebug)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.stackedWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.Connect = QtWidgets.QWidget()
        self.Connect.setObjectName("Connect")
        self.serialPortSelection = QtWidgets.QComboBox(parent=self.Connect)
        self.serialPortSelection.setGeometry(QtCore.QRect(220, 190, 200, 30))
        self.serialPortSelection.setObjectName("serialPortSelection")
        self.labelConnection = QtWidgets.QLabel(parent=self.Connect)
        self.labelConnection.setGeometry(QtCore.QRect(230, 260, 181, 20))
        self.labelConnection.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelConnection.setObjectName("labelConnection")
        self.buttonConnect = QtWidgets.QPushButton(parent=self.Connect)
        self.buttonConnect.setGeometry(QtCore.QRect(220, 220, 200, 30))
        self.buttonConnect.setObjectName("buttonConnect")
        self.butRefresh = QtWidgets.QPushButton(parent=self.Connect)
        self.butRefresh.setGeometry(QtCore.QRect(430, 190, 81, 32))
        self.butRefresh.setObjectName("butRefresh")
        self.stackedWidget.addWidget(self.Connect)
        self.MachineSetup = QtWidgets.QWidget()
        self.MachineSetup.setObjectName("MachineSetup")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.MachineSetup)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 20, 291, 591))
        self.groupBox_3.setObjectName("groupBox_3")
        self.line = QtWidgets.QFrame(parent=self.groupBox_3)
        self.line.setGeometry(QtCore.QRect(20, 300, 101, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.loadcell3 = QtWidgets.QProgressBar(parent=self.groupBox_3)
        self.loadcell3.setGeometry(QtCore.QRect(80, 40, 21, 531))
        self.loadcell3.setMinimum(-100)
        self.loadcell3.setProperty("value", 24)
        self.loadcell3.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.loadcell3.setObjectName("loadcell3")
        self.loadcell1 = QtWidgets.QProgressBar(parent=self.groupBox_3)
        self.loadcell1.setGeometry(QtCore.QRect(40, 40, 21, 531))
        self.loadcell1.setMinimum(-100)
        self.loadcell1.setProperty("value", 0)
        self.loadcell1.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.loadcell1.setObjectName("loadcell1")
        self.buttonTare1 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.buttonTare1.setGeometry(QtCore.QRect(120, 140, 131, 41))
        self.buttonTare1.setObjectName("buttonTare1")
        self.loadcell2 = QtWidgets.QProgressBar(parent=self.groupBox_3)
        self.loadcell2.setGeometry(QtCore.QRect(60, 40, 21, 531))
        self.loadcell2.setMinimum(-100)
        self.loadcell2.setProperty("value", 24)
        self.loadcell2.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.loadcell2.setObjectName("loadcell2")
        self.label = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(130, 300, 101, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(130, 380, 101, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(130, 460, 101, 21))
        self.label_3.setObjectName("label_3")
        self.nLC1 = QtWidgets.QLCDNumber(parent=self.groupBox_3)
        self.nLC1.setGeometry(QtCore.QRect(130, 330, 101, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, brush)
        self.nLC1.setPalette(palette)
        self.nLC1.setObjectName("nLC1")
        self.nLC2 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.nLC2.setGeometry(QtCore.QRect(130, 410, 101, 21))
        self.nLC2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.nLC2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.nLC2.setObjectName("nLC2")
        self.nLC3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.nLC3.setGeometry(QtCore.QRect(130, 490, 101, 21))
        self.nLC3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.nLC3.setObjectName("nLC3")
        self.buttonTare2 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.buttonTare2.setGeometry(QtCore.QRect(120, 180, 131, 41))
        self.buttonTare2.setObjectName("buttonTare2")
        self.buttonTare3 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.buttonTare3.setGeometry(QtCore.QRect(120, 220, 131, 41))
        self.buttonTare3.setObjectName("buttonTare3")
        self.checkBox = QtWidgets.QCheckBox(parent=self.groupBox_3)
        self.checkBox.setGeometry(QtCore.QRect(130, 50, 141, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.groupBox_3)
        self.checkBox_2.setGeometry(QtCore.QRect(130, 70, 141, 20))
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(parent=self.groupBox_3)
        self.checkBox_3.setGeometry(QtCore.QRect(130, 90, 141, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.buttonHome = QtWidgets.QPushButton(parent=self.MachineSetup)
        self.buttonHome.setGeometry(QtCore.QRect(400, 60, 101, 91))
        self.buttonHome.setObjectName("buttonHome")
        self.stackedWidget.addWidget(self.MachineSetup)
        self.ExperimentSetup = QtWidgets.QWidget()
        self.ExperimentSetup.setObjectName("ExperimentSetup")
        self.groupBox = QtWidgets.QGroupBox(parent=self.ExperimentSetup)
        self.groupBox.setGeometry(QtCore.QRect(40, 50, 121, 241))
        self.groupBox.setObjectName("groupBox")
        self.buttonUp = QtWidgets.QPushButton(parent=self.groupBox)
        self.buttonUp.setGeometry(QtCore.QRect(10, 30, 101, 91))
        self.buttonUp.setObjectName("buttonUp")
        self.buttonDown = QtWidgets.QPushButton(parent=self.groupBox)
        self.buttonDown.setGeometry(QtCore.QRect(10, 130, 101, 91))
        self.buttonDown.setObjectName("buttonDown")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.ExperimentSetup)
        self.groupBox_4.setGeometry(QtCore.QRect(220, 50, 221, 311))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.groupBox_4)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 201, 261))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_17 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_3.addWidget(self.label_17)
        self.numExperimentDistance = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget_2)
        self.numExperimentDistance.setDecimals(0)
        self.numExperimentDistance.setObjectName("numExperimentDistance")
        self.verticalLayout_3.addWidget(self.numExperimentDistance)
        self.label_18 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_3.addWidget(self.label_18)
        self.numExperimentSpeed = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget_2)
        self.numExperimentSpeed.setDecimals(0)
        self.numExperimentSpeed.setObjectName("numExperimentSpeed")
        self.verticalLayout_3.addWidget(self.numExperimentSpeed)
        self.label_19 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_3.addWidget(self.label_19)
        self.numExperimentSafeForce = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget_2)
        self.numExperimentSafeForce.setProperty("showGroupSeparator", False)
        self.numExperimentSafeForce.setDecimals(0)
        self.numExperimentSafeForce.setMaximum(1000.0)
        self.numExperimentSafeForce.setObjectName("numExperimentSafeForce")
        self.verticalLayout_3.addWidget(self.numExperimentSafeForce)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.groupBox_5 = QtWidgets.QGroupBox(parent=self.ExperimentSetup)
        self.groupBox_5.setGeometry(QtCore.QRect(480, 40, 331, 461))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.groupBox_5)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 311, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_12 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_2.addWidget(self.label_12)
        self.inputExperimentTitle = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.inputExperimentTitle.setObjectName("inputExperimentTitle")
        self.verticalLayout_2.addWidget(self.inputExperimentTitle)
        self.label_13 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        self.inputExperimentAuthor = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.inputExperimentAuthor.setObjectName("inputExperimentAuthor")
        self.verticalLayout_2.addWidget(self.inputExperimentAuthor)
        self.label_14 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_2.addWidget(self.label_14)
        self.inputExperimentDate = QtWidgets.QDateTimeEdit(parent=self.verticalLayoutWidget)
        self.inputExperimentDate.setEnabled(False)
        self.inputExperimentDate.setObjectName("inputExperimentDate")
        self.verticalLayout_2.addWidget(self.inputExperimentDate)
        self.label_16 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_2.addWidget(self.label_16)
        self.inputExperimentDescription = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.inputExperimentDescription.setObjectName("inputExperimentDescription")
        self.verticalLayout_2.addWidget(self.inputExperimentDescription)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.ExperimentSetup)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 420, 381, 191))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.groupBox_2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 40, 331, 131))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.labOutFolder = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        self.labOutFolder.setObjectName("labOutFolder")
        self.verticalLayout_5.addWidget(self.labOutFolder)
        self.butOutSelectFolder = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.butOutSelectFolder.setMaximumSize(QtCore.QSize(200, 16777215))
        self.butOutSelectFolder.setObjectName("butOutSelectFolder")
        self.verticalLayout_5.addWidget(self.butOutSelectFolder)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.stackedWidget.addWidget(self.ExperimentSetup)
        self.Measure = QtWidgets.QWidget()
        self.Measure.setObjectName("Measure")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.Measure)
        self.tabWidget.setGeometry(QtCore.QRect(10, 60, 611, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.graphTimeBased = PlotWidget(parent=self.tab)
        self.graphTimeBased.setGeometry(QtCore.QRect(10, 10, 561, 481))
        self.graphTimeBased.setObjectName("graphTimeBased")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.graphPosBased = PlotWidget(parent=self.tab_3)
        self.graphPosBased.setGeometry(QtCore.QRect(10, 10, 561, 481))
        self.graphPosBased.setObjectName("graphPosBased")
        self.tabWidget.addTab(self.tab_3, "")
        self.label_11 = QtWidgets.QLabel(parent=self.Measure)
        self.label_11.setGeometry(QtCore.QRect(650, 60, 121, 16))
        self.label_11.setObjectName("label_11")
        self.lMeasurementState = QtWidgets.QLabel(parent=self.Measure)
        self.lMeasurementState.setGeometry(QtCore.QRect(650, 90, 121, 16))
        self.lMeasurementState.setObjectName("lMeasurementState")
        self.testSuccess = QtWidgets.QPushButton(parent=self.Measure)
        self.testSuccess.setGeometry(QtCore.QRect(770, 430, 101, 91))
        self.testSuccess.setObjectName("testSuccess")
        self.label_15 = QtWidgets.QLabel(parent=self.Measure)
        self.label_15.setGeometry(QtCore.QRect(650, 530, 309, 16))
        self.label_15.setObjectName("label_15")
        self.inputExperimentNotes = QtWidgets.QTextEdit(parent=self.Measure)
        self.inputExperimentNotes.setGeometry(QtCore.QRect(640, 560, 309, 81))
        self.inputExperimentNotes.setObjectName("inputExperimentNotes")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.Measure)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 581, 26))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.numSampleIndex = QtWidgets.QSpinBox(parent=self.horizontalLayoutWidget_2)
        self.numSampleIndex.setMinimumSize(QtCore.QSize(80, 0))
        self.numSampleIndex.setMaximum(9999)
        self.numSampleIndex.setProperty("value", 1)
        self.numSampleIndex.setObjectName("numSampleIndex")
        self.horizontalLayout_2.addWidget(self.numSampleIndex)
        self.label_8 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.inputExperimentSample = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget_2)
        self.inputExperimentSample.setObjectName("inputExperimentSample")
        self.horizontalLayout_2.addWidget(self.inputExperimentSample)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.Measure)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(660, 130, 101, 361))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.buttonStartStop = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonStartStop.sizePolicy().hasHeightForWidth())
        self.buttonStartStop.setSizePolicy(sizePolicy)
        self.buttonStartStop.setMinimumSize(QtCore.QSize(100, 100))
        self.buttonStartStop.setObjectName("buttonStartStop")
        self.verticalLayout_4.addWidget(self.buttonStartStop)
        self.butExport = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.butExport.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butExport.sizePolicy().hasHeightForWidth())
        self.butExport.setSizePolicy(sizePolicy)
        self.butExport.setMinimumSize(QtCore.QSize(100, 100))
        self.butExport.setObjectName("butExport")
        self.verticalLayout_4.addWidget(self.butExport)
        self.butClear = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.butClear.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.butClear.sizePolicy().hasHeightForWidth())
        self.butClear.setSizePolicy(sizePolicy)
        self.butClear.setMinimumSize(QtCore.QSize(100, 100))
        self.butClear.setObjectName("butClear")
        self.verticalLayout_4.addWidget(self.butClear)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.stackedWidget.addWidget(self.Measure)
        self.View = QtWidgets.QWidget()
        self.View.setObjectName("View")
        self.wfTree = QtWidgets.QTreeWidget(parent=self.View)
        self.wfTree.setGeometry(QtCore.QRect(10, 20, 141, 661))
        self.wfTree.setObjectName("wfTree")
        self.wfTree.headerItem().setText(0, "1")
        self.tabWidget_2 = QtWidgets.QTabWidget(parent=self.View)
        self.tabWidget_2.setGeometry(QtCore.QRect(170, 20, 681, 611))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 631, 551))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.graphView = PlotWidget(parent=self.tab_4)
        self.graphView.setGeometry(QtCore.QRect(30, 20, 621, 541))
        self.graphView.setObjectName("graphView")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.stackedWidget.addWidget(self.View)
        self.Debug = QtWidgets.QWidget()
        self.Debug.setObjectName("Debug")
        self.buttonSend = QtWidgets.QPushButton(parent=self.Debug)
        self.buttonSend.setGeometry(QtCore.QRect(480, 500, 101, 41))
        self.buttonSend.setObjectName("buttonSend")
        self.commandLineEdit = QtWidgets.QLineEdit(parent=self.Debug)
        self.commandLineEdit.setGeometry(QtCore.QRect(0, 510, 471, 21))
        self.commandLineEdit.setObjectName("commandLineEdit")
        self.commandLineOutput = QtWidgets.QTextBrowser(parent=self.Debug)
        self.commandLineOutput.setGeometry(QtCore.QRect(0, 10, 661, 481))
        self.commandLineOutput.setObjectName("commandLineOutput")
        self.buttonHelp = QtWidgets.QPushButton(parent=self.Debug)
        self.buttonHelp.setGeometry(QtCore.QRect(580, 500, 91, 41))
        self.buttonHelp.setObjectName("buttonHelp")
        self.stackedWidget.addWidget(self.Debug)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1018, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.butConnect.setText(_translate("MainWindow", "Connect"))
        self.butMachineSetup.setText(_translate("MainWindow", "Machine\n"
"Setup"))
        self.butExperimentSetup.setText(_translate("MainWindow", "Experiment\n"
"Setup"))
        self.butMeasure.setText(_translate("MainWindow", "Measure"))
        self.butView.setText(_translate("MainWindow", "View"))
        self.butDebug.setText(_translate("MainWindow", "Debug"))
        self.labelConnection.setText(_translate("MainWindow", "TextLabel"))
        self.buttonConnect.setText(_translate("MainWindow", "Connect"))
        self.butRefresh.setText(_translate("MainWindow", "Refresh"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Loadcell settings"))
        self.buttonTare1.setText(_translate("MainWindow", "Tare loadcell 1"))
        self.label.setText(_translate("MainWindow", "Loadcell 1"))
        self.label_2.setText(_translate("MainWindow", "Loadcell 2"))
        self.label_3.setText(_translate("MainWindow", "Loadcell 3"))
        self.nLC2.setText(_translate("MainWindow", "0 N"))
        self.nLC3.setText(_translate("MainWindow", "0 N"))
        self.buttonTare2.setText(_translate("MainWindow", "Tare loadcell 2"))
        self.buttonTare3.setText(_translate("MainWindow", "Tare loadcell 3"))
        self.checkBox.setText(_translate("MainWindow", "Enable loadcell 1"))
        self.checkBox_2.setText(_translate("MainWindow", "Enable loadcell 2"))
        self.checkBox_3.setText(_translate("MainWindow", "Enable loadcell 3"))
        self.buttonHome.setText(_translate("MainWindow", "Home"))
        self.groupBox.setTitle(_translate("MainWindow", "Machine controls"))
        self.buttonUp.setText(_translate("MainWindow", "UP"))
        self.buttonDown.setText(_translate("MainWindow", "DOWN"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Experiment parameters"))
        self.label_17.setText(_translate("MainWindow", "Distance"))
        self.numExperimentDistance.setSuffix(_translate("MainWindow", " mm"))
        self.label_18.setText(_translate("MainWindow", "Speed"))
        self.numExperimentSpeed.setSuffix(_translate("MainWindow", " mm/s"))
        self.label_19.setText(_translate("MainWindow", "Safe maximum force"))
        self.numExperimentSafeForce.setSuffix(_translate("MainWindow", " N"))
        self.groupBox_5.setTitle(_translate("MainWindow", " Experiment description"))
        self.label_12.setText(_translate("MainWindow", "Experiment title"))
        self.label_13.setText(_translate("MainWindow", "Author"))
        self.label_14.setText(_translate("MainWindow", "Date"))
        self.inputExperimentDate.setDisplayFormat(_translate("MainWindow", "yyyy_MM_dd H:mm:ss"))
        self.label_16.setText(_translate("MainWindow", "Description"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Export and View folder"))
        self.label_4.setText(_translate("MainWindow", "Selected folder:"))
        self.labOutFolder.setText(_translate("MainWindow", "None"))
        self.butOutSelectFolder.setText(_translate("MainWindow", "Select folder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Time based graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Position based graph"))
        self.label_11.setText(_translate("MainWindow", "Meaurement state:"))
        self.lMeasurementState.setText(_translate("MainWindow", "ready"))
        self.testSuccess.setText(_translate("MainWindow", "Finish"))
        self.label_15.setText(_translate("MainWindow", "Notes"))
        self.label_10.setText(_translate("MainWindow", "Sample index"))
        self.label_8.setText(_translate("MainWindow", "Sample"))
        self.buttonStartStop.setText(_translate("MainWindow", "Start"))
        self.butExport.setText(_translate("MainWindow", "Export"))
        self.butClear.setText(_translate("MainWindow", "Clear"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("MainWindow", "Tab 1"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Tab 2"))
        self.buttonSend.setText(_translate("MainWindow", "-> Send"))
        self.buttonHelp.setText(_translate("MainWindow", "Help"))
from pyqtgraph import PlotWidget
