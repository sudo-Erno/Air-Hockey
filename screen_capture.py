import win32api, win32con, win32gui, win32ui
import numpy as np

class ScreenCapture:

    def __init__(self, w = 1285, h = 750):
        self.WIDTH = w
        self.HEIGHT = h
    
    def capture(self):
        # [!] TODO Learn how this library works
        
        windowname = "Air Hockey"

        hwnd = win32gui.FindWindow(None, windowname)
        # hwnd = None

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.WIDTH, self.HEIGHT)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.WIDTH, self.HEIGHT), dcObj, (0,0), win32con.SRCCOPY)
        
        # dataBitMap.SaveBitmapFile(cDC, "my_screenshot.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (self.HEIGHT, self.WIDTH, 4) # If you don't reshape the image, it will have another size, which is the one I don't need
        
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img

if __name__ == "__main__":
    wn = ScreenCapture()
    wn.capture()