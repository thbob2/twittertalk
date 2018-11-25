# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auth3.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
MAIN="""QDialog{
    border: 2px solid grey;
    background-color: #24292E;
    border-radius:5px
    }
    QLabel{
    color:#15c0ef;
    }
    QMessageBox QLabel{
    color:#ffffff;
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
MAIN_WIN = """QMainWindow{
    border: 2px solid grey;
    border-radius: 4px;
    background-color: #24292E;
    
    QMessageBox QLabel{
    color:#ffffff;
    }
}"""
GRPB=""" QGroupBox{
     border:2px solid grey;
     border-radius:5px;
     color: #15c0ef;
     text-align: left;
     background-color: #24292E;
}
"""
STATSLAB=""" QLabel{
    color: #ffffff;
    
}
"""
ERROREDIT="""QLineEdit{
        border: 2px solid #f40404;
        background-color: #24292E;
        color: #f40404;}
"""
VALIDLINE="""
QLineEdit{
    border: 2px solid green;
    background-color: #24292E;
    color: green;}

"""
SWITCHBTN="""QPushButton{
        
        color:#ffffff;
        text-align:left;
}
"""
LEDIT="""QLineEdit{
    border: 2px solid #0565d9;
    background-color: #24292E;
    color: #ffffff;
}
"""
TEDIT="""QTextEdit{
    border: 2px solid #0565d9;
    background-color: #24292E;
    color: #ffffff;
}
"""
PBAR ="""QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
"""
class Ui_AuthWindow(object):
    def setupUi(self, AuthWindow):
        AuthWindow.setObjectName("AuthWindow")
        AuthWindow.setWindowModality(QtCore.Qt.NonModal)
        AuthWindow.resize(419, 182)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AuthWindow.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(AuthWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.login = QtWidgets.QPushButton(AuthWindow)
        self.login.setMinimumSize(QtCore.QSize(0, 31))
        self.login.setObjectName("login")
        self.gridLayout.addWidget(self.login, 5, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(AuthWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.switch = QtWidgets.QPushButton(AuthWindow)
        self.switch.setStyleSheet("text-align:left")
        self.switch.setFlat(True)
        self.switch.setObjectName("switch")
        self.gridLayout.addWidget(self.switch, 5, 1, 1, 1)
        self.pwd = ClickableLineEdit(AuthWindow)
        self.pwd.setMaxLength(32)
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setObjectName("pwd")
        self.gridLayout.addWidget(self.pwd, 4, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(AuthWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(AuthWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 2, 2)
        self.id = ClickableLineEdit(AuthWindow)
        self.id.setMaxLength(32)
        self.id.setObjectName("id")
        self.gridLayout.addWidget(self.id, 2, 1, 1, 2)
        self.label = QtWidgets.QLabel(AuthWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.signin = QtWidgets.QPushButton(AuthWindow)
        self.signin.setMinimumSize(QtCore.QSize(0, 46))
        self.signin.setObjectName("signin")
        self.gridLayout.addWidget(self.signin, 6, 2, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        
        self.retranslateUi(AuthWindow)
        QtCore.QMetaObject.connectSlotsByName(AuthWindow)
        AuthWindow.setStyleSheet(MAIN)
        self.label.setStyleSheet(STATSLAB)
        self.label_2.setStyleSheet(STATSLAB)
        self.label_3.setStyleSheet(STATSLAB)
        self.label_4.setStyleSheet(STATSLAB)
        self.switch.setStyleSheet(SWITCHBTN)
        self.id.setStyleSheet(LEDIT)
        self.pwd.setStyleSheet(LEDIT)
    def retranslateUi(self, AuthWindow):
        _translate = QtCore.QCoreApplication.translate
        AuthWindow.setWindowTitle(_translate("AuthWindow", "Twitter Talk Auth"))
        self.login.setText(_translate("AuthWindow", "Login"))
        self.label_2.setText(_translate("AuthWindow", "      password:"))
        self.switch.setText(_translate("AuthWindow", "show password"))
        self.label_4.setText(_translate("AuthWindow", "welcome to Twitter Talk "))
        self.label_3.setText(_translate("AuthWindow", "don\'t have an account ? join us .."))
        self.label.setText(_translate("AuthWindow", "      username :"))
        self.signin.setText(_translate("AuthWindow", "Sign In"))
#################################################################################
class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLineEdit.mousePressEvent(self, event)


##################################################################################################"
class SignWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 418)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(9, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setMinimumSize(QtCore.QSize(0, 21))
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.acctoken = ClickableLineEdit(Dialog)
        self.acctoken.setMinimumSize(QtCore.QSize(0, 28))
        self.acctoken.setObjectName("acctoken")
        self.gridLayout_2.addWidget(self.acctoken, 6, 1, 1, 1)
        self.username = ClickableLineEdit(Dialog)
        self.username.setMinimumSize(QtCore.QSize(40, 28))
        self.username.setMaxLength(32)
        self.username.setObjectName("username")
        self.gridLayout_2.addWidget(self.username, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setMinimumSize(QtCore.QSize(0, 21))
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 7, 0, 1, 1)
        self.accsecret = ClickableLineEdit(Dialog)
        self.accsecret.setMinimumSize(QtCore.QSize(0, 28))
        self.accsecret.setObjectName("accsecret")
        self.gridLayout_2.addWidget(self.accsecret, 7, 1, 1, 1)
        self.switch = QtWidgets.QPushButton(Dialog)
        self.switch.setStyleSheet("text-align:left")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../index.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.switch.setIcon(icon1)
        self.switch.setCheckable(False)
        self.switch.setChecked(False)
        self.switch.setFlat(True)
        self.switch.setObjectName("switch")
        self.gridLayout_2.addWidget(self.switch, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
        self.csecret = ClickableLineEdit(Dialog)
        self.csecret.setMinimumSize(QtCore.QSize(0, 28))
        self.csecret.setObjectName("csecret")
        self.gridLayout_2.addWidget(self.csecret, 5, 1, 1, 1)
        self.cancel = QtWidgets.QPushButton(Dialog)
        self.cancel.setMinimumSize(QtCore.QSize(96, 0))
        self.cancel.setMaximumSize(QtCore.QSize(160, 16777215))
        self.cancel.setObjectName("cancel")
        self.gridLayout_2.addWidget(self.cancel, 10, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 18))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.pwd = ClickableLineEdit(Dialog)
        self.pwd.setMinimumSize(QtCore.QSize(0, 28))
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setObjectName("pwd")
        self.gridLayout_2.addWidget(self.pwd, 1, 1, 1, 1)
        self.ckey = ClickableLineEdit(Dialog)
        self.ckey.setMinimumSize(QtCore.QSize(0, 28))
        self.ckey.setObjectName("ckey")
        self.gridLayout_2.addWidget(self.ckey, 4, 1, 1, 1)
        self.pwdconfirm = ClickableLineEdit(Dialog)
        self.pwdconfirm.setMinimumSize(QtCore.QSize(0, 28))
        self.pwdconfirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwdconfirm.setObjectName("pwdconfirm")
        self.gridLayout_2.addWidget(self.pwdconfirm, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(0, 17))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)
        self.submit = QtWidgets.QPushButton(Dialog)
        self.submit.setMinimumSize(QtCore.QSize(0, 0))
        self.submit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.submit.setFlat(False)
        self.submit.setObjectName("submit")
        self.gridLayout_2.addWidget(self.submit, 10, 1, 1, 1)
        self.twitterLink = QtWidgets.QLabel(Dialog)
        self.twitterLink.setMinimumSize(QtCore.QSize(89, 20))
        self.twitterLink.setStyleSheet("text-align:centre")
        self.twitterLink.setObjectName("twitterLink")
        self.gridLayout_2.addWidget(self.twitterLink, 9, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        urlLink="<a href=\"https://developer.twitter.com/en/apply/user\"> <font face=verdana size=4 color=#ffffff> don't have your tokens? get them now </a>"

        self.twitterLink.setText(urlLink)
        self.twitterLink.setOpenExternalLinks(True)
        Dialog.setStyleSheet(MAIN)
        self.label.setStyleSheet(STATSLAB)
        self.label_2.setStyleSheet(STATSLAB)
        self.label_3.setStyleSheet(STATSLAB)
        self.label_4.setStyleSheet(STATSLAB)
        self.label_5.setStyleSheet(STATSLAB)
        self.label_6.setStyleSheet(STATSLAB)
        self.label_7.setStyleSheet(STATSLAB)
        self.switch.setStyleSheet(SWITCHBTN)
        self.username.setStyleSheet(LEDIT)
        self.pwd.setStyleSheet(LEDIT)
        self.pwdconfirm.setStyleSheet(LEDIT)
        self.ckey.setStyleSheet(LEDIT)
        self.csecret.setStyleSheet(LEDIT)
        self.acctoken.setStyleSheet(LEDIT)
        self.accsecret.setStyleSheet(LEDIT)
        self.twitterLink.setStyleSheet("text-align:centre")
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Signing in "))
        self.label_3.setText(_translate("Dialog", "confirm password :"))
        self.label_7.setText(_translate("Dialog", "consumer key :"))
        self.label_6.setText(_translate("Dialog", "access secret :"))
        self.label_4.setText(_translate("Dialog", "consumer secret :"))
        self.switch.setText(_translate("Dialog", "show password"))
        self.label_5.setText(_translate("Dialog", "access token :"))
        self.label_2.setText(_translate("Dialog", "password:"))
        self.cancel.setText(_translate("Dialog", "cancel"))
        self.label.setText(_translate("Dialog", "user name:"))
        self.submit.setText(_translate("Dialog", "confirm"))
        self.twitterLink.setText(_translate("Dialog", "get your tokens "))
#########################################################################################
class Ui_UpdateWindow(object):
    def setupUi(self, UpdateWindow):
        self.movie = QMovie("icon/loading.gif")
        size = self.movie.scaledSize()
        UpdateWindow.setObjectName("UpdateWindow")
        UpdateWindow.setGeometry(200,200,size.width(),size.height())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UpdateWindow.sizePolicy().hasHeightForWidth())
        UpdateWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateWindow.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(UpdateWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.MainExtraLab = QtWidgets.QLabel(UpdateWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainExtraLab.sizePolicy().hasHeightForWidth())
        self.MainExtraLab.setSizePolicy(sizePolicy)
        self.MainExtraLab.setMaximumSize(QtCore.QSize(430, 28))
        self.MainExtraLab.setText("")
        self.MainExtraLab.setObjectName("MainExtraLab")
        self.gridLayout.addWidget(self.MainExtraLab, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(UpdateWindow)
        self.label.setText("")
        
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(UpdateWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdateWindow)
        #################""
        UpdateWindow.setStyleSheet(MAIN)
        self.label.setMovie(self.movie)
        self.movie.start()
    def retranslateUi(self, UpdateWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindow.setWindowTitle(_translate("UpdateWindow", "Twitter Talk "))


##########################
class Ui_ShowTweets(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(650, 550)
        form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setObjectName("gridLayout")
        self.MyTweets = QtWidgets.QTableView(form)
        self.MyTweets.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.MyTweets.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.MyTweets.setAlternatingRowColors(True)
        self.MyTweets.setObjectName("MyTweets")
        self.MyTweets.horizontalHeader().setDefaultSectionSize(150)
        self.MyTweets.horizontalHeader().setMinimumSectionSize(90)
        self.MyTweets.horizontalHeader().setStretchLastSection(True)
        self.MyTweets.verticalHeader().setVisible(True)
        self.MyTweets.verticalHeader().setDefaultSectionSize(40)
        self.MyTweets.verticalHeader().setMinimumSectionSize(120)
        self.MyTweets.verticalHeader().setSortIndicatorShown(True)
        self.MyTweets.verticalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.MyTweets, 0, 0, 1, 1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Tweets"))
################################################
class Ui_Acm(object):
    def setupUi(self, acm):
        acm.setObjectName("acm")
        acm.resize(424, 506)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        acm.setWindowIcon(icon)
        self.formLayout_2 = QtWidgets.QFormLayout(acm)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(acm)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.setStyleSheet(TABW)
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(200, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.Npwd = ClickableLineEdit(self.groupBox)
        self.Npwd.setMinimumSize(QtCore.QSize(200, 30))
        self.Npwd.setMaximumSize(QtCore.QSize(200, 30))
        self.Npwd.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.Npwd.setObjectName("Npwd")
        self.gridLayout_2.addWidget(self.Npwd, 1, 0, 1, 1)
        self.submit = QtWidgets.QPushButton(self.groupBox)
        self.submit.setMinimumSize(QtCore.QSize(150, 30))
        self.submit.setMaximumSize(QtCore.QSize(150, 30))
        self.submit.setObjectName("submit")
        self.gridLayout_2.addWidget(self.submit, 2, 1, 1, 1)
        self.Npwdc = ClickableLineEdit(self.groupBox)
        self.Npwdc.setMinimumSize(QtCore.QSize(200, 30))
        self.Npwdc.setMaximumSize(QtCore.QSize(200, 30))
        self.Npwdc.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.Npwdc.setObjectName("Npwdc")
        self.gridLayout_2.addWidget(self.Npwdc, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(200, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.cs = ClickableLineEdit(self.groupBox_2)
        self.cs.setMinimumSize(QtCore.QSize(250, 30))
        self.cs.setObjectName("cs")
        self.gridLayout.addWidget(self.cs, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.act = ClickableLineEdit(self.groupBox_2)
        self.act.setMinimumSize(QtCore.QSize(250, 30))
        self.act.setObjectName("act")
        self.gridLayout.addWidget(self.act, 5, 0, 1, 1)
        self.ck = ClickableLineEdit(self.groupBox_2)
        self.ck.setMinimumSize(QtCore.QSize(250, 30))
        self.ck.setMaximumSize(QtCore.QSize(400, 30))
        self.ck.setObjectName("ck")
        self.gridLayout.addWidget(self.ck, 1, 0, 1, 1)
        self.gapi = QtWidgets.QPushButton(self.groupBox_2)
        self.gapi.setMinimumSize(QtCore.QSize(100, 30))
        self.gapi.setObjectName("gapi")
        self.gridLayout.addWidget(self.gapi, 3, 1, 1, 1)
        self.acs = ClickableLineEdit(self.groupBox_2)
        self.acs.setMinimumSize(QtCore.QSize(250, 30))
        self.acs.setMaximumSize(QtCore.QSize(300, 30))
        self.acs.setObjectName("acs")
        self.gridLayout.addWidget(self.acs, 9, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.groupBox_2)
        self.Cancel = QtWidgets.QPushButton(self.tab)
        self.Cancel.setMinimumSize(QtCore.QSize(150, 30))
        self.Cancel.setMaximumSize(QtCore.QSize(100, 40))
        self.Cancel.setObjectName("Cancel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Cancel)
        self.Ok = QtWidgets.QPushButton(self.tab)
        self.Ok.setMinimumSize(QtCore.QSize(150, 30))
        self.Ok.setMaximumSize(QtCore.QSize(150, 16777215))
        self.Ok.setObjectName("Ok")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Ok)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setMinimumSize(QtCore.QSize(100, 20))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 16777071))
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)
        self.confrimbtn = QtWidgets.QPushButton(self.tab_2)
        self.confrimbtn.setMinimumSize(QtCore.QSize(24, 15))
        self.confrimbtn.setMaximumSize(QtCore.QSize(167, 30))
        self.confrimbtn.setObjectName("confrimbtn")
        self.gridLayout_3.addWidget(self.confrimbtn, 4, 1, 1, 1)
        self.pwd = ClickableLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pwd.sizePolicy().hasHeightForWidth())
        self.pwd.setSizePolicy(sizePolicy)
        self.pwd.setMinimumSize(QtCore.QSize(200, 30))
        self.pwd.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pwd.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.pwd.setObjectName("pwd")
        self.gridLayout_3.addWidget(self.pwd, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.userinfo = QtWidgets.QTextEdit(self.tab_2)
        self.userinfo.setMinimumSize(QtCore.QSize(0, 300))
        self.userinfo.setMaximumSize(QtCore.QSize(300, 300))
        self.userinfo.setObjectName("userinfo")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.userinfo.setFont(font)
        self.userinfo.setReadOnly(True)
        self.gridLayout_3.addWidget(self.userinfo, 2, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabWidget)

        self.retranslateUi(acm)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(acm)


        self.userinfo.setStyleSheet(TEDIT)
        acm.setStyleSheet(MAIN)
        self.Npwd.setStyleSheet(LEDIT)
        self.Npwdc.setStyleSheet(LEDIT)
        self.ck.setStyleSheet(LEDIT)
        self.cs.setStyleSheet(LEDIT)
        self.act.setStyleSheet(LEDIT)
        self.acs.setStyleSheet(LEDIT)
        self.groupBox.setStyleSheet(GRPB)
        self.groupBox_2.setStyleSheet(GRPB)
        self.pwd.setStyleSheet(LEDIT)
    def retranslateUi(self, acm):
        _translate = QtCore.QCoreApplication.translate
        acm.setWindowTitle(_translate("acm", "General Account Settings"))
        self.groupBox.setTitle(_translate("acm", "New Password"))
        self.label.setText(_translate("acm", "Password:"))
        self.submit.setText(_translate("acm", "submit"))
        self.label_2.setText(_translate("acm", "Confirm password:"))
        self.groupBox_2.setTitle(_translate("acm", "Update Tokens"))
        self.label_5.setText(_translate("acm", "Access Token:"))
        self.label_4.setText(_translate("acm", "Consumer key:"))
        self.label_6.setText(_translate("acm", "Secret Token:"))
        self.gapi.setText(_translate("acm", "Generate api "))
        self.label_3.setText(_translate("acm", "Consumer Secret:"))
        self.Cancel.setText(_translate("acm", "Cancel"))
        self.Ok.setText(_translate("acm", "Ok"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("acm", "Account settings"))
        self.label_7.setText(_translate("acm", "Password:"))
        self.confrimbtn.setText(_translate("acm", "confirm"))
        self.label_8.setText(_translate("acm", "User Info:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("acm", "Delete Account"))
#######
class Ui_Admins(object):
    def setupUi(self, Ads):
        Ads.setObjectName("Ads")
        Ads.resize(498, 505)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ads.setWindowIcon(icon)
        self.formLayout_2 = QtWidgets.QFormLayout(Ads)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Ads)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab1 = QtWidgets.QWidget()
        self.Tab1.setObjectName("Tab1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Tab1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.usersT = QtWidgets.QTableView(self.Tab1)
        self.usersT.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.usersT.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.usersT.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.usersT.setObjectName("usersT")
        self.usersT.horizontalHeader().setMinimumSectionSize(100)
        self.usersT.horizontalHeader().setStretchLastSection(True)
        self.usersT.verticalHeader().setVisible(False)
        self.usersT.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.usersT)
        self.deleteU = QtWidgets.QPushButton(self.Tab1)
        self.deleteU.setMinimumSize(QtCore.QSize(50, 30))
        self.deleteU.setMaximumSize(QtCore.QSize(100, 16777215))
        self.deleteU.setObjectName("deleteU")
        self.verticalLayout.addWidget(self.deleteU)
        self.tabWidget.addTab(self.Tab1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setMinimumSectionSize(100)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setDefaultSectionSize(45)
        self.tableView.verticalHeader().setMinimumSectionSize(40)
        self.verticalLayout_2.addWidget(self.tableView)
        self.removeC = QtWidgets.QPushButton(self.tab_2)
        self.removeC.setMinimumSize(QtCore.QSize(0, 25))
        self.removeC.setMaximumSize(QtCore.QSize(200, 30))
        self.removeC.setObjectName("removeC")
        self.verticalLayout_2.addWidget(self.removeC)
        self.tabWidget.addTab(self.tab_2, "")
        self.Tab_3 = QtWidgets.QWidget()
        self.Tab_3.setObjectName("Tab_3")
        self.formLayout = QtWidgets.QFormLayout(self.Tab_3)
        self.formLayout.setObjectName("formLayout")
        self.newModel = QtWidgets.QLineEdit(self.Tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newModel.sizePolicy().hasHeightForWidth())
        self.newModel.setSizePolicy(sizePolicy)
        self.newModel.setMinimumSize(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.newModel.setFont(font)
        self.newModel.setObjectName("newModel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.newModel)
        self.Add = QtWidgets.QPushButton(self.Tab_3)
        self.Add.setMaximumSize(QtCore.QSize(100, 30))
        self.Add.setObjectName("Add")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Add)
        self.modtable = QtWidgets.QTableView(self.Tab_3)
        self.modtable.setMinimumSize(QtCore.QSize(450, 370))
        self.modtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.modtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.modtable.setObjectName("modtable")
        self.modtable.horizontalHeader().setDefaultSectionSize(130)
        self.modtable.horizontalHeader().setMinimumSectionSize(70)
        self.modtable.horizontalHeader().setStretchLastSection(True)
        self.modtable.verticalHeader().setVisible(True)
        self.modtable.verticalHeader().setDefaultSectionSize(60)
        self.modtable.verticalHeader().setMinimumSectionSize(40)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.modtable)
        self.removeModel = QtWidgets.QPushButton(self.Tab_3)
        self.removeModel.setMinimumSize(QtCore.QSize(100, 30))
        self.removeModel.setMaximumSize(QtCore.QSize(150, 30))
        self.removeModel.setObjectName("removeModel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.removeModel)
        self.apply = QtWidgets.QPushButton(self.Tab_3)
        self.apply.setMinimumSize(QtCore.QSize(0, 30))
        self.apply.setMaximumSize(QtCore.QSize(200, 16777215))
        self.apply.setObjectName("apply")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.apply)
        self.tabWidget.addTab(self.Tab_3, "")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabWidget)

        self.retranslateUi(Ads)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ads)
        QtCore.QMetaObject.connectSlotsByName(Ads)
        Ads.setStyleSheet(MAIN)
        self.tabWidget.setStyleSheet(TABW)
        self.newModel.setStyleSheet(LEDIT)

    def retranslateUi(self, Ads):
        _translate = QtCore.QCoreApplication.translate
        Ads.setWindowTitle(_translate("Ads", "Adminstrative Settings"))
        self.deleteU.setText(_translate("Ads", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("Ads", "Manage Users"))
        self.removeC.setText(_translate("Ads", "remove"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Ads", "Manage Corpus"))
        self.Add.setText(_translate("Ads", "Add"))
        self.removeModel.setText(_translate("Ads", "Remove Model"))
        self.apply.setText(_translate("Ads", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_3), _translate("Ads", "Manage Model"))


####################################################
if __name__ == "__main__":
 
    app = QtWidgets.QApplication(sys.argv)
    auth = QtWidgets.QDialog()
    ui = SignWindow()
    ui.setupUi(auth)
    auth.show()
    sys.exit(app.exec_())


