import cv2
import numpy as np

class Vision:
    def __init__(self):
        pass

    def to_hsv(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def to_gray(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def blur(self, frame, ksize=(5, 5)):
        return cv2.GaussianBlur(frame, ksize, 0)
    
    def canny_edges(self, frame, low, high):
        return cv2.Canny(frame, low, high)

    def threshold(self, frame, low, high):
        return cv2.threshold(frame, low, high, cv2.THRESH_BINARY)

    def in_range(self, frame, low, high):
        return cv2.inRange(frame, low, high)
    
    def sobel(self, frame, x, y, ksize=5):
        if x:
            return cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize)
        elif y:
            return cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize)
        else:
            return cv2.Sobel(frame, cv2.CV_64F, 1, 1, ksize)

    def detect_ball(self, frame, low, high):
        hsv = self.to_hsv(frame)
        ball = self.in_range(hsv, low, high)
        return ball