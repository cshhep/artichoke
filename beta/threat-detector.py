import numpy as np
import cv2
import pyautogui
import time

screen_width, screen_height = pyautogui.size()

MAX_CONTOUR_AREA = 1000

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
ZOOM_BOX_WIDTH = 200
ZOOM_BOX_HEIGHT = 200

# color and boundries

lower_red = np.array([0, 0, 200])
upper_red = np.array([50, 50, 255])



while True:

    
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


    mask = cv2.inRange(frame, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        valid_contours = [c for c in contours if cv2.contourArea(c) < MAX_CONTOUR_AREA]


        if valid_contours:
            c = max(valid_contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            

        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        # center calculation
        center_x = x + w // 2
        center_y = y + h // 2
        

        box_width = 5  # adjust
        box_height = 5


        box_x1 = center_x - box_width // 2
        box_y1 = center_y - box_height // 2
        box_x2 = center_x + box_width // 2
        box_y2 = center_y + box_height // 2
        
        # drawing threat
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)
        
        # future prediction
        center_x = x + w // 2
        center_y = y + h // 2
        length = 10 
        
        end_x = int(center_x + length)
        end_y = center_y
        
        cv2.line(frame, (center_x, center_y), (end_x, end_y), (255, 0, 0), 2)
    frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    threat_region = frame[box_y1:box_y2, box_x1:box_x2]


    zoomed_threat = cv2.resize(threat_region, (ZOOM_BOX_WIDTH, ZOOM_BOX_HEIGHT))


    top_left_y = DISPLAY_HEIGHT - ZOOM_BOX_HEIGHT
    top_left_x = DISPLAY_WIDTH - ZOOM_BOX_WIDTH
        
        # "magnified" position
    frame[top_left_y:DISPLAY_HEIGHT, top_left_x:DISPLAY_WIDTH] = zoomed_threat

    
    box_x1 = max(0, box_x1)
    box_y1 = max(0, box_y1)
    box_x2 = min(frame.shape[1], box_x2)
    box_y2 = min(frame.shape[0], box_y2)


    if (box_x2 - box_x1 > 0) and (box_y2 - box_y1 > 0):
        threat_region = frame[box_y1:box_y2, box_x1:box_x2]
        zoomed_threat = cv2.resize(threat_region, (ZOOM_BOX_WIDTH, ZOOM_BOX_HEIGHT))



    cv2.imshow('AI Detection', frame)


    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
