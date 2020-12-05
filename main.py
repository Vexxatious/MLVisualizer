from KNN import KNN
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import ctypes

Algorithms = {"K Nearest Neighbor": KNN}
Datasets = {"K Nearest Neighbor": [{'k': [[1,3],[2,1],[1,4],[2,2]], 'r':[[6,5],[6,7],[8,6],[7,7]]}]}

current_algorithm = None
current_dataset = None
parameters = []

class KNNGUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 113)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 281, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.KCounter = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.KCounter.setObjectName("KCounter")
        self.horizontalLayout.addWidget(self.KCounter)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 60, 281, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.RunButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.RunButton.setObjectName("RunButton")
        self.gridLayout.addWidget(self.RunButton, 0, 0, 1, 1)

        self.RunButton.clicked.connect(self.runButtonCheck)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def runButtonCheck(self):
        global parameters
        if self.KCounter.value() <= len(current_dataset):
            ctypes.windll.user32.MessageBoxW(0, "K shouldn't be less than number of groups", "Warning", 0)
            return
        parameters.append(self.KCounter.value())
        Dialog.accept()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Choose K"))
        self.RunButton.setText(_translate("Dialog", "Run"))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(621, 378)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 621, 381))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newModel = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.newModel.setObjectName("newModel")
        self.horizontalLayout.addWidget(self.newModel)
        self.LoadModel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.LoadModel.setObjectName("LoadModel")
        self.horizontalLayout.addWidget(self.LoadModel)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 1)
        self.AlgorithmCombo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.AlgorithmCombo.setObjectName("AlgorithmCombo")
        self.AlgorithmCombo.addItems(["Linear Regression","K Nearest Neighbor","Support Vector Machine"])
        self.gridLayout.addWidget(self.AlgorithmCombo, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.DatasetCombo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.DatasetCombo.setObjectName("DatasetCombo")
        self.horizontalLayout_2.addWidget(self.DatasetCombo)
        self.LoadDataset = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.LoadDataset.setObjectName("LoadDataset")
        self.horizontalLayout_2.addWidget(self.LoadDataset)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 2, 1, 1)
        self.ContinueButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ContinueButton.setObjectName("ContinueButton")
        self.gridLayout.addWidget(self.ContinueButton, 3, 0, 1, 1)

        self.newModel.stateChanged.connect(self.checkLoadButton)
        self.AlgorithmCombo.currentIndexChanged.connect(self.checkAlgorithmCombo)
        self.ContinueButton.clicked.connect(self.checkContinueButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Choose Model"))
        self.newModel.setText(_translate("Dialog", "New"))
        self.LoadModel.setText(_translate("Dialog", "Load"))
        self.label_5.setText(_translate("Dialog", "Choose Dataset"))
        self.label.setText(_translate("Dialog", "Choose Algorithm"))
        self.LoadDataset.setText(_translate("Dialog", "Load"))
        self.ContinueButton.setText(_translate("Dialog", "Continue"))

    def checkLoadButton(self):
        self.LoadModel.setEnabled(not self.newModel.isChecked())

    def checkAlgorithmCombo(self):
        if self.AlgorithmCombo.currentIndex() == 1:
            self.newModel.setEnabled(False)
            self.LoadModel.setEnabled(False)
            self.DatasetCombo.addItems(["Dataset 1","Dataset 2"])

    def checkContinueButton(self):
        global current_algorithm,current_dataset
        if self.AlgorithmCombo.currentIndex() != -1 and self.DatasetCombo.currentIndex() != -1:
            if self.AlgorithmCombo.currentText() == "K Nearest Neighbor":
                current_algorithm = "K Nearest Neighbor"
                current_dataset = Datasets[self.AlgorithmCombo.currentText()][self.DatasetCombo.currentIndex()]
                Dialog.accept()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()

    if current_algorithm != None and current_dataset != None:
        gui = KNNGUI()
        gui.setupUi(Dialog)
        Dialog.show()
        app.exec_()
        algorithm = Algorithms[current_algorithm](current_dataset,parameters)

