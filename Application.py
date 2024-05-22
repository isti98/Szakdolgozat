from DetectBug import DetectBug
from Ui import Ui
from ImageFormat import ImageFormat

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QImage 
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit,  QDialog, QGraphicsPixmapItem
from PyQt5.QtWidgets import QFileDialog, QApplication, QGraphicsScene, QGraphicsView 
from PyQt5.uic import loadUi 


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        
        #Variables
        self.ui = Ui()
        self.detectBug = DetectBug()

        #Setups
        self.ui.setupUi(self)

        #GoupBox of Project
        self.ui.NewProject.clicked.connect(self.newProject)
        self.ui.LoadProject.clicked.connect(self.loadProject)
        self.ui.DeleteProject.clicked.connect(self.deleteProject)

        #GoupBox of Model
        self.ui.NewModel.clicked.connect(self.newModel)
        self.ui.LoadModel.clicked.connect(self.loadModel)
        self.ui.DeleteModel.clicked.connect(self.deleteModel)

        #GoupBox of Images
        self.ui.selectFolder.clicked.connect(self.selectFolder)
        self.ui.addImage.clicked.connect(self.addImage)
        self.ui.renameImage.clicked.connect(self.renameImage)
        self.ui.removeImage.clicked.connect(self.removeImage)
        self.ui.viewImage.clicked.connect(self.viewImage)

        #Detect Bug
        self.ui.detectBugsButton.clicked.connect(self.detect)
        

    #Connectted Functions
    #Project
    def newProject(self):
        name = self.askForInput("Creating new Project","The name of the new Project: ")
        if name != None:
            if self.ui.projects.new(name)==False :
                self.MessageBox("Error", "The given name is already taken, try with anotherone!")

    def loadProject(self):
            self.ui.projects.load(self.ui.images)
            self.ui.imagesTitle.setText(self.ui.projects.currentText())
            
    def deleteProject(self):
            workingDirectory = os.getcwd()
            if self.ui.projects.isEmpty():
                currentProject = os.path.join(workingDirectory ,self.ui.projects.path, self.ui.projects.currentText())
                if(currentProject == self.ui.images.currentPath):
                    self.ui.images.currentPath = None
                    self.ui.images.clear()
                    self.ui.imagesTitle.setText("")
                self.ui.projects.delete()

            else:
                if self.askForConfirmation("Confirm","The folder is not empty, are You sure y want to delete it?") : 
                    currentProject = os.path.join(workingDirectory ,self.ui.projects.path, self.ui.projects.currentText())
                    if(currentProject == self.ui.images.currentPath):
                        self.ui.images.currentPath = None
                        self.ui.images.clear()
                        self.ui.imagesTitle.setText("")
                    self.ui.projects.deleteAll()

    #Model
    def newModel(self):
        source = self.browseFiles("The name of the new Model: ", "Models (*.pt)")
        name = self.askForInput("Naming the new Model","The name of the new Model: ")
        if source[0] != "" and name != None :
            if self.ui.models.new(source[0], name)==False: 
                self.MessageBox("Error", "The given name is already taken, try with anotherone!")

    def loadModel(self):
        self.detectBug.load(self.ui.models.selectedModel()[1])
        if(self.detectBug.modelLoaded == False):
            self.ui.models.delete()
            self.MessageBox("Error", "The model has been deleted since it has been added it.")

            

    def deleteModel(self):
        self.ui.models.delete()
        

    #Image
    def selectFolder(self):
        folder = self.browseFolders("Select a new folder! ")
        if folder != "" :
            self.listImages(folder)
        else:    
            self.MessageBox("Error", "You didnt choose a folder")

    def listImages(self, folder):
        self.ui.imageBrowser.clear()
        self.ui.imageBrowser.currentPath = folder
        for name in os.listdir(folder):
            if ImageFormat.isImage(name):
                self.ui.imageBrowser.addItem(name)

        
    def addImage(self):
        if self.ui.imageBrowser.currentItem()!=None and self.ui.images.currentPath !=None:
            path = self.ui.imageBrowser.currentPath
            name = self.ui.imageBrowser.currentItem().text()
            if os.path.exists(os.path.join(path, name)) and os.path.exists(self.ui.images.currentPath) :
                self.ui.images.add(path, name)
            else:
                self.MessageBox("Error", "The chosen image or project doesnt exits anymore.")

    def renameImage(self):
        newName = self.askForInput("Renaming", "Give the new name of the image: ")
        if newName != None :
            if self.ui.images.rename(newName) ==False:
                self.MessageBox("Error", "The given name is already exits.")
    
    def removeImage(self):
        self.ui.images.remove()
    
    def viewImage(self):
        if self.ui.images.currentItem()!=None :
            image = os.path.join(self.ui.images.currentPath, self.ui.images.currentItem().text())
            self.showImage(image)

    #DetectBug
    def detect(self):
        if self.ui.projects.currentText()!=None:
            project = os.path.join(self.ui.projects.path, self.ui.projects.currentText())
            if self.ui.images.currentItem() !=None :
                image =self.ui.images.currentItem().text()
                detectedImage = self.detectBug.run(project, image)
                if( detectedImage != None ):
                    self.showImage(os.path.join(detectedImage, image))
            else:
                self.detectBug.runAll(project)
        else:
            self.MessageBox("Error", "No data to detect on!")

    def showImage(self, imageName):
        pix = QPixmap(imageName)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        self.ui.ImageView.setScene(scene)


    #Other methods
    def MessageBox(self, tittle, text ):
        msg = QMessageBox()
        msg.setWindowTitle(tittle)
        msg.setText(text)
        msg.exec_() 

    def askForConfirmation(self, tittle, text):
        result = False 
        msg = QMessageBox()
        msg.setWindowTitle(tittle)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.exec_() 
        if msg.standardButton(msg.clickedButton()) == QMessageBox.Ok:
            result = True
        return result

    def browseFiles(self,message,type):
        fname= QFileDialog.getOpenFileName(self, message,"",type)
        return fname

    def browseFolders(self, messsage):
        fname = QFileDialog.getExistingDirectory(self, messsage,"")
        return fname
    
    def askForInput(self,title, message):
        result =None
        text, ok = QInputDialog.getText(self, title, message) 
        if ok and text is not None:
            result = text
        return result

    def exit(self):
        QtWidgets.qApp.quit()


