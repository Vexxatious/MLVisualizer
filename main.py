from KNN import KNN
from nn import NN
import nn
from LinearRegression import LinearRegression
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog
import random

Algorithms = {"K Nearest Neighbor": KNN,"Linear Regression": LinearRegression,"Neural Network": NN}
Datasets = {"K Nearest Neighbor": [{'r': [[1,3],[2,1],[1,4],[2,2]], 'g':[[6,5],[6,7],[8,6],[7,7]]},
                                   {'r': [[4,4],[3,4],[4,5],[3,5],[3.5,6],[3.5,4]], 'g':[[2,5],[2,4],[3.5,2],[4,2],[5,4],[5,5],[4,7],[3,3],[2.5,3],[2.5,6],[3,7],[4.5,3],[2.5,4],[5.6,6]]},
                                   {'r': [[1,3],[2,1],[1,4],[2,2]], 'g':[[6,2],[6,3],[8,1],[7,3]], 'b':[[4,7],[6,8],[3,6],[7,8]]}],
            "Linear Regression": [[[1,2],[2,3],[4,5],[6,7],[8,9]]],
            "Neural Network": ["mnist"]}

current_algorithm = ""
current_dataset = []
parameters = []
model_loaded = False
model_path = ""

class NNGUI(object):
    def setupUi(self, Dialog):
        Dialog.setFixedSize(397,297)
        Dialog.setObjectName("Dialog")
        Dialog.resize(397, 297)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 401, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.epoch_counter = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.epoch_counter.setObjectName("epoch_counter")
        self.epoch_counter.setValue(10)
        self.gridLayout.addWidget(self.epoch_counter, 1, 1, 1, 1)
        self.activation_combo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.activation_combo.setObjectName("activation_combo")
        self.activation_combo.addItem("")
        self.activation_combo.addItem("")
        self.activation_combo.addItem("")
        self.activation_combo.addItem("")
        self.gridLayout.addWidget(self.activation_combo, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.layers = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.layers.setObjectName("layers")
        self.gridLayout.addWidget(self.layers, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.runButtonCheck)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.activation_combo.setItemText(0, _translate("Dialog", "relu"))
        self.activation_combo.setItemText(1, _translate("Dialog", "sigmoid"))
        self.activation_combo.setItemText(2, _translate("Dialog", "tanh"))
        self.activation_combo.setItemText(3, _translate("Dialog", "linear"))
        self.label_2.setText(_translate("Dialog", "Epochs:"))
        self.label_3.setText(_translate("Dialog", "Layers ( neurons, comma seperated )"))
        self.label.setText(_translate("Dialog", "Activation function: "))
        self.layers.setText(_translate("Dialog", "128,128"))
        self.pushButton.setText(_translate("Dialog", "Run"))
    
    def runButtonCheck(self):
        global parameters
        if self.epoch_counter.value() < 1:
            ctypes.windll.user32.MessageBoxW(0,"Epochs cannot be less than 1","Warning",0)
            return
        parameters.append([int(i) for i in self.layers.text().split(',')])
        parameters.append(self.activation_combo.currentText())
        parameters.append(self.epoch_counter.value())
        Dialog.accept()
        
        
class KNNGUI(object):
    def setupUi(self, Dialog):
        Dialog.setFixedSize(280,113)
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
        Dialog.setFixedSize(621,378)
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
        self.AlgorithmCombo.addItems(["Linear Regression","K Nearest Neighbor","Neural Network"])
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
        self.newModel.setEnabled(False)
        self.LoadModel.setEnabled(False)
        self.DatasetCombo.addItems(["Test"])
        self.LoadDataset = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.LoadDataset.setObjectName("LoadDataset")
        self.horizontalLayout_2.addWidget(self.LoadDataset)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 2, 1, 1)
        self.ContinueButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ContinueButton.setObjectName("ContinueButton")
        self.gridLayout.addWidget(self.ContinueButton, 3, 0, 1, 1)

        self.LoadDataset.clicked.connect(self.checkLoadDataset)
        self.newModel.stateChanged.connect(self.checkNewModel)
        self.AlgorithmCombo.currentIndexChanged.connect(self.checkAlgorithmCombo)
        self.ContinueButton.clicked.connect(self.checkContinueButton)
        self.LoadModel.clicked.connect(self.checkLoadModel)
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

    def checkLoadModel(self):
        global model_loaded,model_path
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()
        model_loaded = True
        model_path = file_path
        self.ContinueButton.setEnabled(True)
        self.newModel.setEnabled(False)

    def checkNewModel(self):
        if self.newModel.isEnabled():
            self.ContinueButton.setEnabled(self.newModel.isChecked())
        self.LoadModel.setEnabled(not self.newModel.isChecked())

    def checkAlgorithmCombo(self):
        self.DatasetCombo.clear()
        if self.AlgorithmCombo.currentText() == "K Nearest Neighbor":
            self.newModel.setEnabled(False)
            self.LoadModel.setEnabled(False)
            self.ContinueButton.setEnabled(True)
            self.DatasetCombo.addItems(["2 groups separate","2 groups surrounded","3 groups"])
        elif self.AlgorithmCombo.currentText() == "Linear Regression":
            self.newModel.setEnabled(False)
            self.LoadModel.setEnabled(False)
            self.ContinueButton.setEnabled(True)
            self.DatasetCombo.addItems(["Test"])
        elif self.AlgorithmCombo.currentText() == "Neural Network":
            self.newModel.setEnabled(True)
            self.LoadModel.setEnabled(True)
            self.ContinueButton.setEnabled(False)
            self.LoadDataset.setEnabled(False)
            self.DatasetCombo.addItems(["Handwritten digits"])


    def checkContinueButton(self):
        global current_algorithm,current_dataset
        if self.AlgorithmCombo.currentIndex() != -1 and self.DatasetCombo.currentIndex() != -1:
                current_algorithm = self.AlgorithmCombo.currentText()
                current_dataset = Datasets[self.AlgorithmCombo.currentText()][self.DatasetCombo.currentIndex()]
                Dialog.accept()


    def checkLoadDataset(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfile()
        dataset = []
        if self.AlgorithmCombo.currentText() == "K Nearest Neighbor":
            dataset = convert_to_dataset_from_file_knn(file_path)
        elif self.AlgorithmCombo.currentText() == "Linear Regression":
            dataset = convert_to_dataset_from_file_linear_regression(file_path)
        self.DatasetCombo.addItem("Custom Dataset")
        self.DatasetCombo.setCurrentIndex(self.DatasetCombo.count()-1)
        Datasets[self.AlgorithmCombo.currentText()].append(dataset)

def convert_to_dataset_from_file_linear_regression(file):
    arr = [line.split() for line in file]
    dataset = []
    for i in range(len(arr)):
        new_arr = []
        for j in arr[i]:
            new_arr.append([float(j[0]),float(j[2])])
        dataset.append(new_arr)
    return dataset[0]

def convert_to_dataset_from_file_knn(file):
    arr = [line.split() for line in file]
    string = "bgrcmyk"
    new_arr = []
    dict_ = {}
    for i in range(len(arr)):
        new_arr = []
        for j in arr[i]:
            new_arr.append([float(j[0]), float(j[2])])
        color = random.choice(string)
        string = string.replace(color, "")
        dict_[color] = new_arr
    return dict_

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()

    if current_algorithm != None and current_dataset != None:
        if current_algorithm == "K Nearest Neighbor":
            Dialog = QtWidgets.QDialog()
            gui = KNNGUI()
            gui.setupUi(Dialog)
            Dialog.show()
            app.exec_()
        if current_algorithm == "Neural Network" and not model_loaded:
            Dialog = QtWidgets.QDialog()
            gui = NNGUI()
            gui.setupUi(Dialog)
            Dialog.show()
            app.exec_()
        elif current_algorithm == "Neural Network" and model_loaded:
            algorithm = NN(current_dataset,parameters,model=model_path)
    algorithm = Algorithms[current_algorithm](current_dataset,parameters)
    if current_algorithm == "Neural Network":
        nn.start()

