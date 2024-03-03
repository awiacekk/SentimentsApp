from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit, QTableWidgetItem, QFileDialog
from models import Models


class Ui_MainWindow(object):

    def __init__(self):
        self.row = 1
        self.col = 3
        self.models = Models()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1302, 630)
        MainWindow.setWindowIcon(QtGui.QIcon("icon.jpg"))
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(970, 440, 331, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setGeometry(QtCore.QRect(720, 380, 171, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setDisabled(True)
        self.pushButton.clicked.connect(self.textToSentiment)
        self.pushButton2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton2.setGeometry(QtCore.QRect(720, 380, 171, 51))
        self.pushButton2.setObjectName("pushButton_2")
        self.pushButton2.clicked.connect(self.loadFiles)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.pushButton2)
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.comboBox)
        self.comboBox.setGeometry(QtCore.QRect(720, 430, 171, 51))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Model Without Feature Selection")
        self.comboBox.addItem("Model With Feature Selection")
        self.textBox = QTextEdit(self.centralwidget)
        self.textBox.setGeometry(QtCore.QRect(0, 440, 971, 131))
        self.textBox.setObjectName("textBox")
        self.textBox.setFont(QFont("Arial", 10))
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(0, 0, 1301, 431))
        self.table.setObjectName("tableWidget")
        self.table.setRowCount(self.row)
        self.table.setColumnCount(self.col)
        self.table.setItem(0, 0, QTableWidgetItem("SENTENCE"))
        self.table.setItem(0, 1, QTableWidgetItem('SENTIMENT'))
        self.table.setItem(0, 2, QTableWidgetItem('MODEL'))
        self.table.setColumnWidth(0, 1030)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def loadFiles(self):
        file = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.models.loadSavedModels(file)
        self.pushButton.setDisabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SentimentsApp"))
        self.pushButton.setText(_translate("MainWindow", "Add"))
        self.pushButton2.setText(_translate("MainWindow", "Choose File"))

    def textToSentiment(self):
        text = self.textBox.toPlainText()

        if self.comboBox.currentText() == "model1":
            returned = self.models.calculateModel1(text)
        else:
            returned = self.models.calculateModel2(text)

        self.textBox.setText("")
        self.table.setItem(self.row - 1, 0, QTableWidgetItem(text))
        self.table.setItem(self.row - 1, 1, QTableWidgetItem(returned))
        if self.comboBox.currentText() == "Model Without Feature Selection":
            name = "Model1"
        else:
            name = "Model2"
        self.table.setItem(self.row - 1, 2, QTableWidgetItem(name))
        self.row += 1
        self.table.setRowCount(self.row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
