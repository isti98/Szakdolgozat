
class ImageFormat():
    imageType = [".bmp",".dng",".jpeg", ".jpg",".mpo", ".png", ".tif", ".tiff", ".webp", ".pfm"] 
    
    @staticmethod
    def isImage(fileName):
        result =True
        i = 0
        length = len(ImageFormat.imageType)
        while i<length and fileName.endswith(ImageFormat.imageType[i])==False:
            i+=1
        if i >= length:
            result=False
        return result