from ImageFormat import ImageFormat
from ultralytics import YOLO

import os

class DetectBug():
    def __init__(self):
        self.model = None
        self.modelLoaded = False

    def load(self, modelPath):
        if(os.path.exists(modelPath)):
            self.model = YOLO(modelPath)
            self.modelLoaded = True
        else:
            self.modelLoaded=False
        return self.modelLoaded

    def run(self, projectPath, imageName):
        detectedImage = None
        workingDir= os.getcwd()
        source = os.path.join(workingDir, projectPath, imageName)
        target = os.path.join(workingDir, projectPath)
        if self.modelLoaded and  os.path.exists(source):
            detectedImage = self.model.predict(source=source, project=target, save=True, exist_ok=True, imgsz=640, conf=0.5)[0].save_dir

        return detectedImage
        
    def runAll(self, projectPath):
        detectedImage = None
        workingDir= os.getcwd()
        target = os.path.join(workingDir, projectPath)
        if self.modelLoaded and self.isEmpty(projectPath):
            images=[]
            for i in os.listdir(projectPath):
                if ImageFormat.isImage(i):
                    source = os.path.join(projectPath, i)
                    images.append(source)

            detectedImage = self.model.predict(source=images, project=target, save=True, exist_ok=True, imgsz=640, conf=0.5)[0].save_dir
        
        return detectedImage 

    def isEmpty(self, projectPath):
        workingDir= os.getcwd()
        target = os.path.join(workingDir, projectPath)
        size = len(os.listdir(target))
        if os.path.exists(os.path.join(target,"predict")):
            size -=1
        return size > 0