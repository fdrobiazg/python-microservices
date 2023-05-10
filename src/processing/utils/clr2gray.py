import cv2

def convert(img): 
    source = cv2.imread(img)
    converted = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)