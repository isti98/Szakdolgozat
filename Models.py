import os
from PyQt5 import  QtWidgets

class Models(QtWidgets.QComboBox):
    def __init__(self, inheritedVar, defaultPath):
        QtWidgets.QComboBox.__init__(self,inheritedVar)
        self.defaultPath = defaultPath
        self.pathOfModels=[]
        
        if not os.path.exists(self.defaultPath):
            os.mkdir(self.defaultPath)
        dir = os.listdir(self.defaultPath)
        for i in dir:
            if (i.endswith(".pt")):
                self.addItem(i)
                workingDirectory = os.getcwd()
                path =str(os.path.join(workingDirectory,defaultPath,i)).replace("\\","/")
                self.pathOfModels.append(path)

    def new(self, source, name):
        noError = True
        if self.findText(name) == -1:
            i = 0
            while i<self.count() and self.pathOfModels[i] != source:
                i+=1
            if(i>=self.count()):
                self.addItem(name)
                self.pathOfModels.append(str(source))
            else: 
                noError=False
        else: 
            noError = False
        return noError
    
    def selectedModel(self):
        return (self.currentText,self.pathOfModels[self.currentIndex()])

    def delete(self):
        if self.count() > 0:
            self.removeItem(self.currentIndex())
