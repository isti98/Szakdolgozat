from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


import shutil
import os

class Images(QtWidgets.QListWidget):
    def __init__(self, inheritedVar):
        QtWidgets.QListWidget.__init__(self,inheritedVar)
        self.currentPath=None

    def add(self, path, name):
        noError= True
        if len(self.findItems(name, Qt.MatchExactly)) == 0:
            self.addItem(name)
            source = os.path.join(path, name)
            target = os.path.join(self.currentPath, name)
            shutil.copyfile(source, target)
        else: 
            noError = False
        return noError
    
    def rename(self, newName):
        noError= True
        if(self.currentItem()!=None):
            newName = newName + self.format(self.currentItem().text())
            if len(self.findItems(newName, Qt.MatchExactly)) == 0:
                source = os.path.join(self.currentPath, self.currentItem().text())
                target = os.path.join(self.currentPath, newName)
                self.currentItem().setText(newName)
                os.rename(source, target)
            else:
                noError = False
        else: 
            noError = False
        return noError

    def remove(self):
        if self.currentItem()!=None:
            imagePath= os.path.join(self.currentPath, self.currentItem().text())
            os.remove(imagePath)
            self.takeItem(self.currentRow())

    def format(self, name):
        staringIndex = name.find(".")
        return name[staringIndex:]
