# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_work.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QLocale,
    QMetaObject, QRect,QTimer)

from PySide6.QtGui import (QColor,QCursor, QFont,QIcon, QPalette,QIcon)

from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
    QLabel, QMainWindow, QMenu,QMenuBar, QProgressBar, QPushButton, QStatusBar, 
    QTabWidget, QTableWidget, QTableWidgetItem,QTextEdit, QWidget, QButtonGroup, 
    QVBoxLayout, QToolTip, QFileDialog,QVBoxLayout)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import pandas as pd
from enums import SystemMode
import logic
import numpy as np
import sys
import matplotlib.cm as cm

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"SolarOptimus")
        MainWindow.resize(791, 598)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 791, 551))
        self.tabWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget_2 = QTabWidget(self.tab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setGeometry(QRect(180, 30, 581, 351))
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.tableWidget = QTableWidget(self.tab_6)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(60, 50, 501, 211))
        self.pushButton_2 = QPushButton(self.tab_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(60, 270, 101, 41))
        self.pushButton_3 = QPushButton(self.tab_6)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(170, 270, 101, 41))
        self.label = QLabel(self.tab_6)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 10, 711, 21))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.tableWidget_3 = QTableWidget(self.tab_7)
        if (self.tableWidget_3.columnCount() < 5):
            self.tableWidget_3.setColumnCount(5)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(4, __qtablewidgetitem9)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        self.tableWidget_3.setGeometry(QRect(60, 50, 501, 211))
        self.pushButton_7 = QPushButton(self.tab_7)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(60, 270, 101, 41))
        self.pushButton_6 = QPushButton(self.tab_7)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(170, 270, 101, 41))
        self.label_2 = QLabel(self.tab_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 10, 711, 21))
        self.label_2.setFont(font)
        self.tabWidget_2.addTab(self.tab_7, "")
        self.Mansoon = QWidget()
        self.Mansoon.setObjectName(u"Mansoon")
        self.tableWidget_4 = QTableWidget(self.Mansoon)
        if (self.tableWidget_4.columnCount() < 5):
            self.tableWidget_4.setColumnCount(5)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        self.tableWidget_4.setObjectName(u"tableWidget_4")
        self.tableWidget_4.setGeometry(QRect(60, 50, 501, 211))
        self.pushButton_8 = QPushButton(self.Mansoon)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(170, 270, 101, 41))
        self.pushButton_9 = QPushButton(self.Mansoon)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(60, 270, 101, 41))
        self.label_3 = QLabel(self.Mansoon)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 10, 711, 21))
        self.label_3.setFont(font)
        self.tabWidget_2.addTab(self.Mansoon, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.tableWidget_5 = QTableWidget(self.tab_10)
        if (self.tableWidget_5.columnCount() < 5):
            self.tableWidget_5.setColumnCount(5)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(4, __qtablewidgetitem19)
        self.tableWidget_5.setObjectName(u"tableWidget_5")
        self.tableWidget_5.setGeometry(QRect(60, 50, 501, 211))
        self.pushButton_11 = QPushButton(self.tab_10)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(60, 270, 101, 41))
        self.pushButton_10 = QPushButton(self.tab_10)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(170, 270, 101, 41))
        self.label_4 = QLabel(self.tab_10)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 10, 711, 21))
        self.label_4.setFont(font)
        self.tabWidget_2.addTab(self.tab_10, "")
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(180, 390, 181, 24))
        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 80, 161, 271))
        self.label_19 = QLabel(self.groupBox_4)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(30, 50, 101, 16))
        self.textEdit_15 = QTextEdit(self.groupBox_4)
        self.textEdit_15.setObjectName(u"textEdit_15")
        self.textEdit_15.setGeometry(QRect(30, 70, 104, 21))
        self.label_20 = QLabel(self.groupBox_4)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(30, 130, 101, 16))
        self.textEdit_16 = QTextEdit(self.groupBox_4)
        self.textEdit_16.setObjectName(u"textEdit_16")
        self.textEdit_16.setGeometry(QRect(30, 150, 104, 21))
        self.textEdit_17 = QTextEdit(self.groupBox_4)
        self.textEdit_17.setObjectName(u"textEdit_17")
        self.textEdit_17.setGeometry(QRect(30, 230, 104, 21))
        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(30, 210, 101, 16))
        self.textEdit_31 = QTextEdit(self.tab)
        self.textEdit_31.setObjectName(u"textEdit_31")
        self.textEdit_31.setGeometry(QRect(160, 477, 591, 21))
        self.pushButton_18 = QPushButton(self.tab)
        self.pushButton_18.setObjectName(u"pushButton_18")
        self.pushButton_18.setGeometry(QRect(50, 470, 101, 31))
        self.label_53 = QLabel(self.tab)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setGeometry(QRect(50, 440, 561, 16))
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.checkBox = QCheckBox(self.tab_3)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(70, 140, 151, 20))
        self.checkBox_2 = QCheckBox(self.tab_3)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(70, 160, 141, 20))
        self.checkBox_3 = QCheckBox(self.tab_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(70, 180, 191, 20))
        self.checkBox_4 = QCheckBox(self.tab_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setGeometry(QRect(70, 200, 201, 20))
        self.checkBox_5 = QCheckBox(self.tab_3)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setGeometry(QRect(70, 220, 171, 20))
        self.groupBox_5 = QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(30, 40, 291, 231))
        self.line = QFrame(self.groupBox_5)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 70, 251, 16))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(20, 20, 261, 31))
        self.label_23 = QLabel(self.groupBox_5)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(20, 50, 281, 16))
        self.groupBox_6 = QGroupBox(self.groupBox_5)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(20, 230, 291, 231))
        self.line_2 = QFrame(self.groupBox_6)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(20, 70, 251, 16))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_24 = QLabel(self.groupBox_6)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(20, 20, 261, 31))
        self.label_25 = QLabel(self.groupBox_6)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(20, 50, 281, 16))
        self.pushButton_4 = QPushButton(self.tab_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 450, 121, 41))
        font1 = QFont()
        font1.setKerning(True)
        self.pushButton_4.setFont(font1)
        self.pushButton_4.setAutoFillBackground(True)
        self.progressBar = QProgressBar(self.tab_3)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(170, 460, 591, 23))
        self.progressBar.setValue(24)
        self.GrapWidget = QWidget(self.tab_3)
        self.GrapWidget.setObjectName(u"GrapWidget")
        self.GrapWidget.setGeometry(QRect(350, 50, 411, 371))
        self.groupBox_7 = QGroupBox(self.tab_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(30, 300, 291, 91))
        self.label_26 = QLabel(self.groupBox_7)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(10, 30, 191, 16))
        self.label_27 = QLabel(self.groupBox_7)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(10, 60, 191, 16))
        self.WatValue = QLabel(self.groupBox_7)
        self.WatValue.setObjectName(u"WatValue")
        self.WatValue.setGeometry(QRect(190, 30, 49, 16))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.WatValue.setFont(font2)
        self.BatValue = QLabel(self.groupBox_7)
        self.BatValue.setObjectName(u"BatValue")
        self.BatValue.setGeometry(QRect(190, 60, 49, 16))
        self.BatValue.setFont(font2)
        self.tabWidget.addTab(self.tab_3, "")
        self.groupBox_5.raise_()
        self.checkBox.raise_()
        self.checkBox_2.raise_()
        self.checkBox_3.raise_()
        self.checkBox_4.raise_()
        self.checkBox_5.raise_()
        self.pushButton_4.raise_()
        self.progressBar.raise_()
        self.GrapWidget.raise_()
        self.groupBox_7.raise_()
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_2.setEnabled(True)
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(40, 40, 381, 201))
        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 60, 104, 21))
        self.textEdit_2 = QTextEdit(self.groupBox)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(20, 140, 104, 21))
        self.textEdit_3 = QTextEdit(self.groupBox)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setGeometry(QRect(170, 60, 104, 21))
        self.textEdit_4 = QTextEdit(self.groupBox)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setGeometry(QRect(170, 140, 104, 21))
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 40, 111, 16))
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(170, 40, 231, 16))
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 120, 111, 16))
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(170, 120, 111, 16))
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(120, 280, 571, 211))
        self.textEdit_5 = QTextEdit(self.groupBox_2)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setGeometry(QRect(50, 80, 104, 21))
        self.textEdit_6 = QTextEdit(self.groupBox_2)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setGeometry(QRect(50, 120, 104, 21))
        self.textEdit_7 = QTextEdit(self.groupBox_2)
        self.textEdit_7.setObjectName(u"textEdit_7")
        self.textEdit_7.setGeometry(QRect(50, 160, 104, 21))
        self.textEdit_8 = QTextEdit(self.groupBox_2)
        self.textEdit_8.setObjectName(u"textEdit_8")
        self.textEdit_8.setGeometry(QRect(50, 40, 104, 21))
        self.textEdit_9 = QTextEdit(self.groupBox_2)
        self.textEdit_9.setObjectName(u"textEdit_9")
        self.textEdit_9.setGeometry(QRect(310, 40, 104, 21))
        self.textEdit_10 = QTextEdit(self.groupBox_2)
        self.textEdit_10.setObjectName(u"textEdit_10")
        self.textEdit_10.setGeometry(QRect(310, 80, 104, 21))
        self.textEdit_11 = QTextEdit(self.groupBox_2)
        self.textEdit_11.setObjectName(u"textEdit_11")
        self.textEdit_11.setGeometry(QRect(310, 120, 104, 21))
        self.textEdit_12 = QTextEdit(self.groupBox_2)
        self.textEdit_12.setObjectName(u"textEdit_12")
        self.textEdit_12.setGeometry(QRect(310, 160, 104, 21))
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(170, 40, 141, 16))
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(170, 80, 111, 16))
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(170, 120, 111, 16))
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(170, 160, 111, 16))
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(430, 40, 111, 16))
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(430, 80, 111, 16))
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(430, 120, 131, 16))
        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(430, 160, 131, 16))
        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(460, 40, 311, 201))
        self.textEdit_13 = QTextEdit(self.groupBox_3)
        self.textEdit_13.setObjectName(u"textEdit_13")
        self.textEdit_13.setGeometry(QRect(20, 50, 104, 21))
        self.textEdit_14 = QTextEdit(self.groupBox_3)
        self.textEdit_14.setObjectName(u"textEdit_14")
        self.textEdit_14.setGeometry(QRect(20, 100, 104, 21))
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(140, 100, 161, 16))
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(140, 50, 141, 16))
        self.textEdit_30 = QTextEdit(self.groupBox_3)
        self.textEdit_30.setObjectName(u"textEdit_30")
        self.textEdit_30.setGeometry(QRect(20, 150, 104, 21))
        self.label_29 = QLabel(self.groupBox_3)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(140, 150, 161, 16))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.pushButton_5 = QPushButton(self.tab_4)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(30, 20, 121, 41))
        self.pushButton_5.setFont(font1)
        self.pushButton_5.setAutoFillBackground(True)
        self.progressBar_2 = QProgressBar(self.tab_4)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setGeometry(QRect(180, 30, 591, 23))
        self.progressBar_2.setValue(24)
        self.groupBox_8 = QGroupBox(self.tab_4)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(340, 410, 291, 91))
        font3 = QFont()
        font3.setBold(False)
        self.groupBox_8.setFont(font3)
        self.label_28 = QLabel(self.groupBox_8)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(10, 40, 191, 21))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_28.setFont(font4)
        self.WatValue_2 = QLabel(self.groupBox_8)
        self.WatValue_2.setObjectName(u"WatValue_2")
        self.WatValue_2.setGeometry(QRect(220, 40, 49, 16))
        font5 = QFont()
        font5.setPointSize(14)
        font5.setBold(True)
        self.WatValue_2.setFont(font5)
        self.pushButton_12 = QPushButton(self.tab_4)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(30, 430, 121, 41))
        self.pushButton_12.setFont(font1)
        self.pushButton_12.setAutoFillBackground(True)
        self.tabWidget_3 = QTabWidget(self.tab_4)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tabWidget_3.setGeometry(QRect(30, 70, 731, 321))
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.GrapWidget_2 = QWidget(self.tab_5)
        self.GrapWidget_2.setObjectName(u"GrapWidget_2")
        self.GrapWidget_2.setGeometry(QRect(0, 0, 541, 291))
        self.pushButton_15 = QPushButton(self.tab_5)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(570, 170, 141, 24))
        self.groupBox_13 = QGroupBox(self.tab_5)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setGeometry(QRect(570, 50, 141, 111))
        self.checkBox_9 = QCheckBox(self.groupBox_13)
        self.checkBox_9.setObjectName(u"checkBox_9")
        self.checkBox_9.setGeometry(QRect(10, 80, 111, 20))
        self.checkBox_8 = QCheckBox(self.groupBox_13)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setGeometry(QRect(10, 60, 131, 20))
        self.checkBox_6 = QCheckBox(self.groupBox_13)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setGeometry(QRect(10, 20, 141, 20))
        self.checkBox_7 = QCheckBox(self.groupBox_13)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setGeometry(QRect(10, 40, 131, 20))
        self.pushButton_17 = QPushButton(self.tab_5)
        self.pushButton_17.setObjectName(u"pushButton_17")
        self.pushButton_17.setGeometry(QRect(570, 200, 141, 24))
        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.GrapWidget_3 = QWidget(self.tab_8)
        self.GrapWidget_3.setObjectName(u"GrapWidget_3")
        self.GrapWidget_3.setGeometry(QRect(200, 0, 521, 291))
        self.groupBox_9 = QGroupBox(self.tab_8)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(10, 100, 171, 91))
        self.label_30 = QLabel(self.groupBox_9)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(10, 30, 191, 16))
        self.label_31 = QLabel(self.groupBox_9)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QRect(10, 60, 191, 16))
        self.WatValue_3 = QLabel(self.groupBox_9)
        self.WatValue_3.setObjectName(u"WatValue_3")
        self.WatValue_3.setGeometry(QRect(130, 30, 49, 16))
        self.WatValue_3.setFont(font2)
        self.BatValue_3 = QLabel(self.groupBox_9)
        self.BatValue_3.setObjectName(u"BatValue_3")
        self.BatValue_3.setGeometry(QRect(130, 60, 49, 16))
        self.BatValue_3.setFont(font2)
        self.pushButton_16 = QPushButton(self.tab_8)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setGeometry(QRect(10, 200, 171, 24))
        self.tabWidget_3.addTab(self.tab_8, "")
        self.tabWidget.addTab(self.tab_4, "")
        self.Parameters = QWidget()
        self.Parameters.setObjectName(u"Parameters")
        self.pushButton_13 = QPushButton(self.Parameters)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setGeometry(QRect(320, 480, 75, 24))
        self.pushButton_14 = QPushButton(self.Parameters)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(400, 480, 91, 24))
        self.groupBox_10 = QGroupBox(self.Parameters)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(20, 20, 461, 331))
        self.label_32 = QLabel(self.groupBox_10)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(10, 90, 341, 16))
        self.textEdit_19 = QTextEdit(self.groupBox_10)
        self.textEdit_19.setObjectName(u"textEdit_19")
        self.textEdit_19.setGeometry(QRect(350, 170, 104, 21))
        self.label_33 = QLabel(self.groupBox_10)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(10, 130, 311, 16))
        self.label_34 = QLabel(self.groupBox_10)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(10, 170, 301, 16))
        self.textEdit_20 = QTextEdit(self.groupBox_10)
        self.textEdit_20.setObjectName(u"textEdit_20")
        self.textEdit_20.setGeometry(QRect(350, 130, 104, 21))
        self.label_35 = QLabel(self.groupBox_10)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(10, 210, 441, 16))
        self.textEdit_21 = QTextEdit(self.groupBox_10)
        self.textEdit_21.setObjectName(u"textEdit_21")
        self.textEdit_21.setGeometry(QRect(350, 250, 104, 21))
        self.label_36 = QLabel(self.groupBox_10)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setGeometry(QRect(10, 250, 181, 16))
        self.label_37 = QLabel(self.groupBox_10)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setGeometry(QRect(10, 40, 441, 16))
        self.textEdit_18 = QTextEdit(self.groupBox_10)
        self.textEdit_18.setObjectName(u"textEdit_18")
        self.textEdit_18.setGeometry(QRect(350, 90, 104, 21))
        self.textEdit_23 = QTextEdit(self.groupBox_10)
        self.textEdit_23.setObjectName(u"textEdit_23")
        self.textEdit_23.setGeometry(QRect(350, 210, 104, 21))
        self.label_42 = QLabel(self.groupBox_10)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setGeometry(QRect(10, 290, 181, 16))
        self.textEdit_25 = QTextEdit(self.groupBox_10)
        self.textEdit_25.setObjectName(u"textEdit_25")
        self.textEdit_25.setGeometry(QRect(350, 290, 104, 21))
        self.groupBox_11 = QGroupBox(self.Parameters)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(500, 70, 271, 251))
        self.label_38 = QLabel(self.groupBox_11)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setGeometry(QRect(10, 40, 341, 16))
        self.label_39 = QLabel(self.groupBox_11)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setGeometry(QRect(10, 60, 341, 16))
        self.label_40 = QLabel(self.groupBox_11)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setGeometry(QRect(20, 100, 181, 16))
        self.label_41 = QLabel(self.groupBox_11)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setGeometry(QRect(20, 170, 211, 16))
        self.textEdit_22 = QTextEdit(self.groupBox_11)
        self.textEdit_22.setObjectName(u"textEdit_22")
        self.textEdit_22.setGeometry(QRect(50, 130, 104, 21))
        self.label_43 = QLabel(self.groupBox_11)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setGeometry(QRect(160, 130, 181, 16))
        self.textEdit_24 = QTextEdit(self.groupBox_11)
        self.textEdit_24.setObjectName(u"textEdit_24")
        self.textEdit_24.setGeometry(QRect(50, 200, 104, 21))
        self.label_44 = QLabel(self.groupBox_11)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setGeometry(QRect(160, 200, 181, 16))
        self.groupBox_12 = QGroupBox(self.Parameters)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setGeometry(QRect(20, 359, 751, 101))
        self.label_45 = QLabel(self.groupBox_12)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setGeometry(QRect(10, 30, 341, 16))
        self.label_46 = QLabel(self.groupBox_12)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setGeometry(QRect(10, 70, 341, 16))
        self.label_47 = QLabel(self.groupBox_12)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setGeometry(QRect(430, 30, 341, 16))
        self.label_48 = QLabel(self.groupBox_12)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setGeometry(QRect(430, 70, 341, 16))
        self.textEdit_26 = QTextEdit(self.groupBox_12)
        self.textEdit_26.setObjectName(u"textEdit_26")
        self.textEdit_26.setGeometry(QRect(190, 30, 104, 21))
        self.textEdit_27 = QTextEdit(self.groupBox_12)
        self.textEdit_27.setObjectName(u"textEdit_27")
        self.textEdit_27.setGeometry(QRect(190, 70, 104, 21))
        self.textEdit_28 = QTextEdit(self.groupBox_12)
        self.textEdit_28.setObjectName(u"textEdit_28")
        self.textEdit_28.setGeometry(QRect(570, 70, 104, 21))
        self.textEdit_29 = QTextEdit(self.groupBox_12)
        self.textEdit_29.setObjectName(u"textEdit_29")
        self.textEdit_29.setGeometry(QRect(570, 30, 104, 21))
        self.label_49 = QLabel(self.groupBox_12)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setGeometry(QRect(300, 30, 181, 16))
        self.label_50 = QLabel(self.groupBox_12)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setGeometry(QRect(300, 70, 181, 16))
        self.label_51 = QLabel(self.groupBox_12)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setGeometry(QRect(680, 70, 181, 16))
        self.label_52 = QLabel(self.groupBox_12)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setGeometry(QRect(680, 30, 181, 16))
        self.tabWidget.addTab(self.Parameters, "")
        self.groupBox_10.raise_()
        self.pushButton_13.raise_()
        self.pushButton_14.raise_()
        self.groupBox_11.raise_()
        self.groupBox_12.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 791, 33))
        self.menuSolarOptimus_Tool = QMenu(self.menubar)
        self.menuSolarOptimus_Tool.setObjectName(u"menuSolarOptimus_Tool")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSolarOptimus_Tool.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("Solar Optimus", u"Solar Optimus", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Solar Optimus", u"Load Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Solar Optimus", u"Power [W]", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Solar Optimus", u"Time of Usage [h]", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Solar Optimus", u"From [xx:xx XM]", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Solar Optimus", u"To [xx:xx XM]", None));
        self.pushButton_2.setText(QCoreApplication.translate("Solar Optimus", u"Add Load", None))
        self.pushButton_3.setText(QCoreApplication.translate("Solar Optimus", u"Remove Load", None))
        self.label.setText(QCoreApplication.translate("Solar Optimus", u"Enter a sample day load profile depending on the seaon", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("Solar Optimus", u"Winter", None))
        ___qtablewidgetitem5 = self.tableWidget_3.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Solar Optimus", u"Load Name", None));
        ___qtablewidgetitem6 = self.tableWidget_3.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Solar Optimus", u"Power [W]", None));
        ___qtablewidgetitem7 = self.tableWidget_3.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Solar Optimus", u"Time of Usage [h]", None));
        ___qtablewidgetitem8 = self.tableWidget_3.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Solar Optimus", u"From [xx:xx XM]", None));
        ___qtablewidgetitem9 = self.tableWidget_3.horizontalHeaderItem(4)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Solar Optimus", u"To [xx:xx XM]", None));
        self.pushButton_7.setText(QCoreApplication.translate("Solar Optimus", u"Add Load", None))
        self.pushButton_6.setText(QCoreApplication.translate("Solar Optimus", u"Remove Load", None))
        self.label_2.setText(QCoreApplication.translate("Solar Optimus", u"Enter a sample day load profile depending on the seaon", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QCoreApplication.translate("Solar Optimus", u"Spring", None))
        ___qtablewidgetitem10 = self.tableWidget_4.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Solar Optimus", u"Load Name", None));
        ___qtablewidgetitem11 = self.tableWidget_4.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Solar Optimus", u"Power [W]", None));
        ___qtablewidgetitem12 = self.tableWidget_4.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Solar Optimus", u"Time of Usage [h]", None));
        ___qtablewidgetitem13 = self.tableWidget_4.horizontalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Solar Optimus", u"From [xx:xx XM]", None));
        ___qtablewidgetitem14 = self.tableWidget_4.horizontalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Solar Optimus", u"To [xx:xx XM]", None));
        self.pushButton_8.setText(QCoreApplication.translate("Solar Optimus", u"Remove Load", None))
        self.pushButton_9.setText(QCoreApplication.translate("Solar Optimus", u"Add Load", None))
        self.label_3.setText(QCoreApplication.translate("Solar Optimus", u"Enter a sample day load profile depending on the seaon", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.Mansoon), QCoreApplication.translate("Solar Optimus", u"Mansoon", None))
        ___qtablewidgetitem15 = self.tableWidget_5.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Solar Optimus", u"Load Name", None));
        ___qtablewidgetitem16 = self.tableWidget_5.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Solar Optimus", u"Power [W]", None));
        ___qtablewidgetitem17 = self.tableWidget_5.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Solar Optimus", u"Time of Usage [h]", None));
        ___qtablewidgetitem18 = self.tableWidget_5.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Solar Optimus", u"From [xx:xx XM]", None));
        ___qtablewidgetitem19 = self.tableWidget_5.horizontalHeaderItem(4)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Solar Optimus", u"To [xx:xx XM]", None));
        self.pushButton_11.setText(QCoreApplication.translate("Solar Optimus", u"Add Load", None))
        self.pushButton_10.setText(QCoreApplication.translate("Solar Optimus", u"Remove Load", None))
        self.label_4.setText(QCoreApplication.translate("Solar Optimus", u"Enter a sample day load profile depending on the seaon", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_10), QCoreApplication.translate("Solar Optimus", u"Summer", None))
        self.pushButton.setText(QCoreApplication.translate("Solar Optimus", u"Copy Sample to other seasons", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Solar Optimus", u"System Info", None))
        self.label_19.setText(QCoreApplication.translate("Solar Optimus", u"System Longitude", None))
        self.label_20.setText(QCoreApplication.translate("Solar Optimus", u"System Latitude", None))
        self.label_21.setText(QCoreApplication.translate("Solar Optimus", u"Designed Years", None))
        self.pushButton_18.setText(QCoreApplication.translate("Solar Optimus", u"Browse Files", None))
        self.label_53.setText(QCoreApplication.translate("Solar Optimus", u"OPTIONAL: Add your solar data file in .csv form. Verify csv compatibility in user manual !", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Solar Optimus", u"1 - Load Profile", None))
        self.checkBox.setText(QCoreApplication.translate("Solar Optimus", u"Critical (0%-1% ENSP)", None))
        self.checkBox_2.setText(QCoreApplication.translate("Solar Optimus", u"High (1%-4% ENSP)", None))
        self.checkBox_3.setText(QCoreApplication.translate("Solar Optimus", u"Medium (4%-6% ENSP)", None))
        self.checkBox_4.setText(QCoreApplication.translate("Solar Optimus", u"Basic (6%-10% ENSP)", None))
        self.checkBox_5.setText(QCoreApplication.translate("Solar Optimus", u"Minimal (>10% ENSP)", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Solar Optimus", u"Robustness selector", None))
        self.label_22.setText(QCoreApplication.translate("Solar Optimus", u"How important is energy availability?", None))
        self.label_23.setText(QCoreApplication.translate("Solar Optimus", u"Choose one option at the end of the sim.", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Solar Optimus", u"Focus of the Optimization", None))
        self.label_24.setText(QCoreApplication.translate("Solar Optimus", u"Choose a single focus for the optimization. ", None))
        self.label_25.setText(QCoreApplication.translate("Solar Optimus", u"It will affect significantly the ouput of the tool", None))
        self.pushButton_4.setText(QCoreApplication.translate("Solar Optimus", u"Launch Tool", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Solar Optimus", u"Optimized Value", None))
        self.label_26.setText(QCoreApplication.translate("Solar Optimus", u"Peak Solar Panel Wattage [W]:", None))
        self.label_27.setText(QCoreApplication.translate("Solar Optimus", u"Battery Capacity [Wh]:", None))
        self.WatValue.setText(QCoreApplication.translate("Solar Optimus", u"45", None))
        self.BatValue.setText(QCoreApplication.translate("Solar Optimus", u"45", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Solar Optimus", u"2 - First Optimization", None))
        self.groupBox.setTitle(QCoreApplication.translate("Solar Optimus", u"Solar Panel", None))
        self.label_5.setText(QCoreApplication.translate("Solar Optimus", u"Peak Power [W]", None))
        self.label_6.setText(QCoreApplication.translate("Solar Optimus", u"Temperature Coefficient [%/\u00b0C]", None))
        self.label_7.setText(QCoreApplication.translate("Solar Optimus", u"Area  [m\u00b2]", None))
        self.label_8.setText(QCoreApplication.translate("Solar Optimus", u"Number of Panels", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Solar Optimus", u"Battery Array", None))
        self.label_11.setText(QCoreApplication.translate("Solar Optimus", u"Nominal Capacity [Ah]", None))
        self.label_12.setText(QCoreApplication.translate("Solar Optimus", u"Minimum SOC [%]", None))
        self.label_13.setText(QCoreApplication.translate("Solar Optimus", u"Battery Mass [kg]", None))
        self.label_14.setText(QCoreApplication.translate("Solar Optimus", u"Battery Height [cm]", None))
        self.label_15.setText(QCoreApplication.translate("Solar Optimus", u"Cycle Life", None))
        self.label_16.setText(QCoreApplication.translate("Solar Optimus", u"Lifetime in Years", None))
        self.label_17.setText(QCoreApplication.translate("Solar Optimus", u"Battery Strings in Parallel", None))
        self.label_18.setText(QCoreApplication.translate("Solar Optimus", u"Battery Strings in Series", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Solar Optimus", u"PCU", None))
        self.label_9.setText(QCoreApplication.translate("Solar Optimus", u"Charge Control Efficiency [%]", None))
        self.label_10.setText(QCoreApplication.translate("Solar Optimus", u"Inverter Efficiency [%]", None))
        self.label_29.setText(QCoreApplication.translate("Solar Optimus", u"Max Charge Current [A]", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Solar Optimus", u"3 - System parameters", None))
        self.pushButton_5.setText(QCoreApplication.translate("Solar Optimus", u"Launch Tool", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Solar Optimus", u"Precise value of ENS/LOL - Percentage", None))
        self.label_28.setText(QCoreApplication.translate("Solar Optimus", u"Energy Not Supplied (ENS) [%]:", None))
        self.WatValue_2.setText(QCoreApplication.translate("Solar Optimus", u"10", None))
        self.pushButton_12.setText(QCoreApplication.translate("Solar Optimus", u"Download raw data", None))
        self.pushButton_15.setText(QCoreApplication.translate("Solar Optimus", u"Sample New Day", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("Solar Optimus", u"Parameters to plot:", None))
        self.checkBox_9.setText(QCoreApplication.translate("Solar Optimus", u"Battery SOC [%]", None))
        self.checkBox_8.setText(QCoreApplication.translate("Solar Optimus", u"Load Demand [W]", None))
        self.checkBox_6.setText(QCoreApplication.translate("Solar Optimus", u"Panel Power [W]", None))
        self.checkBox_7.setText(QCoreApplication.translate("Solar Optimus", u"Battery Power [W]", None))
        self.pushButton_17.setText(QCoreApplication.translate("Solar Optimus", u"Clear Last Trace", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("Solar Optimus", u"Sample Day", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Solar Optimus", u"Battery Analysis", None))
        self.label_30.setText(QCoreApplication.translate("Solar Optimus", u"Lifetime in years:", None))
        self.label_31.setText(QCoreApplication.translate("Solar Optimus", u"Final Capacity", None))
        self.WatValue_3.setText(QCoreApplication.translate("Solar Optimus", u"10", None))
        self.BatValue_3.setText(QCoreApplication.translate("Solar Optimus", u"3", None))
        self.pushButton_16.setText(QCoreApplication.translate("Solar Optimus", u"Clear Last Trace", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_8), QCoreApplication.translate("Solar Optimus", u"Battery Analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Solar Optimus", u"4 - Verification", None))
        self.pushButton_13.setText(QCoreApplication.translate("Solar Optimus", u"Save", None))
        self.pushButton_14.setText(QCoreApplication.translate("Solar Optimus", u"Restore Default", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Solar Optimus", u"PV-Modeling", None))
        self.label_32.setText(QCoreApplication.translate("Solar Optimus", u"Losses due to shading by surrounding houses or trees...", None))
        self.label_33.setText(QCoreApplication.translate("Solar Optimus", u"Loss due to mismatch between modules of the PV-array. ", None))
        self.label_34.setText(QCoreApplication.translate("Solar Optimus", u"Loss of energy due to the connectors in the system.", None))
        self.label_35.setText(QCoreApplication.translate("Solar Optimus", u"Nameplate rating. Losses due to field variation from datasheet.", None))
        self.label_36.setText(QCoreApplication.translate("Solar Optimus", u"Light-induced degradation.", None))
        self.label_37.setText(QCoreApplication.translate("Solar Optimus", u"Modify the constant efficiency of the solar panel. Please refer to PVWatt's loss tool.", None))
        self.label_42.setText(QCoreApplication.translate("Solar Optimus", u"Losses in a section of cable.", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Solar Optimus", u"Soiling-Modeling", None))
        self.label_38.setText(QCoreApplication.translate("Solar Optimus", u"Modify the parameters of the soiling model. ", None))
        self.label_39.setText(QCoreApplication.translate("Solar Optimus", u"Refer to PVLib's documentation.", None))
        self.label_40.setText(QCoreApplication.translate("Solar Optimus", u"Rate at which PV is cleaned:", None))
        self.label_41.setText(QCoreApplication.translate("Solar Optimus", u"Amount of rain need to clean the PV:", None))
        self.label_43.setText(QCoreApplication.translate("Solar Optimus", u"[Weeks]", None))
        self.label_44.setText(QCoreApplication.translate("Solar Optimus", u"[mm]", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Solar Optimus", u"Other", None))
        self.label_45.setText(QCoreApplication.translate("Solar Optimus", u"Mean price per W of solar panel", None))
        self.label_46.setText(QCoreApplication.translate("Solar Optimus", u"Mean price per Wh of battery", None))
        self.label_47.setText(QCoreApplication.translate("Solar Optimus", u"Load efficiency:", None))
        self.label_48.setText(QCoreApplication.translate("Solar Optimus", u"Initial state of charge:", None))
        self.label_49.setText(QCoreApplication.translate("Solar Optimus", u"[INR]", None))
        self.label_50.setText(QCoreApplication.translate("Solar Optimus", u"[INR]", None))
        self.label_51.setText(QCoreApplication.translate("Solar Optimus", u"[%]", None))
        self.label_52.setText(QCoreApplication.translate("Solar Optimus", u"[%]", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Parameters), QCoreApplication.translate("SolarOptimus", u"Parameters", None))
        self.menuSolarOptimus_Tool.setTitle(QCoreApplication.translate("SolarOptimus", u"", None))
    # retranslateUi

### TO COPY COOOOOLLLE ###

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setWindowTitle("Solar Optimus") 
        self.setWindowIcon(QIcon("logo_solar_ic.ico"))
        self.ui.setupUi(self)

        ### TAB 1: LOAD PROFILE ###

        #Browse CSV:
        self.ui.pushButton_18.clicked.connect(lambda: self.open_file_dialog())
        self.file_path = ""
        # Adding removing lines from first table
        self.ui.pushButton_2.clicked.connect(lambda: self._addRow(self.ui.tableWidget))
        self.ui.pushButton_3.clicked.connect(lambda: self._removeRow(self.ui.tableWidget))
        # Adding removing lines from second table
        self.ui.pushButton_7.clicked.connect(lambda: self._addRow(self.ui.tableWidget_3))
        self.ui.pushButton_6.clicked.connect(lambda: self._removeRow(self.ui.tableWidget_3))
        # Adding removing lines from third table
        self.ui.pushButton_9.clicked.connect(lambda: self._addRow(self.ui.tableWidget_4))
        self.ui.pushButton_8.clicked.connect(lambda: self._removeRow(self.ui.tableWidget_4))    
        # Adding removing lines from fourth table
        self.ui.pushButton_11.clicked.connect(lambda: self._addRow(self.ui.tableWidget_5))
        self.ui.pushButton_10.clicked.connect(lambda: self._removeRow(self.ui.tableWidget_5))  

        #Copying the active view to other tables
        self.ui.pushButton.clicked.connect(lambda: self._copyTable())

        ### TAB 2: FIRST OPTIMIZATION ###
        self.ui.WatValue.hide()  # Hide results
        self.ui.BatValue.hide()  # Hide results
        #To modify to optimize function
        self.ui.pushButton_4.clicked.connect(lambda: logic.launchOpti(self))
        self.ui.progressBar.setValue(0)
        
        # Create a button group and make it exclusive
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.ui.checkBox, SystemMode.FULL_RELIABILITY.value)
        self.button_group.addButton(self.ui.checkBox_2, SystemMode.RELIABILITY.value)
        self.button_group.addButton(self.ui.checkBox_3, SystemMode.BALANCED.value)
        self.button_group.addButton(self.ui.checkBox_4, SystemMode.PRICE.value)
        self.button_group.addButton(self.ui.checkBox_5, SystemMode.FULL_PRICE.value)
        for button in self.button_group.buttons():
            button.setEnabled(False)  # or True to re-enable
        # Graph elements
        # --- Create matplotlib graph in GrapWidget (tab_3) ---
        self.canvas = MplCanvas(self.ui.GrapWidget, width=5, height=4, dpi=100)
        self.pick_connection_id = None
        self.hover_connection_id = None
        toolbar = NavigationToolbar(self.canvas, self)

        # Layout inside GrapWidget (assumed from Qt Designer)
        layout = QVBoxLayout(self.ui.GrapWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        #Change the plot with the selectors buttons:
                # Define custom names
        self.names = ["checkBox", "checkBox_2", "checkBox_3", "checkBox_4", "checkBox_5"]

        for name in self.names:
            cb = getattr(self.ui, name)  # Get the actual checkbox object
            cb.toggled.connect(lambda state, n=name: self.handle_checkbox(n, state))

        #Store info for which points where selected
        self.selected_indices = []
        self.arrow_artists = []
        
        #Define a timer class to delay the appearance of system info upon hover
        self.hover_timer = QTimer()
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self._show_tooltip)
        self.pending_hover_index = None  # To store which point we're hovering over

        #Store color
        self.point_colors = []
        self.just_launched = True

        ### TAB 3: SECOND OPTIMIZATION ###

        #Battery Graph
        self.canvas_3 = MplCanvas(self.ui.GrapWidget_3, width=5, height=4, dpi=100)
        toolbar_3 = NavigationToolbar(self.canvas_3, self)
        self.ui.progressBar_2.setValue(0)

        # Layout inside GrapWidget (assumed from Qt Designer)
        layout_3 = QVBoxLayout(self.ui.GrapWidget_3)
        layout_3.setContentsMargins(0, 0, 0, 0)
        layout_3.addWidget(toolbar_3)
        layout_3.addWidget(self.canvas_3)

        self.canvas_2 = MplCanvas(self.ui.GrapWidget_2, width=5, height=4, dpi=100)
        toolbar_2 = NavigationToolbar(self.canvas_2, self)

        # Layout inside GrapWidget (assumed from Qt Designer)
        layout_2 = QVBoxLayout(self.ui.GrapWidget_2)
        layout_2.setContentsMargins(0, 0, 0, 0)
        layout_2.addWidget(toolbar_2)
        layout_2.addWidget(self.canvas_2)

        #Launch the code
        self.design_year = 5
        self.df_final = []
        self.df_bat = []
        self.ui.pushButton_5.clicked.connect(lambda: logic.launchVerification(self))
        self.ui.pushButton_15.clicked.connect(lambda: self._resampleSystem())
        self.ui.pushButton_16.clicked.connect(lambda: self._clearLastPlot())
        #Hide any results before launch
        self.ui.WatValue_2.hide()  # Hide results
        self.ui.WatValue_3.hide()
        self.ui.BatValue_3.hide()
        self.ui.pushButton_12.clicked.connect(self._saveFile)
        self.ui.pushButton_12.setEnabled(False)

        self.one_day_df = []
        for checkbox in [self.ui.checkBox_6, self.ui.checkBox_7, self.ui.checkBox_8, self.ui.checkBox_9]:
            checkbox.stateChanged.connect(lambda: self._updateSystemPlot())

        self.ui.pushButton_17.clicked.connect(lambda: self._clearLastSystPlot())

        ### TAB 4: PARAMETERS MODIFICATIONS ###
        #Default values for PV-Panel etas
        self.shadingEta = 2 #[%]
        self.mismatchEta = 2 #[%]
        self.connectEta = 0.05 #[%]
        self.nameplateEta = 1 #[%]
        self.lightEta = 0.15 #[%]
        self.cableEta =  2 #[%]
        #Default values for soiling modeling
        self.cleaningFreq = 12 #[weeks]
        self.rainClean = 7 #[mm]
        #Default values for others
        self.pricePerW = 31 #[INR]
        self.pricePerWh = 15 #[INR]
        self.loadEta = 85 #[%]
        self.initStateBat = 50 #[%]
        #Set initial values
        self._setdefaultvalues()
        #Connect restore value
        self.ui.pushButton_14.clicked.connect(lambda: self._setdefaultvalues())
        #self._set_all_default_values()


# --- ACTION FUNCTIONS: FIRST OPTIMIZATION ---

     # --- Opens file dialog for file selection by the user ---
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,                         # parent
            "Open File",                  # dialog title
            "",                           # initial directory
            "Data Files (*.csv *.xls *.xlsx);;CSV Files (*.csv);;Excel Files (*.xls *.xlsx);;All Files (*)"
        )
        if file_path:
            self.ui.textEdit_31.setText(file_path)
            self.file_path = file_path
        else:
            self.ui.textEdit_31.setText("")

    def _disable_button(self):
        """
        Disables all buttons in the button group (checkboxes) and clears their selection.
        """
        self.button_group.setExclusive(False)  # allow deselecting all buttons
        for button in self.button_group.buttons():
            button.setChecked(False)
            button.setEnabled(False)
        self.button_group.setExclusive(True)   # restore exclusivity

    def _draw_comparison(self):
        """
        Draws green and orange arrows and text annotations on the pareto plot to compare two selected points.
        It compares price hikes and ENS difference between the two points
        """
        # Clear previous arrows
        for artist in self.arrow_artists:
            if hasattr(artist, 'remove'):
                artist.remove()
        self.arrow_artists.clear()

        idx1, idx2 = self.selected_indices
        pt1 = self.df.iloc[idx1]
        pt2 = self.df.iloc[idx2]

        A = (pt1["ENS"], pt1["Cost"])
        B = (pt2["ENS"], pt2["Cost"])
        ax = self.canvas.axes

        # Make sure A is always the leftmost point
        if A[0] > B[0]:
            A, B = B, A

        # Horizontal ΔENS arrow
        ens_arrow = FancyArrowPatch(
            posA=A, posB=(B[0], A[1]),
            arrowstyle='<-',
            color='green',
            linestyle='--',
            lw=1,
            clip_on=True,
            mutation_scale= 15
        )
        ax.add_patch(ens_arrow)
        self.arrow_artists.append(ens_arrow)

        # Vertical ΔCost arrow
        cost_arrow = FancyArrowPatch(
            posA=(B[0], A[1]), posB=B,
            arrowstyle='<-',
            color='orange',
            linestyle='--',
            lw=1,
            clip_on=True, 
            mutation_scale=15 
        )
        ax.add_patch(cost_arrow)
        self.arrow_artists.append(cost_arrow)

        # Calculate deltas
        delta_ens = -abs(A[0] - B[0]) * 100
        delta_cost = (1 - min(A[1], B[1]) / max(A[1], B[1])) * 100

        # Text labels
        text1 = ax.text(
            (A[0] + B[0]) / 2, A[1] + 0.005,
            f'{delta_ens:.1f}% ENS',
            ha='center', color='green', fontsize=8, clip_on=True
        )
        self.arrow_artists.append(text1)

        text2 = ax.text(
            B[0] + 0.0005, (A[1] + B[1]) / 2,
            f'+{delta_cost:.1f}% Cost',
            va='center', color='orange', fontsize=8, clip_on=True
        )
        self.arrow_artists.append(text2)

        self.canvas.draw_idle()
    
    def _clear_arrows(self):
        """
        Removes all comparison arrows and annotations from the pareto plot.
        """
        for artist in self.arrow_artists:
            if hasattr(artist, 'remove'):
                try:
                    artist.remove()
                except NotImplementedError:
                    print(f"Warning: Artist {artist} could not be removed (NotImplementedError).")
        self.arrow_artists.clear()
        self.canvas.draw_idle()

    def resample_graph(self, df_res, lower_bound, upper_bound):

        """
        Filters and samples points in a specified ENS range and leaves only three points.
        Returns a DataFrame. Facilitate choice of designer
        """

        #Make sure that the arrow list and state is reset after each resampling
        self.selected_indices.clear()
        self._clear_arrows()

        self.just_launched = False

            # Filter the DataFrame to the ENS interval
        df_filtered = df_res[(df_res["ENS"] >= lower_bound) & (df_res["ENS"] <= upper_bound)].copy()

        if df_filtered.empty or len(df_filtered) < 3:
            print("Not enough points in the selected ENS range.")
            return None

        ens_center = (lower_bound + upper_bound) / 2
        reliable_point = df_filtered.loc[df_filtered["ENS"].idxmin()]
        cheap_point = df_filtered.loc[df_filtered["Cost"].idxmin()]

        df_filtered["ens_dist"] = (df_filtered["ENS"] - ens_center).abs()
        balanced_point = df_filtered.loc[df_filtered["ens_dist"].idxmin()]
        df_filtered.drop(columns=["ens_dist"], inplace=True)
        df_sampled = pd.DataFrame([reliable_point, balanced_point, cheap_point]).drop_duplicates()

        # 👉 Copy the first point and append it to the end
        if not df_sampled.empty:
            first_point_copy = df_sampled.iloc[0].copy()
            df_sampled = pd.concat([df_sampled, pd.DataFrame([first_point_copy])], ignore_index=True)

        return df_sampled.reset_index(drop=True)

    def handle_checkbox(self, name, check):
        """
        Handles checkbox selection and triggers appropriate graph resampling.
        """
        if check and hasattr(self, 'df_full'):
            if name == "checkBox":
                df = self.resample_graph(self.df_full, lower_bound=0.0, upper_bound=0.01)
            elif name == "checkBox_2":
                df = self.resample_graph(self.df_full, lower_bound=0.01, upper_bound=0.03)
            elif name == "checkBox_3":
                df = self.resample_graph(self.df_full, lower_bound=0.03, upper_bound=0.06)
            elif name == "checkBox_4":
                df = self.resample_graph(self.df_full, lower_bound=0.06, upper_bound=0.09)
            elif name == "checkBox_5":
                df = self.resample_graph(self.df_full, lower_bound=0.09, upper_bound=0.15)
            else:
                df = self.df_full

            if df.empty:
                print("No points in this ENS range.")
                return

            cheapest_point = df.loc[df["Cost"].idxmin()]
            x_opt = cheapest_point["ENS"]
            y_opt = cheapest_point["Cost"]
            self._updatePlot(df, x_opt, y_opt)
            self._printOptimized(str(cheapest_point["P_pv"]), str(cheapest_point["C_bat"]))

    def on_pick(self, event, idx_opt):
        """
        Handles point selection on the scatter plot and toggles comparison of different points/systems
        """
        if event.ind is None or len(event.ind) == 0:
            return

        ind = int(event.ind[-1])  # Ensure it's a Python int

        # Toggle selection
        if ind in self.selected_indices:
            if ind == idx_opt:
                self.selected_indices.remove(ind)
                self.point_colors[ind] = 'red'
                self._clear_arrows()
            else:
                self.selected_indices.remove(ind)
                self.point_colors[ind] = 'blue'
                self._clear_arrows()
        else:
            self.selected_indices.append(ind)
            self.point_colors[ind] = 'green'

        # Update point colors
        self.points.set_facecolor(self.point_colors)
        self.canvas.draw_idle()

        # Draw arrows only when exactly 2 points are selected
        if len(self.selected_indices) == 2:
            self._draw_comparison()

    def on_hover(self, event):
        """
        Handles hover events over points to show tooltips with a delay.
        """
        if event.inaxes != self.canvas.axes:
            self.hover_timer.stop()
            self.pending_hover_index = None
            QToolTip.hideText()
            return

        cont, ind = self.points.contains(event)
        if not cont or 'ind' not in ind or len(ind['ind']) == 0:
            self.hover_timer.stop()
            self.pending_hover_index = None
            QToolTip.hideText()
            return

        i = ind['ind'][0]
        if self.pending_hover_index != i:
            # Only restart timer if we moved to a new point
            self.hover_timer.stop()
            self.pending_hover_index = i
            self.hover_timer.start(1000)  # 500 milliseconds delay

    def _show_tooltip(self):
        """
        Displays a tooltip with information about the hovered point.
        """
        i = self.pending_hover_index
        if i is None:
            return

        data = self.custom_data[i]
        tooltip = (
            f"Ppv: {round(data['P_pv'],1)} W\n"
            f"Cbat: {round(data['C_bat'],1)} Wh\n"
            f"ENSP: {round(data['ENS']*100,1)} %"
        )
        QToolTip.showText(QCursor.pos(), tooltip, self.canvas)

    def _updatePlot(self, df_res, x_opt = None, y_opt = None):
        """
        Updates the scatter parreto plot and point colors, including recommended points.
        """

        if x_opt is not None and y_opt is not None:
            df_res["recommended"] = (df_res["ENS"] == x_opt) & (df_res["Cost"] == y_opt)
        else:
            df_res["recommended"] = False
        
        #Color information
        num_points = len(df_res)
        default_color = 'blue'
        self.point_colors = [default_color] * num_points
        idx_opt = df_res.index[df_res["recommended"]]
        self.point_colors = ['red' if recommended else default_color for recommended in df_res["recommended"]]
  
        #Disconnect previous hover and clicking connections
        if self.pick_connection_id is not None:
            self.canvas.mpl_disconnect(self.pick_connection_id)
            self.pick_connection_id = None
        if self.hover_connection_id is not None:
            self.canvas.mpl_disconnect(self.hover_connection_id)
            self.hover_connection_id = None

        for button in self.button_group.buttons():
            button.setEnabled(True)  # or True to re-enable
        # Clear previous content
        self.df = df_res.copy() 
        self.canvas.axes.clear()
        self.canvas.axes.set_xlabel("Energy Not Supplied Ratio", fontsize=9)
        self.canvas.axes.set_ylabel("Normalized System Cost", fontsize=9)
        self.canvas.axes.set_title("Pareto Front: ENS ratio vs. Price")
        self.canvas.figure.tight_layout()
        x = df_res["ENS"]
        y = df_res["Cost"]

        self.custom_data = df_res[["P_pv", "C_bat", "ENS"]].to_dict(orient="records")
        self.points = self.canvas.axes.scatter(x, y, s=50, c=self.point_colors, picker=3, zorder=2, clip_on=True)
        offset = 0.002

        if x_opt is not None and y_opt is not None:
            red_patch = mpatches.Patch(color='red', label='Best system')
            self.canvas.axes.legend(
                handles=[red_patch],
                loc='lower left',          # Position
                fontsize=8,                # Reduce font size
                frameon=True,              # Add a legend frame (optional)
                fancybox=True,             # Rounded box
                framealpha=0.8,            # Slight transparency
                borderpad=0.5              # Padding around the legend text
            )
            
        x_min, x_max = self.canvas.axes.get_xlim()
        y_min, y_max = self.canvas.axes.get_ylim()
        self.canvas.axes.set_xlim(x_min - 0.005, x_max + 0.005)
        padding = 0.05 * (y_max - y_min)
        self.canvas.axes.set_ylim(max(0, y_min - padding), min(1, y_max + padding))
        self.canvas.axes.grid(True, which='both', linestyle='--', color='gray', alpha=0.5)

        # Connect picking (clicking) for selecting points
        if self.just_launched == False:
            # Suppose you want to pass 'my_data' to your on_pick function
            self.pick_connection_id = self.canvas.mpl_connect("pick_event",lambda event: self.on_pick(event, idx_opt))
            self.hover_connection_id = self.canvas.mpl_connect("motion_notify_event",self.on_hover)

        self.canvas.figure.tight_layout()
        self.canvas.draw_idle() 

    def _printOptimized(self, Ppv, Cbat):
        """
        Displays the recommended system configuration values on the GUI.
        """
        self.ui.WatValue.setText(Ppv)
        self.ui.BatValue.setText(Cbat)
        self.ui.WatValue.show()  # Show results
        self.ui.BatValue.show()  # Show results 

    def _addRow(self, table):
        """
        Adds a new row to the given table widget.
        """
        rowCount = table.rowCount()
        table.insertRow(rowCount)

    def _removeRow(self, table):
        """
        Removes the last row from the given table widget if any exist.
        """
        if table.rowCount() > 0:
            table.removeRow(table.rowCount()-1)

    def _copyTable(self):
        """
        Copies the contents of the current tab's table to all other tables.
        """

        self.table_widgets = [self.ui.tableWidget, self.ui.tableWidget_3, self.ui.tableWidget_4, self.ui.tableWidget_5]
        
        current_index = self.ui.tabWidget_2.currentIndex()
        tab_container = self.ui.tabWidget_2.widget(current_index)
        table = tab_container.findChild(QTableWidget)

        if table:
            rows = table.rowCount()
            cols = table.columnCount()
        else:
           print("No table found in active tab")

        for idx, target_table in enumerate(self.table_widgets):
            if idx == current_index:
                continue  # Skip the source table itself

            # Ensure same size
            target_table.setRowCount(rows)
            target_table.setColumnCount(cols)

            for i in range(rows):
                for j in range(cols):
                    item = table.item(i, j)
                    if item:
                        target_table.setItem(i, j, QTableWidgetItem(item.text()))
                    else:
                        target_table.setItem(i, j, QTableWidgetItem(""))

    
    def _updateProgress(self, value):
        """
        Updates the progress bar in the GUI.
        """
        self.ui.progressBar.setValue(value)
        QApplication.processEvents()

     # --- Inputs error function ---
    def _return_error(self, error_text):
        """
        Displays an error message on a button for a limited time.
        """
        button = self.ui.pushButton_4
        original_text = button.text()
        palette = button.palette()
        original_palette = QPalette(palette)  # Save full original palette

        # Set text color to red
        palette.setColor(QPalette.ButtonText, QColor("red"))
        button.setPalette(palette)
        button.setText(error_text)
        button.setDisabled(True)

        def reset():
            button.setDisabled(False)
            button.setPalette(original_palette)
            button.setText(original_text)

        QTimer.singleShot(5000, reset) 

# --- ACTION FUNCTIONS: SECOND OPTIMIZATION ---

    def _return_error_2(self, error_text):
        """
        Displays an error message on a button for a limited time.
        """
        button = self.ui.pushButton_5
        original_text = button.text()
        palette = button.palette()
        original_palette = QPalette(palette)  # Save full original palette

        # Set text color to red
        palette.setColor(QPalette.ButtonText, QColor("red"))
        button.setPalette(palette)
        button.setText(error_text)
        button.setDisabled(True)

        def reset():
            button.setDisabled(False)
            button.setPalette(original_palette)
            button.setText(original_text)

        QTimer.singleShot(5000, reset) 

    def _showBatteryInfo(self, lifetime, capacity_design):
        self.ui.WatValue_3.setText(lifetime)
        self.ui.BatValue_3.setText(capacity_design)
        self.ui.WatValue_3.show()  # Show results
        self.ui.BatValue_3.show()  # Show results

    def _showfinalInfo(self, ENS):
        self.ui.WatValue_2.show()
        self.ui.WatValue_2.setText(ENS)

    def _clearLastPlot(self):
        """
        Removes the last DataFrame from the list and refreshes the battery plot.
        """
        if len(self.df_bat)>=1:
            self.df_bat.pop()  # Remove last element
            self._refreshBatteryPlot()  # Refresh with updated list

    def _refreshBatteryPlot(self):
        """
        Redraws the battery plot from the current list of DataFrames.
        """
        self.canvas_3.axes.clear()
        self.canvas_3.axes.set_ylabel("System health [%]", fontsize=8)
        self.canvas_3.axes.set_title("Battery health over time", fontsize=8)
        #self.canvas_3.axes.axvline(x=df_plot.index[-1]design_year, label= 'End of design time')
        self.canvas_3.figure.tight_layout()

        # Plot each DataFrame
        for i, df_plot in enumerate(self.df_bat):
            x = df_plot.index
            y = df_plot["Battery SOH"] * 100
            self.canvas_3.axes.plot(
                x, y,
                linewidth=2,
                zorder=2,
                clip_on=True,
                label=f'Sample {i+1}'
            )

        # Add horizontal line for replacement limit
        self.canvas_3.axes.axhline(
            y=80, color='red', linestyle='--', linewidth=1, label='Replacement Limit'
        )

        start_time = self.df_bat[0].index[0]
        design_end_time = start_time + pd.DateOffset(years=self.design_year)

        self.canvas_3.axes.axvline(
            x=design_end_time,
            color='gold',
            linestyle='--',
            linewidth=1.5,
            label=f'End of {self.design_year}y design'
        )

        # Add grid and legend
        self.canvas_3.axes.grid(True, which='both', linestyle='--', color='gray', alpha=0.5)
        self.canvas_3.axes.tick_params(axis='x', labelsize=7, labelcolor='black')
        self.canvas_3.axes.tick_params(axis='y', labelsize=7, labelcolor='black')
        self.canvas_3.axes.legend(fontsize=6)
        self.canvas_3.figure.tight_layout()
        self.canvas_3.draw_idle()

    def _updateBatteryplot(self, df):
        """
        Updates the battery plot by adding the new DataFrame to the list
        and refreshing the entire plot.
        """
        self.df_bat.append(df.copy())
        self._refreshBatteryPlot()

    def _resampleSystem(self, day=None):
        """
        Takes a list of timezone-aware DataFrames and creates a one-day sample from each,
        then updates the plot for each DataFrame.

        Parameters:
        - df_list: list of DataFrames (each with a datetime index)
        - day: optional, specific day to extract; if None, picks one randomly from the first DataFrame.

        Returns:
        - one_day_dfs: list of DataFrames corresponding to one day each.
        """
        if len(self.df_final)>=1:

            one_day_dfs = []
            df_list = self.df_final.copy()

            # Choose the day
            if day is None:
                unique_days = df_list[-1].index.normalize().unique()
                day = np.random.choice(unique_days)
            else:
                day = pd.to_datetime(day).date()

            # Convert to naive Timestamp
            naive_day = pd.Timestamp(day)

            # Process each DataFrame in the list
            for df in df_list:
                # If the DataFrame is timezone-aware, localize or convert
                if df.index.tz is not None:
                    try:
                        localized_day = naive_day.tz_localize(df.index.tz)
                    except TypeError:
                        # Already tz-aware: convert instead
                        localized_day = naive_day.tz_convert(df.index.tz)
                else:
                    localized_day = naive_day

                # Filter by date while preserving timezone
                mask = df.index.normalize() == localized_day
                one_day_df = df.loc[mask]
                one_day_dfs.append(one_day_df)

            # Plot the first DataFrame as a representative plot
            self.one_day_df = one_day_dfs

            if one_day_dfs:
                self._updateSystemPlot()

    def _clearLastSystPlot(self):
        """
        Removes the last DataFrame from the list and refreshes the battery plot for the System Plot
        """
        if len(self.df_final)>=1 and len(self.one_day_df)>=1:
            self.df_final.pop()  # Remove last element
            self.one_day_df.pop()
            self._updateSystemPlot()

    def _updateSystemPlot(self):
        """
        Updates the battery plot with multiple curves from a list of DataFrames,
        plotting only the variables selected by the user via checkboxes.
        Uses different shades per scenario for each parameter.
        Includes the day of the data in the plot title.
        """

        if not self.one_day_df:
            self.canvas_2.figure.clf()
            self.canvas_2.draw()
            return

        df_list = self.one_day_df.copy()
        self.canvas_2.figure.clear()
        self.canvas_2.axes = self.canvas_2.figure.add_subplot(111)

        if not df_list:
            return  # handle empty list gracefully

        # Use the first DataFrame's date as the title reference
        first_df = df_list[0]
        day_str = first_df.index[0].strftime('%Y-%m-%d') if isinstance(first_df.index, pd.DatetimeIndex) else "Unknown Date"
        x = pd.date_range(start=f"{day_str} 00:00:00", end=f"{day_str} 23:30:00", freq="30min")

        # Checkboxes
        plot_output_power = self.ui.checkBox_6.isChecked()
        plot_load_power = self.ui.checkBox_8.isChecked()
        plot_battery_power = self.ui.checkBox_7.isChecked()
        plot_battery_soc = self.ui.checkBox_9.isChecked()

        n_scenarios = len(df_list)
        color_indices = np.linspace(0.5, 0.9, n_scenarios)

        # Plot each DataFrame with shades of the base color
        for i, df in enumerate(df_list):
            scenario_label = f"Sim {i+1}"

            if plot_output_power:
                y2 = df["Output Power"]
                self.canvas_2.axes.plot(
                    x, y2,
                    label=f"{scenario_label} - Panel Power [W]",
                    color=cm.Blues(color_indices[i]),
                    linewidth=2,
                    zorder=2,
                    clip_on=True,
                    alpha=1
                )
            if plot_load_power:
                y3 = df["Load Power"]
                self.canvas_2.axes.plot(
                    x, y3,
                    label=f"{scenario_label} - Load Demand [W]",
                    color=cm.Greens(color_indices[i]),
                    linewidth=2,
                    zorder=2,
                    clip_on=True,
                    alpha=1
                )
            if plot_battery_power:
                y4 = df["Battery Power"]
                self.canvas_2.axes.plot(
                    x, y4,
                    label=f"{scenario_label} - Battery Power [W]",
                    color=cm.Reds(color_indices[i]),
                    linewidth=2,
                    zorder=2,
                    clip_on=True,
                    alpha=1
                )

        # Twin y-axis for Battery SOC
        ax2 = self.canvas_2.axes.twinx()
        ax2.set_ylabel("Battery SOC [%]", fontsize=7)

        if plot_battery_soc:
            for i, df in enumerate(df_list):
                scenario_label = f"Sim {i+1}"  # moved inside the loop
                y1 = df["Battery SOC"] * 100
                ax2.plot(
                    x, y1,
                    label=f"{scenario_label} - Battery SOC [%]",
                    color=cm.Purples(color_indices[i]),
                    linewidth=2,
                    zorder=2,
                    clip_on=True,
                    alpha=1
                )

        # X-axis formatting
        self.canvas_2.axes.set_ylabel("Power Variable [W]", fontsize=7)
        self.canvas_2.axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.canvas_2.axes.set_title(f"System Variables Over Time ({day_str})", fontsize = 8)
        self.canvas_2.axes.tick_params(axis='x', labelsize=7, labelcolor='black', rotation=45)
        self.canvas_2.axes.tick_params(axis='y', labelsize=7, labelcolor='black')
        ax2.tick_params(axis='y', labelsize=7, labelcolor='black')

        # Grid
        self.canvas_2.axes.grid(True, which='both', linestyle='--', color='gray', alpha=0.5)

        # Combine legends from both y-axes
        lines_1, labels_1 = self.canvas_2.axes.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()

        # Remove duplicate labels
        combined = dict(zip(labels_1 + labels_2, lines_1 + lines_2))
        self.canvas_2.axes.legend(
            combined.values(), combined.keys(),
            loc='center left',
            bbox_to_anchor=(1.25, 0.5),
            fontsize=6,
            frameon=True
        )

        self.canvas_2.figure.autofmt_xdate()
        self.canvas_2.figure.subplots_adjust(right=0.65)
        self.canvas_2.figure.tight_layout()
        self.canvas_2.draw_idle()

    def _saveFile(self):
        # Initialize Tkinter root
        # Open "Save As" dialog
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        # Save the file if the user selected a file path
        if file_path:
            self.df_final[-1].to_csv(file_path, index=True, sep=';', encoding='utf-8-sig')
            print(f"File saved successfully at {file_path}")
        else:
            print("Save operation cancelled.")

    def _downloadtoggle(self, action):
        self.ui.pushButton_12.setEnabled(action) 

    def _hideFinalResult(self):
        self.ui.WatValue_2.hide()  # Hide results
        self.ui.WatValue_3.hide()
        self.ui.BatValue_3.hide()

    def _updateProgress_2(self, value):
        """
        Updates the progress bar in the GUI.
        """
        self.ui.progressBar_2.setValue(value)
        QApplication.processEvents()

# --- ACTION FUNCTIONS: MODIFY PARAMETERS ---
    def _setdefaultvalues(self):
        self.ui.textEdit_18.setPlainText(str(self.shadingEta)) #Shading
        self.ui.textEdit_20.setPlainText(str(self.mismatchEta)) #Mismatch
        self.ui.textEdit_19.setPlainText(str(self.connectEta)) #Connector
        self.ui.textEdit_23.setPlainText(str(self.nameplateEta)) #Nameplate
        self.ui.textEdit_21.setPlainText(str(self.lightEta)) #Light-induced
        self.ui.textEdit_25.setPlainText(str(self.cableEta)) #Cable
        self.ui.textEdit_26.setPlainText(str(self.pricePerW)) #INR/W
        self.ui.textEdit_27.setPlainText(str(self.pricePerWh)) #INR/Wh
        self.ui.textEdit_29.setPlainText(str(self.loadEta)) #Load
        self.ui.textEdit_28.setPlainText(str(self.initStateBat)) #Initial Battery State
        self.ui.textEdit_22.setPlainText(str(self.cleaningFreq)) #Cleaning freq
        self.ui.textEdit_24.setPlainText(str(self.rainClean)) #Rain to clean PV


# --- GETTER FUNCTIONS ---
# For first Optimisation
    def get_longitude(self):
        return self.ui.textEdit_15.toPlainText()

    def get_latitude(self):
        return self.ui.textEdit_16.toPlainText()

    def get_years(self):
        return self.ui.textEdit_17.toPlainText()

    def get_tableItem(self, idx):

        tab_container = self.ui.tabWidget_2.widget(idx)
        table = tab_container.findChild(QTableWidget)

        rows = table.rowCount()
        cols = table.columnCount()

        # get header
        headers = [table.horizontalHeaderItem(col).text() if table.horizontalHeaderItem(col) else f"Col {col}" for col in range(cols)]

        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # or None
            data.append(row_data)

        df = pd.DataFrame(data, columns=headers)
        return df
    
    def get_focus(self):
        id = self.button_group.checkedId()
        return SystemMode(id)

# For second Optimisation
    def get_power(self):
        return self.ui.textEdit.toPlainText()
    
    def get_temp_coef(self):
        return self.ui.textEdit_3.toPlainText()
    
    def get_area(self):
        return self.ui.textEdit_2.toPlainText()
    
    def get_PV_num(self):
        return self.ui.textEdit_4.toPlainText()
    
    def get_PCU_inv(self):
        return self.ui.textEdit_13.toPlainText()
    
    def get_PCU_charge(self):
        return self.ui.textEdit_14.toPlainText()
    
    def get_capa(self):
        return self.ui.textEdit_8.toPlainText()
    
    def get_height(self):
        return self.ui.textEdit_7.toPlainText()
    
    def get_mass(self):
        return self.ui.textEdit_6.toPlainText()
    
    def get_SOC_min(self):
        return self.ui.textEdit_5.toPlainText()
    
    def get_cycle(self):
        return self.ui.textEdit_9.toPlainText()
    
    def get_lifetime(self):
        return self.ui.textEdit_10.toPlainText()
    
    def get_bat_para(self):
        return self.ui.textEdit_11.toPlainText()
    
    def get_bat_series(self):
        return self.ui.textEdit_12.toPlainText()

 #For parameters variations   
    def get_param_shading(self):
        return self.ui.textEdit_18.toPlainText()
    
    def get_param_mismatch(self):
        return self.ui.textEdit_20.toPlainText()

    def get_param_connect(self):
        return self.ui.textEdit_19.toPlainText()
    
    def get_param_nameplate(self):
        return self.ui.textEdit_23.toPlainText()
    
    def get_param_light(self):
        return self.ui.textEdit_21.toPlainText()
    
    def get_param_cable(self):
        return self.ui.textEdit_25.toPlainText()
    
    def get_param_PVrate(self):
        return self.ui.textEdit_22.toPlainText()
    
    def get_param_PVrain(self):
        return self.ui.textEdit_24.toPlainText()
    
    def get_param_Wprice(self):
        return self.ui.textEdit_26.toPlainText()

    def get_param_Whprice(self):
        return self.ui.textEdit_27.toPlainText()
    
    def get_param_loadEff(self):
        return self.ui.textEdit_29.toPlainText()
    
    def get_param_SOCinit(self):
        return self.ui.textEdit_28.toPlainText()
    
    def get_max_current(self):
        return self.ui.textEdit_30.toPlainText()
    
    def get_solar_file(self):
        return self.ui.textEdit_31.toPlainText()
    
'''
    ### DEBUG TOOL ###
    def _set_all_default_values(self):
        """
        Sets default values for all user input QTextEdit fields.
        """

        # System Info (Tab 1)
        self.ui.textEdit_15.setPlainText("77.5718")  # Example default longitude
        self.ui.textEdit_16.setPlainText("34.1605")  # Example default latitude
        self.ui.textEdit_17.setPlainText("15")   # Example default years

        # Solar Panel & PCU (Tab 2)
        self.ui.textEdit.setPlainText("570")  # Example default Power
        self.ui.textEdit_2.setPlainText("2.6")  # Example default Area
        self.ui.textEdit_3.setPlainText("-0.7")  # Example default temp coef
        self.ui.textEdit_4.setPlainText("6")  # Example default PV num

        self.ui.textEdit_13.setPlainText("85")  # PCU inverter eff.
        self.ui.textEdit_14.setPlainText("91")  # PCU charge eff.

        # Battery Array (Tab 2)
        self.ui.textEdit_8.setPlainText("300")  # Battery capacity
        self.ui.textEdit_7.setPlainText("22")  # Battery height
        self.ui.textEdit_6.setPlainText("77")  # Battery mass
        self.ui.textEdit_5.setPlainText("20")  # Min SOC
        self.ui.textEdit_9.setPlainText("1500")  # Cycle life
        self.ui.textEdit_10.setPlainText("20")  # Lifetime in years
        self.ui.textEdit_11.setPlainText("2")   # Battery para
        self.ui.textEdit_12.setPlainText("3")   # Battery series
        self.ui.textEdit_30.setPlainText("15")

        print("All user input QTextEdits set to default values.")'''


        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Solar Optimus")
    window = MainWindow()
    window.show()

    # Trigger return_error after 2 seconds
    #QTimer.singleShot(10000, window.get_inverter_efficiency)

    sys.exit(app.exec_())

