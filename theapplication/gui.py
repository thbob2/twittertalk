# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mywindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
MAIN_WIN = """QMainWindow{
    border: 2px solid grey;
    border-radius: 4px;
    background-color: #24292E;
    QLabel{
    color:#15c0ef;
    }
    QMessageBox QLabel{
    color:#ffffff;
    }
}   

"""
GRPB=""" QGroupBox{
     border:2px solid grey;
     border-radius:5px;
     color: #15c0ef;
     text-align: left;
     background-color: #24292E;
}
"""
TVIEW="""
    QTableView{
    border:2px solid grey;
    border-radius: 4px;
    background-color: #E6ECF0
    }
    QTreeView{
    border:2px solid grey;
    background-color: #E6ECF0;
    border-radius: 4px
    } 
"""
TABW=""" 
    QTabWidget::pane {
    border: 1px solid black;
    background: #24292E;
 }

    QTabWidget::tab-bar:top {
        top: 1px;
    }

    QTabWidget::tab-bar:bottom {
        bottom: 1px;
    }

    QTabWidget::tab-bar:left {
        right: 1px;
    }

    QTabWidget::tab-bar:right {
        left: 1px;
    }

    QTabBar::tab {
        border: 1px solid black;
    }

    QTabBar::tab:selected {
        background: white;
    }

    QTabBar::tab:!selected {
        background: silver;
    }

    QTabBar::tab:!selected:hover {
        background: #999;
    }

    QTabBar::tab:top:!selected {
        margin-top: 3px;
    }

    QTabBar::tab:bottom:!selected {
        margin-bottom: 3px;
    }

    QTabBar::tab:top, QTabBar::tab:bottom {
        min-width: 8ex;
        margin-right: -1px;
        padding: 5px 10px 5px 10px;
    }

    QTabBar::tab:top:selected {
        border-bottom-color: none;
    }

    QTabBar::tab:bottom:selected {
        border-top-color: none;
    }

    QTabBar::tab:top:last, QTabBar::tab:bottom:last,
    QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
        margin-right: 0;
    }

    QTabBar::tab:left:!selected {
        margin-right: 3px;
    }

    QTabBar::tab:right:!selected {
        margin-left: 3px;
    }

    QTabBar::tab:left, QTabBar::tab:right {
        min-height: 8ex;
        margin-bottom: -1px;
        padding: 10px 5px 10px 5px;
    }

    QTabBar::tab:left:selected {
        border-left-color: none;
    }

    QTabBar::tab:right:selected {
        border-right-color: none;
    }

    QTabBar::tab:left:last, QTabBar::tab:right:last,
    QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
        margin-bottom: 0;
    }
    QTabWidget::chunk{
         background-color:  #24292E;
    }
    QWidgets{
        border:2px solid grey;
        border-radius:3px;
        background-color: #4EC3DD;
    }
    QWidgets::chunk{
        background-color:  #24292E;
}
"""
BLUE_BAR = """QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: #0565d9;
    width: 10px;
    border-radius: 4px;
}
"""
RED_BAR = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: #af0d0d;
    width: 10px;
    border-radius: 4px;
}
"""
LOADB = """ QProgressBar{
    border: 2px solid grey;
    text-align: centre
}
QProgressBar::chunk {
    background-color: #4ec3dd;
    width: 10px;
 
}
"""
STATSLAB=""" QLabel{
    color: #ffffff
}

"""
LAB = """
    QLabel{
    color:#15c0ef;
    }
