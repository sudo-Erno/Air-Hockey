import cv2
import numpy as np
from screen_capture import ScreenCapture
from vision_processing import Vision

def create_dataset(frame, i):
    filename = f"screenshot_{i}.jpg"
    filepath = r"C:\\Users\\Erno\\Documents\\ProgramasAtom\\AirHockeyAI\\Screenshots\\" + filename
    
    cv2.imwrite(filepath, frame)

class Agent:
    def __init__(self):
        self.WIDTH = 1180
        self.HEIGHT = 1000
        self.window = ScreenCapture(self.WIDTH, self.HEIGHT)
        self.vision = Vision()

    def capture(self):
        i = 0
        while True:
            screenshot = self.window.capture() # h, w, c
            hsv = self.vision.to_hsv(screenshot)

            # Modify the image so to see only the pitch
            hsv = hsv[60:self.HEIGHT-95, 15:self.WIDTH-15,:]

            # == BLACK ==
            low_black = np.array([0, 0, 0])
            high_black = np.array([150, 100, 130])
            ball = self.vision.in_range(hsv, low_black, high_black)

            # == RED ==
            low_red = np.array([0, 50, 50])
            high_red = np.array([10, 255, 255])

            mask1 = self.vision.in_range(hsv, low_red, high_red)
            
            low_red = np.array([170, 50, 50])
            high_red = np.array([180, 255, 255])

            mask2 = self.vision.in_range(hsv, low_red, high_red)

            players = mask1 + mask2

            # == players + ball ==
            items = ball + players
            
            # == Creates dataset ==
            # create_dataset(items, i)
            # i += 1

            # == Detecting goal ==
            is_goal = self.detect_if_goal(screenshot)

            # == Get how many goals have been made by each team ==
            cv2.imshow("Image", self.get_goals(screenshot))

            # cv2.imshow("Game", self.detect_if_goal(screenshot))
            
            if cv2.waitKey(1) == ord("q"):
                cv2.destroyAllWindows()
                break

    def detect_if_goal(self, frame):
        """
        Checks if the goal signs appears on the screen.
        """
        goal_alert = cv2.imread('./goal_frame_test.jpg') # This image has colors
        
        goal_alert = goal_alert[100:140, 530:670]
        frame = frame[100:140, 530:670]

        difference = cv2.absdiff(frame, goal_alert)
        difference = difference.astype(np.uint8)

        percentage = (np.count_nonzero(difference)*100) / difference.size

        if percentage < 75:
            print("Goal!")
            return True

    def get_goals(self, frame):
        """
        Checks how many goals have been made.

        returns: 2 frames, each with the score of each player.
        """
        goal_1 = frame [30:60, 500:550,:]
        return goal_1

if __name__ == "__main__":
    print("Play!")
    agent = Agent()
    agent.capture()