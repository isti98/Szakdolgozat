from Images import Images
from ImageFormat import ImageFormat
from PyQt5 import QtWidgets

import os

class Projects(QtWidgets.QComboBox):
    def __init__(self, inheritedVar, path ):
        QtWidgets.QComboBox.__init__(self,inheritedVar)
        self.path=path
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        dir = os.listdir(self.path)
        for i in dir:
             self.addItem(i)
    
    def new(self, name):  
        noError= True
        if self.findText(name) == -1 and name !="":
            newDir = os.path.join(self.path, name)
            os.mkdir(newDir)
            self.addItem(name)
        else: 
            noError=False
        return noError

    def load(self, activeProject):
        if(self.currentText() != ""):
            activeProject.clear()
            workingDirectory = os.getcwd()
            dir = os.path.join(workingDirectory ,self.path, self.currentText())
            activeProject.currentPath = dir 
            for name in os.listdir(dir):
                if ImageFormat.isImage(name):
                    activeProject.addItem(name)

    def isEmpty(self):
        if self.count() > 0:
            currentItem = self.currentText()
            dir = os.path.join(self.path, currentItem)
            filesInProject = os.listdir(dir)
            return len(filesInProject)==0
    
    def delete(self):
        removedItem = self.currentText()
        self.removeItem(self.currentIndex())
        removedDir = os.path.join(self.path,removedItem)
        os.rmdir(removedDir)

    def deleteAll(self):
        removedItem = self.currentText()
        self.removeItem(self.currentIndex())
        dir = os.path.join(self.path, removedItem)
        predicts = os.path.join(dir, "predict")
        if os.path.exists(predicts): 
            filesInPrediction = os.listdir(predicts)
            for files in filesInPrediction:
                os.remove(os.path.join(predicts , files))
            os.rmdir(predicts)
        filesInProject = os.listdir(dir)
        for files in filesInProject:
            os.remove(os.path.join(dir, files))
        removedDir = os.path.join(self.path,removedItem)
        os.rmdir(removedDir)