"""
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1079, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadLab = QtWidgets.QLabel(self.centralwidget)
        self.loadLab.setText("")
        self.loadLab.setObjectName("loadLab")
        self.horizontalLayout.addWidget(self.loadLab)
        self.LoadBar = QtWidgets.QProgressBar(self.centralwidget)
        self.LoadBar.setMaximumSize(QtCore.QSize(16777203, 15))
        self.LoadBar.setProperty("value", 0)
        self.LoadBar.setObjectName("LoadBar")
        self.horizontalLayout.addWidget(self.LoadBar)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(106, 111))
        self.groupBox.setMaximumSize(QtCore.QSize(200, 16777180))
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.MyTree = QtWidgets.QTreeView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MyTree.sizePolicy().hasHeightForWidth())
        self.MyTree.setSizePolicy(sizePolicy)
        self.MyTree.setMaximumSize(QtCore.QSize(1700, 16777199))
        self.MyTree.setMouseTracking(True)
        self.MyTree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.MyTree.setAutoFillBackground(True)
        self.MyTree.setFrameShape(QtWidgets.QFrame.Panel)
        self.MyTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.MyTree.setDragEnabled(False)
        self.MyTree.setAlternatingRowColors(True)
        self.MyTree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.MyTree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.MyTree.setAutoExpandDelay(1)
        self.MyTree.setIndentation(20)
        self.MyTree.setRootIsDecorated(True)
        self.MyTree.setUniformRowHeights(True)
        self.MyTree.setSortingEnabled(True)
        self.MyTree.setAnimated(True)
        self.MyTree.setAllColumnsShowFocus(True)
        self.MyTree.setObjectName("MyTree")
        self.MyTree.header().setVisible(False)
        self.MyTree.header().setCascadingSectionResizes(True)
        self.MyTree.header().setDefaultSectionSize(200)
        self.MyTree.header().setHighlightSections(False)
        self.MyTree.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.MyTree, 3, 0, 1, 1)
        self.ModelsBox = QtWidgets.QComboBox(self.groupBox)
        self.ModelsBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ModelsBox.sizePolicy().hasHeightForWidth())
        self.ModelsBox.setSizePolicy(sizePolicy)
        self.ModelsBox.setMinimumSize(QtCore.QSize(35, 44))
        self.ModelsBox.setMouseTracking(True)
        self.ModelsBox.setFrame(True)
        self.ModelsBox.setObjectName("ModelsBox")
        self.gridLayout.addWidget(self.ModelsBox, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(60, 60))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab1 = QtWidgets.QWidget()
        self.Tab1.setAutoFillBackground(True)
        self.Tab1.setObjectName("Tab1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Tab1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.CP = QtWidgets.QRadioButton(self.Tab1)
        self.CP.setObjectName("CP")
        self.gridLayout_3.addWidget(self.CP, 6, 0, 1, 1)
        self.NB = QtWidgets.QRadioButton(self.Tab1)
        self.NB.setObjectName("NB")
        self.gridLayout_3.addWidget(self.NB, 7, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.Tab1)
        self.tableView.setMouseTracking(True)
        self.tableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableView.setAutoFillBackground(True)
        self.tableView.setInputMethodHints(QtCore.Qt.ImhPreferLatin)
        self.tableView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableView.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableView.setLineWidth(0)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setProperty("showDropIndicator", False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setGridStyle(QtCore.Qt.SolidLine)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setDefaultSectionSize(150)
        self.tableView.horizontalHeader().setMinimumSectionSize(100)
        self.tableView.horizontalHeader().setSortIndicatorShown(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.tableView, 0, 0, 1, 6)
        self.groupBox_2 = QtWidgets.QGroupBox(self.Tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(500, 500))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.posBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.posBar.setProperty("value", 0)
        self.posBar.setObjectName("posBar")
        self.verticalLayout.addWidget(self.posBar)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.negBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.negBar.setProperty("value", 0)
        self.negBar.setObjectName("negBar")
        self.verticalLayout.addWidget(self.negBar)
        self.gridLayout_3.addWidget(self.groupBox_2, 4, 4, 9, 2)
        self.choiceBox = QtWidgets.QCheckBox(self.Tab1)
        self.choiceBox.setObjectName("choiceBox")
        self.gridLayout_3.addWidget(self.choiceBox, 8, 0, 1, 1)
        self.SearchBtn = QtWidgets.QPushButton(self.Tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBtn.sizePolicy().hasHeightForWidth())
        self.SearchBtn.setSizePolicy(sizePolicy)
        self.SearchBtn.setObjectName("SearchBtn")
        self.gridLayout_3.addWidget(self.SearchBtn, 6, 1, 1, 1)
        self.showtweetsbtn = QtWidgets.QPushButton(self.Tab1)
        self.showtweetsbtn.setObjectName("showtweetsbtn")
        self.gridLayout_3.addWidget(self.showtweetsbtn, 6, 2, 1, 1)
        self.refrechBtn = QtWidgets.QPushButton(self.Tab1)
        self.refrechBtn.setObjectName("refrechBtn")
        self.gridLayout_3.addWidget(self.refrechBtn, 7, 1, 1, 1)
        self.saveBtn = QtWidgets.QPushButton(self.Tab1)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout_3.addWidget(self.saveBtn, 7, 2, 1, 1)
        self.tableView.raise_()
        self.groupBox_2.raise_()
        self.CP.raise_()
        self.NB.raise_()
        self.choiceBox.raise_()
        self.SearchBtn.raise_()
        self.showtweetsbtn.raise_()
        self.refrechBtn.raise_()
        self.saveBtn.raise_()
        self.tabWidget.addTab(self.Tab1, "")
        self.Tab2 = QtWidgets.QWidget()
        self.Tab2.setObjectName("Tab2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Tab2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QtCore.QSize(400, 300))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SavedModels = QtWidgets.QComboBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SavedModels.sizePolicy().hasHeightForWidth())
        self.SavedModels.setSizePolicy(sizePolicy)
        self.SavedModels.setMinimumSize(QtCore.QSize(200, 30))
        self.SavedModels.setMaximumSize(QtCore.QSize(500, 400))
        self.SavedModels.setObjectName("SavedModels")
        self.verticalLayout_3.addWidget(self.SavedModels)
        self.LoadBtn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadBtn.sizePolicy().hasHeightForWidth())
        self.LoadBtn.setSizePolicy(sizePolicy)
        self.LoadBtn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.LoadBtn.setObjectName("LoadBtn")
        self.verticalLayout_3.addWidget(self.LoadBtn)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.posBar_2 = QtWidgets.QProgressBar(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posBar_2.sizePolicy().hasHeightForWidth())
        self.posBar_2.setSizePolicy(sizePolicy)
        self.posBar_2.setMaximumSize(QtCore.QSize(250, 300))
        self.posBar_2.setProperty("value", 0)
        self.posBar_2.setObjectName("posBar_2")
        self.verticalLayout_3.addWidget(self.posBar_2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.negBar_2 = QtWidgets.QProgressBar(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.negBar_2.sizePolicy().hasHeightForWidth())
        self.negBar_2.setSizePolicy(sizePolicy)
        self.negBar_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.negBar_2.setProperty("value", 0)
        self.negBar_2.setObjectName("negBar_2")
        self.verticalLayout_3.addWidget(self.negBar_2)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.Loaded = QtWidgets.QTableView(self.Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Loaded.sizePolicy().hasHeightForWidth())
        self.Loaded.setSizePolicy(sizePolicy)
        self.Loaded.setMinimumSize(QtCore.QSize(5, 0))
        self.Loaded.setMouseTracking(True)
        self.Loaded.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Loaded.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Loaded.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Loaded.setObjectName("Loaded")
        self.Loaded.horizontalHeader().setCascadingSectionResizes(True)
        self.Loaded.horizontalHeader().setSortIndicatorShown(True)
        self.Loaded.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.Loaded)
        self.tabWidget.addTab(self.Tab2, "")
        self.Tab3 = QtWidgets.QWidget()
        self.Tab3.setObjectName("Tab3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Tab3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.Tab3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMaximumSize(QtCore.QSize(600, 200))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setMaximumSize(QtCore.QSize(120, 20))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setMaximumSize(QtCore.QSize(120, 18))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_6)
        self.histModlesBox = QtWidgets.QComboBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histModlesBox.sizePolicy().hasHeightForWidth())
        self.histModlesBox.setSizePolicy(sizePolicy)
        self.histModlesBox.setMinimumSize(QtCore.QSize(250, 40))
        self.histModlesBox.setMaximumSize(QtCore.QSize(250, 40))
        self.histModlesBox.setObjectName("histModlesBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.histModlesBox)
        self.prod2 = QtWidgets.QComboBox(self.groupBox_4)
        self.prod2.setMinimumSize(QtCore.QSize(250, 40))
        self.prod2.setMaximumSize(QtCore.QSize(250, 40))
        self.prod2.setObjectName("prod2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.prod2)
        self.graphChoice = QtWidgets.QComboBox(self.groupBox_4)
        self.graphChoice.setMinimumSize(QtCore.QSize(100, 30))
        self.graphChoice.setEditable(False)
        self.graphChoice.setObjectName("graphChoice")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/both.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.graphChoice.addItem(icon1, "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.graphChoice.addItem(icon2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.graphChoice.addItem(icon3, "")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.graphChoice)
        self.showhisbtn = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showhisbtn.sizePolicy().hasHeightForWidth())
        self.showhisbtn.setSizePolicy(sizePolicy)
        self.showhisbtn.setMaximumSize(QtCore.QSize(100, 40))
        self.showhisbtn.setObjectName("showhisbtn")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.showhisbtn)
        self.saveGraph = QtWidgets.QPushButton(self.groupBox_4)
        self.saveGraph.setMinimumSize(QtCore.QSize(30, 30))
        self.saveGraph.setMaximumSize(QtCore.QSize(100, 25))
        self.saveGraph.setObjectName("saveGraph")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.saveGraph)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.HistLay = QtWidgets.QVBoxLayout()
        self.HistLay.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.HistLay.setSpacing(0)
        self.HistLay.setObjectName("HistLay")
        self.verticalLayout_2.addLayout(self.HistLay)
        self.tabWidget.addTab(self.Tab3, "")
        self.plotevo = QtWidgets.QWidget()
        self.plotevo.setObjectName("plotevo")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.plotevo)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.plotevo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(260, 180))
        self.groupBox_5.setMaximumSize(QtCore.QSize(400, 180))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_5)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QtCore.QSize(200, 20))
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.startDE = QtWidgets.QDateEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDE.sizePolicy().hasHeightForWidth())
        self.startDE.setSizePolicy(sizePolicy)
        self.startDE.setMinimumSize(QtCore.QSize(200, 30))
        self.startDE.setMaximumSize(QtCore.QSize(200, 30))
        self.startDE.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2018, 3, 9), QtCore.QTime(0, 0, 2)))
        self.startDE.setMinimumDate(QtCore.QDate(2018, 3, 9))
        self.startDE.setCalendarPopup(True)
        self.startDE.setObjectName("startDE")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.startDE)
        self.plotChoice = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotChoice.sizePolicy().hasHeightForWidth())
        self.plotChoice.setSizePolicy(sizePolicy)
        self.plotChoice.setMinimumSize(QtCore.QSize(100, 30))
        self.plotChoice.setMaximumSize(QtCore.QSize(150, 40))
        self.plotChoice.setObjectName("plotChoice")
        self.plotChoice.addItem(icon1, "")
        self.plotChoice.addItem(icon2, "")
        self.plotChoice.addItem(icon3, "")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.plotChoice)
        self.label_8 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMaximumSize(QtCore.QSize(200, 20))
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.endDE = QtWidgets.QDateEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endDE.sizePolicy().hasHeightForWidth())
        self.endDE.setSizePolicy(sizePolicy)
        self.endDE.setMinimumSize(QtCore.QSize(200, 30))
        self.endDE.setMaximumSize(QtCore.QSize(200, 30))
        self.endDE.setMinimumDate(QtCore.QDate(2018, 3, 9))
        self.endDE.setCalendarPopup(True)
        self.endDE.setObjectName("endDE")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.endDE)
        self.saveplot = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveplot.sizePolicy().hasHeightForWidth())
        self.saveplot.setSizePolicy(sizePolicy)
        self.saveplot.setMinimumSize(QtCore.QSize(150, 30))
        self.saveplot.setMaximumSize(QtCore.QSize(150, 30))
        self.saveplot.setObjectName("saveplot")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.saveplot)
        self.showp = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showp.sizePolicy().hasHeightForWidth())
        self.showp.setSizePolicy(sizePolicy)
        self.showp.setMinimumSize(QtCore.QSize(150, 30))
        self.showp.setMaximumSize(QtCore.QSize(150, 30))
        self.showp.setObjectName("showp")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.showp)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        self.pltlayot = QtWidgets.QVBoxLayout()
        self.pltlayot.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.pltlayot.setSpacing(0)
        self.pltlayot.setObjectName("pltlayot")
        self.verticalLayout_5.addLayout(self.pltlayot)
        self.tabWidget.addTab(self.plotevo, "")
        self.DbSettings = QtWidgets.QWidget()
        self.DbSettings.setObjectName("DbSettings")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.DbSettings)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.DbPicture = QtWidgets.QTableView(self.DbSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DbPicture.sizePolicy().hasHeightForWidth())
        self.DbPicture.setSizePolicy(sizePolicy)
        self.DbPicture.setMinimumSize(QtCore.QSize(800, 560))
        self.DbPicture.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.DbPicture.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.DbPicture.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.DbPicture.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.DbPicture.setObjectName("DbPicture")
        self.DbPicture.horizontalHeader().setDefaultSectionSize(150)
        self.DbPicture.horizontalHeader().setStretchLastSection(True)
        self.DbPicture.verticalHeader().setVisible(False)
        self.DbPicture.verticalHeader().setDefaultSectionSize(50)
        self.DbPicture.verticalHeader().setMinimumSectionSize(70)
        self.verticalLayout_6.addWidget(self.DbPicture)
        self.deleteA = QtWidgets.QPushButton(self.DbSettings)
        self.deleteA.setMaximumSize(QtCore.QSize(167, 16777116))
        self.deleteA.setObjectName("deleteA")
        self.verticalLayout_6.addWidget(self.deleteA)
        self.tabWidget.addTab(self.DbSettings, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1079, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionChange_Password = QtWidgets.QAction(MainWindow)
        self.actionChange_Password.setObjectName("actionChange_Password")
        self.actionChange_Token_keys = QtWidgets.QAction(MainWindow)
        self.actionChange_Token_keys.setObjectName("actionChange_Token_keys")
        self.actionCheck_for_updates = QtWidgets.QAction(MainWindow)
        self.actionCheck_for_updates.setObjectName("actionCheck_for_updates")
        self.actionAccount_Management = QtWidgets.QAction(MainWindow)
        self.actionAccount_Management.setObjectName("actionAccount_Management")
        self.actionAdmin_Settings = QtWidgets.QAction(MainWindow)
        self.actionAdmin_Settings.setObjectName("actionAdmin_Settings")
        self.menuSettings.addAction(self.actionCheck_for_updates)
        self.menuSettings.addAction(self.actionAccount_Management)
        self.menuSettings.addAction(self.actionAdmin_Settings)
        self.menuBar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        self.ModelsBox.setCurrentIndex(-1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#############################################################
        self.loadLab.setText("")
        self.LoadBar.setEnabled(False)
        self.LoadBar.setValue(0)
        self.statusbar.addPermanentWidget(self.loadLab,2)
        self.statusbar.addPermanentWidget(self.LoadBar,1)
        self.loadLab.setText("")
        MainWindow.setStyleSheet(MAIN_WIN) 
        self.groupBox.setStyleSheet(GRPB)
        self.groupBox_3.setStyleSheet(GRPB)
        self.groupBox_2.setStyleSheet(GRPB)
        self.groupBox_4.setStyleSheet(GRPB)
        self.groupBox_5.setStyleSheet(GRPB)
        self.MyTree.setStyleSheet(TVIEW)
        self.tableView.setStyleSheet(TVIEW)
        self.tabWidget.setStyleSheet(TABW)
        self.Loaded.setStyleSheet(TVIEW)   
        self.negBar.setStyleSheet(RED_BAR)
        self.negBar_2.setStyleSheet(RED_BAR)
        self.posBar.setStyleSheet(BLUE_BAR)
        self.posBar_2.setStyleSheet(BLUE_BAR)
        self.loadLab.setStyleSheet(STATSLAB)
        self.LoadBar.setStyleSheet(LOADB)
        self.label.setStyleSheet(LAB)
        self.label_8.setStyleSheet(LAB)
        self.label_7.setStyleSheet(LAB)
        self.label_6.setStyleSheet(LAB)
        self.label_5.setStyleSheet(LAB)
        self.label_4.setStyleSheet(LAB)
        self.label_3.setStyleSheet(LAB)
        self.label_2.setStyleSheet(LAB)
        self.CP.setChecked(True)
################################################################################    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Twitter Talk"))
        self.CP.setText(_translate("MainWindow", "Lexical Approche (PatternAnalyzer) "))
        self.NB.setText(_translate("MainWindow", "Automatic approche (Naive Bayes)"))
        self.label.setText(_translate("MainWindow", "Positivity:"))
        self.label_2.setText(_translate("MainWindow", "Negativity:"))
        self.choiceBox.setText(_translate("MainWindow", "Actuall Tendency"))
        self.SearchBtn.setText(_translate("MainWindow", "Search"))
        self.showtweetsbtn.setText(_translate("MainWindow", "show tweets"))
        self.refrechBtn.setText(_translate("MainWindow", "Refresh"))
        self.saveBtn.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("MainWindow", "Search and analyse"))
        self.LoadBtn.setText(_translate("MainWindow", "Load"))
        self.label_3.setText(_translate("MainWindow", "Positivity:"))
        self.label_4.setText(_translate("MainWindow", "Negativity:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), _translate("MainWindow", "Saved results"))
        self.label_5.setText(_translate("MainWindow", "First Analyse :"))
        self.label_6.setText(_translate("MainWindow", "second Analyse:"))
        self.graphChoice.setItemText(0, _translate("MainWindow", "Both"))
        self.graphChoice.setItemText(1, _translate("MainWindow", "Positivity"))
        self.graphChoice.setItemText(2, _translate("MainWindow", "Negativity"))
        self.showhisbtn.setText(_translate("MainWindow", "Show Progress"))
        self.saveGraph.setText(_translate("MainWindow", "save Graphe"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab3), _translate("MainWindow", "comparatif study"))
        self.label_7.setText(_translate("MainWindow", "Start point:"))
        self.plotChoice.setItemText(0, _translate("MainWindow", "Both"))
        self.plotChoice.setItemText(1, _translate("MainWindow", "Positive"))
        self.plotChoice.setItemText(2, _translate("MainWindow", "Negative"))
        self.label_8.setText(_translate("MainWindow", "end point:"))
        self.saveplot.setText(_translate("MainWindow", "Save graphe "))
        self.showp.setText(_translate("MainWindow", "Show Progression"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotevo), _translate("MainWindow", "Time Evolution"))
        self.deleteA.setText(_translate("MainWindow", "delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DbSettings), _translate("MainWindow", "Neo4j Settings"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionChange_Password.setText(_translate("MainWindow", "Change Password"))
        self.actionChange_Token_keys.setText(_translate("MainWindow", "Change Token keys"))
        self.actionCheck_for_updates.setText(_translate("MainWindow", "Check for updates"))
        self.actionAccount_Management.setText(_translate("MainWindow", "General"))
        self.actionAdmin_Settings.setText(_translate("MainWindow", "Admin Settings"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

